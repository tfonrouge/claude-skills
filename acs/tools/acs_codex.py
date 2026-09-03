#!/usr/bin/env python3
"""ACS (Analyze, Criticize, Suggest) over Codex — implementation.

Invoked through acs-codex.sh, which resolves the interpreter. Standard library only: a shipped
skill must not inherit whatever happens to be installed on one machine.

Exit codes
  0  a valid advisory was rendered
  1  Codex answered but the document or the renderer invariants failed
  2  usage, python, binary, capability, auth, effort shape, schema dialect or self-test, Git,
     instruction source, or receiver-guard error   (nothing was sent to Codex, or nothing was paid)
  3  Codex invocation failed or rejected the configuration
"""

import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(SKILL_DIR, "schemas", "acs-output.schema.json")
PROMPT_PATH = os.path.join(SKILL_DIR, "references", "acs.prompt.md")
CAPABILITY = "advisory-v1"
MAX_OUTPUT_BYTES = 256 * 1024
DEFAULT_TIMEOUT = 900
FALLBACK_CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
EXEC_FLAGS = ["--ephemeral", "--ignore-user-config", "--sandbox", "--output-schema",
              "--output-last-message"]
EFFORT_RE = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")
DELIM_RE = re.compile(r"^--- (?:BEGIN|END) (?:ADVISORY|ROAR|ACS-DIAGNOSTIC) ---$")

DIALECT = {"type", "required", "properties", "items", "enum", "pattern",
           "minItems", "maxItems", "minLength", "maxLength", "additionalProperties"}
ANNOTATIONS = {"$schema", "$id", "title", "description", "default", "examples", "$comment"}


class Fail(Exception):
    def __init__(self, code, message, raw=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.raw = raw


# ---------------------------------------------------------------- text handling

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[@-Z\\-_]")
# every character that could start a new line, hide text, or reorder it visually
LINE_BREAKS = "\r\n\x0b\x0c\u2028\u2029\u0085"
SCRUB_RE = re.compile(r"[\x00-\x08\x0e-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069\ufeff]")


def field(value):
    """The one normalization. EVERY value rendered into a block goes through it — model names,
    versions, paths, hashes, focus text and model output alike, because a header field that skips
    it can close the block and forge content outside it.

    Removes ANSI/OSC escape sequences, turns every line break (CR, LF, VT, FF, NEL, U+2028,
    U+2029) into a single space, and replaces the remaining C0/C1 controls, bidirectional
    overrides and BOM with U+FFFD so the substitution stays visible. The result is always exactly
    one line.
    """
    text = str(value)
    text = ANSI_RE.sub("", text)
    for ch in LINE_BREAKS:
        text = text.replace(ch, " ")
    text = SCRUB_RE.sub("\ufffd", text)
    text = text.replace("\t", " ")
    return " ".join(text.split()).strip()


def seal(lines):
    """Guarantee the block's frame: only the intended first and last lines may be delimiters."""
    body = [("\\" + line if DELIM_RE.match(line) else line) for line in lines[1:-1]]
    return [lines[0]] + body + [lines[-1]]


def run(cmd, **kw):
    kw.setdefault("stdout", subprocess.PIPE)
    kw.setdefault("stderr", subprocess.PIPE)
    kw.setdefault("universal_newlines", True)
    return subprocess.run(cmd, **kw)


def codex_error(stderr, stdout):
    """Codex reports failures as a JSON blob on stderr; the last line of it is a brace.

    Prefer the "message" field when there is one, else the first line that looks like an error,
    else the last non-empty line. Truncated, and escaped like every other rendered field.
    """
    text = (stderr or "") + "\n" + (stdout or "")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        if '"message"' in line:
            try:
                return field(json.loads("{" + line.rstrip(",") + "}")["message"])[:600]
            except Exception:
                return field(line)[:600]
    for line in lines:
        if line.startswith("ERROR") or "error" in line.lower():
            return field(line)[:600]
    return field(lines[-1]) if lines else "no message"

# ---------------------------------------------------------------- schema subset

def check_dialect(node, where="<root>"):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ANNOTATIONS:
                continue
            if key not in DIALECT:
                raise Fail(2, "schema uses keyword outside the ACS dialect: %r at %s" % (key, where))
            if key == "pattern":
                try:
                    re.compile(value)
                except re.error as exc:
                    raise Fail(2, "schema pattern does not compile at %s: %s" % (where, exc))
            if key in ("properties", "items"):
                if isinstance(value, dict) and key == "properties":
                    for name, sub in value.items():
                        check_dialect(sub, "%s.%s" % (where, name))
                else:
                    check_dialect(value, where + "[]")
    elif isinstance(node, list):
        for i, sub in enumerate(node):
            check_dialect(sub, "%s[%d]" % (where, i))


def type_ok(value, expected):
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    raise Fail(2, "schema uses an unsupported type: %r" % expected)


def validate(value, schema, path="$"):
    """Errors are accumulated as a list of human-readable strings."""
    errs = []
    if "type" in schema and not type_ok(value, schema["type"]):
        return ["%s: expected %s, got %s" % (path, schema["type"], type(value).__name__)]
    if "enum" in schema and value not in schema["enum"]:
        errs.append("%s: %r is not one of %s" % (path, value, schema["enum"]))
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append("%s: shorter than %d characters" % (path, schema["minLength"]))
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append("%s: longer than %d characters" % (path, schema["maxLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append("%s: %r does not match %s" % (path, value, schema["pattern"]))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append("%s: fewer than %d items" % (path, schema["minItems"]))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append("%s: more than %d items" % (path, schema["maxItems"]))
        if "items" in schema:
            for i, item in enumerate(value):
                errs += validate(item, schema["items"], "%s[%d]" % (path, i))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errs.append("%s: missing required property %r" % (path, name))
        if schema.get("additionalProperties") is False:
            for name in value:
                if name not in props:
                    errs.append("%s: unexpected property %r" % (path, name))
        for name, sub in props.items():
            if name in value:
                errs += validate(value[name], sub, "%s.%s" % (path, name))
    return errs


# ---------------------------------------------------------------- preflight

def git_root():
    res = run(["git", "rev-parse", "--show-toplevel"])
    if res.returncode != 0:
        raise Fail(2, "not inside a Git work tree; ACS v1 requires one")
    return os.path.realpath(res.stdout.strip())


def git_context(root):
    head = run(["git", "-C", root, "rev-parse", "--short", "HEAD"])
    head = head.stdout.strip() if head.returncode == 0 else "no-commit"
    st = run(["git", "-C", root, "status", "--porcelain"])
    if st.returncode != 0:
        # "we could not tell" must never be rendered as "clean": the header would state a fact
        # that was never established. Nothing has been spent yet, so this is a preflight error.
        raise Fail(2, "cannot determine the worktree state of %s: %s"
                   % (root, (st.stderr or st.stdout or "git status failed").strip()[:200]))
    dirty = "dirty" if st.stdout.strip() else "clean"
    return head, dirty


def resolve_codex():
    env = os.environ.get("ACS_CODEX_BIN")
    if env:
        if not (os.path.isfile(env) and os.access(env, os.X_OK)):
            raise Fail(2, "ACS_CODEX_BIN is not an executable file: %s" % env)
        return env
    found = shutil.which("codex")
    if found:
        return found
    if os.path.isfile(FALLBACK_CODEX) and os.access(FALLBACK_CODEX, os.X_OK):
        return FALLBACK_CODEX
    raise Fail(2, "codex binary not found (PATH, ACS_CODEX_BIN, or %s)" % FALLBACK_CODEX)


def probe_capabilities(codex):
    res = run([codex, "exec", "--help"])
    if res.returncode != 0:
        raise Fail(2, "`codex exec --help` failed: %s" % (res.stderr or res.stdout).strip()[:200])
    text = res.stdout + res.stderr
    missing = [f for f in EXEC_FLAGS if f not in text]
    if missing:
        raise Fail(2, "this codex build lacks required options: %s" % ", ".join(missing))
    res = run([codex, "login", "--help"])
    if res.returncode != 0 or "status" not in (res.stdout + res.stderr):
        raise Fail(2, "this codex build has no `login status`")
    ver = run([codex, "--version"])
    return (ver.stdout.strip() or "unknown") if ver.returncode == 0 else "unknown"


def login_method(codex):
    res = run([codex, "login", "status"])
    if res.returncode != 0:
        raise Fail(2, "codex is not authenticated (`codex login status` failed); run `codex login`")
    text = (res.stdout + res.stderr).lower()
    if "api key" in text or "api-key" in text:
        return "API key"
    if "chatgpt" in text or "account" in text:
        return "ChatGPT account"
    return "authenticated (method not reported)"


def instruction_sources(root):
    """Sources Codex would load for `codex exec -C <root> --ignore-user-config`.

    Verified precedence, from the Codex binary: AGENTS.override.md, AGENTS.md, then configured
    fallback filenames — the last of which --ignore-user-config drops. Only the global directory
    and the working directory (which is `root`, because we pass -C) are part of the chain: deeper
    nested files are not, and refusing them would block for nothing.
    """
    home = os.environ.get("CODEX_HOME") or os.path.expanduser("~/.codex")
    found = []
    for base in (home, root):
        for name in ("AGENTS.override.md", "AGENTS.md"):
            path = os.path.join(base, name)
            if not os.path.lexists(path):
                continue
            # Fail closed: a candidate that exists but cannot be inspected may still be loaded by
            # Codex, so "we could not read it" must never be reported as "it is not there".
            if not os.path.isfile(path):
                raise Fail(2, "a Codex instruction file exists but is not a readable regular file, "
                              "so its content cannot be determined: %s" % path)
            try:
                content = open(path, encoding="utf-8", errors="replace").read()
            except OSError as exc:
                raise Fail(2, "a Codex instruction file exists but cannot be read, so it cannot be "
                              "determined whether it is empty: %s (%s)" % (path, exc))
            if content.strip():
                found.append(path)
                break  # precedence: the first non-empty one at this level wins
    return found


def resolve_auditor():
    if os.environ.get("ACS_TESTING") == "1" and os.environ.get("ACS_ROAR_AUDITOR"):
        return os.environ["ACS_ROAR_AUDITOR"]
    skills_dir = os.path.dirname(SKILL_DIR)
    for cand in (os.path.join(skills_dir, "owner-roar-protocol", "tools", "roar-install-check.sh"),):
        if os.path.isfile(cand):
            return cand
    raise Fail(2, "owner-roar-protocol auditor not found next to this skill; ACS requires "
                  "owner-roar-protocol 0.1.3 or later")


def receiver_guard(root):
    auditor = resolve_auditor()
    if not (os.path.isfile(auditor) and os.access(auditor, os.X_OK)):
        raise Fail(2, "auditor is not executable: %s" % auditor)
    help_res = run([auditor, "--help"])
    if "--receiver" not in (help_res.stdout + help_res.stderr):
        raise Fail(2, "the installed owner-roar-protocol auditor does not support the receiver "
                      "guard; upgrade to 0.1.3 or later")
    receiver = os.path.join(root, "CLAUDE.md")
    res = run([auditor, "--receiver", receiver, "--require-capability", CAPABILITY, "--quiet"])
    if res.returncode != 0:
        detail = (res.stderr or res.stdout).strip().splitlines()
        detail = detail[-1] if detail else "no detail"
        raise Fail(2, "receiver protocol does not declare %s; install or upgrade with "
                      "/owner-roar-protocol, then start a new session (%s)" % (CAPABILITY, detail))
    return receiver


# ---------------------------------------------------------------- rendering

def render_advisory(doc, meta):
    lines = ["--- BEGIN ADVISORY ---", "Type: ACS"]
    lines.append("Source: codex %s · model requested: %s · model reported: unavailable · auth %s · %s"
                 % (field(meta["codex_version"]), field(meta["model_requested"]),
                    field(meta["auth"]), field(meta["date"])))
    lines.append("Context: repo %s · HEAD %s · worktree %s   (context only, not a reproducible identity)"
                 % (field(meta["root"]), field(meta["head"]), field(meta["dirty"])))
    lines.append("Focus: " + field(meta["focus"]))
    lines.append("Summary: " + field(doc["summary"]))
    for item in doc["items"]:
        lines.append("%s · %s" % (field(item["id"]), field(item["title"])))
        for text, key_a, key_b, label in (
                ("observations", "text", "evidence", "  Observed (evidence): "),
                ("claims_to_verify", "text", "how_to_check", "  To verify (how): "),
                ("inferences", "text", "from", "  Inferred (from): "),
                ("alternatives", "text", "tradeoff", "  Alternatives (tradeoff): "),
                ("costs_and_risks", "text", "level", "  Costs / risks (level): ")):
            for entry in item.get(text, []):
                lines.append("%s%s [%s]" % (label, field(entry[key_a]), field(entry[key_b])))
        lines.append("  Critique: " + field(item["critique"]))
        lines.append("  Suggestion: " + field(item["suggestion"]))
    if not doc["items"]:
        lines.append("No material proposals.")
    for note in doc.get("not_verified", []):
        lines.append("Not verified: " + field(note))
    lines.append("--- END ADVISORY ---")
    lines = seal(lines)
    if doc["items"]:
        lines.append("")
        lines.append("@Owner-Disposition")
        for item in doc["items"]:
            lines.append("%s: ___" % field(item["id"]))
    return "\n".join(lines)


def render_diagnostic(fail, raw_bytes):
    """The raw is never printed: only its size and digest, so a caller can correlate it."""
    raw_bytes = raw_bytes or b""
    lines = ["--- BEGIN ACS-DIAGNOSTIC ---",
             "Type: ACS",
             "Result: failed",
             "Exit: %d" % fail.code,
             "Error: " + field(fail.message),
             "raw: %d bytes, sha256 %s" % (len(raw_bytes), hashlib.sha256(raw_bytes).hexdigest()),
             "--- END ACS-DIAGNOSTIC ---"]
    return "\n".join(seal(lines))


# ---------------------------------------------------------------- main

USAGE = ("usage: acs-codex.sh [--model M] [--effort E] [--timeout S] [--dry-run] -- <focus text>")


def parse_args(argv):
    opts = {"model": None, "effort": None, "timeout": DEFAULT_TIMEOUT, "dry_run": False, "focus": None}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--":
            focus = " ".join(argv[i + 1:]).strip()
            if not focus:
                raise Fail(2, "no focus text after `--`\n" + USAGE)
            opts["focus"] = focus
            return opts
        if a == "--dry-run":
            opts["dry_run"] = True
        elif a in ("--model", "--effort", "--timeout"):
            i += 1
            if i >= len(argv):
                raise Fail(2, "%s needs a value\n%s" % (a, USAGE))
            opts[a[2:]] = argv[i]
        elif a in ("-h", "--help"):
            print(USAGE)
            sys.exit(0)
        else:
            raise Fail(2, "unknown argument %r (options must precede `--`)\n%s" % (a, USAGE))
        i += 1
    raise Fail(2, "missing `--` before the focus text\n" + USAGE)


def main(argv):
    opts = parse_args(argv)
    if opts["effort"] is not None and not EFFORT_RE.match(opts["effort"]):
        raise Fail(2, "malformed --effort value %r" % opts["effort"])
    try:
        timeout = int(opts["timeout"])
        if timeout <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise Fail(2, "--timeout must be a positive integer")

    # schema first: a broken schema must never cost usage
    schema_path = SCHEMA_PATH
    if os.environ.get("ACS_TESTING") == "1" and os.environ.get("ACS_SCHEMA_PATH"):
        # test hook, not a public interface: it lets the harness exercise schema variants against a
        # temporary copy instead of mutating the shipped file
        schema_path = os.environ["ACS_SCHEMA_PATH"]
    try:
        schema = json.load(open(schema_path, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Fail(2, "cannot read the ACS schema: %s" % exc)
    check_dialect(schema)
    try:
        prompt_body = open(PROMPT_PATH, encoding="utf-8").read()
    except OSError as exc:
        raise Fail(2, "cannot read the ACS prompt: %s (%s)" % (PROMPT_PATH, exc))

    root = git_root()
    sources = instruction_sources(root)
    if sources:
        raise Fail(2, "ACS v1 does not run with Codex project instructions present (%s); the Owner "
                      "must decide how they reconcile with the ACS contract" % ", ".join(sources))
    receiver = receiver_guard(root)
    codex = resolve_codex()
    version = probe_capabilities(codex)
    auth = login_method(codex)
    head, dirty = git_context(root)

    prompt = (prompt_body.rstrip("\n") + "\n\n## Focus for this run\n\n" + opts["focus"] + "\n")

    tmp = tempfile.mkdtemp(prefix="acs-")
    try:
        final = os.path.join(tmp, "final.json")
        cmd = [codex, "exec", "--ephemeral", "--ignore-user-config", "-s", "read-only",
               "-C", root, "--output-schema", schema_path, "-o", final]
        if opts["model"]:
            cmd += ["-m", opts["model"]]
        if opts["effort"]:
            cmd += ["-c", "model_reasoning_effort=%s" % opts["effort"]]
        cmd.append("-")

        model_requested = opts["model"] or "default (Codex built-in, user config ignored)"
        if opts["dry_run"]:
            print("ACS preflight")
            print("  codex        : %s (%s)" % (codex, version))
            print("  auth         : %s" % auth)
            print("  repo         : %s (HEAD %s, worktree %s)" % (root, head, dirty))
            print("  receiver     : %s — capability %s declared" % (receiver, CAPABILITY))
            print("  instructions : none applicable (AGENTS.override.md / AGENTS.md, global and repo root)")
            print("  schema       : %s (dialect ok)" % schema_path)
            print("  model        : %s" % model_requested)
            print("  timeout      : %ds" % timeout)
            print("\nCommand (not executed):\n  " + shlex.join(cmd))
            print("\nPrompt on stdin:\n" + prompt)
            return 0

        try:
            res = subprocess.run(cmd, input=prompt, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            captured = b"".join(part if isinstance(part, bytes) else (part or "").encode("utf-8")
                                for part in (exc.stdout, exc.stderr))
            raise Fail(3, "Codex invocation timed out after %ds" % timeout, captured)
        except OSError as exc:
            raise Fail(3, "Codex invocation failed: %s" % exc)
        if res.returncode != 0:
            captured = ((res.stdout or "") + (res.stderr or "")).encode("utf-8")
            raise Fail(3, "Codex invocation failed or rejected the configuration (exit %d): %s"
                       % (res.returncode, codex_error(res.stderr, res.stdout)), captured)
        if not os.path.isfile(final):
            raise Fail(3, "Codex produced no final message file",
                       ((res.stdout or "") + (res.stderr or "")).encode("utf-8"))
        raw = open(final, "rb").read()
        if not raw.strip():
            raise Fail(3, "Codex returned empty output", raw)
        if len(raw) > MAX_OUTPUT_BYTES:
            raise Fail(1, "Codex output is %d bytes, over the %d byte cap"
                       % (len(raw), MAX_OUTPUT_BYTES), raw)
        try:
            doc = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise Fail(1, "Codex output is not valid JSON: %s" % exc, raw)

        errors = validate(doc, schema)
        if errors:
            raise Fail(1, "output does not satisfy the schema: " + "; ".join(errors[:5]), raw)
        ids = [item["id"] for item in doc["items"]]
        expected = ["ACS-%02d" % (n + 1) for n in range(len(ids))]
        if ids != expected:
            raise Fail(1, "item ids must be unique, ordered and consecutive from ACS-01; got %s"
                       % (", ".join(ids) or "none"), raw)

        print(render_advisory(doc, {
            "codex_version": version, "model_requested": model_requested, "auth": auth,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "root": root, "head": head, "dirty": dirty, "focus": opts["focus"]}))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Fail as failure:
        if failure.code in (1, 3):
            print(render_diagnostic(failure, failure.raw))
        else:
            sys.stderr.write("acs: " + failure.message + "\n")
        sys.exit(failure.code)
    except KeyboardInterrupt:
        sys.stderr.write("acs: interrupted\n")
        sys.exit(3)
