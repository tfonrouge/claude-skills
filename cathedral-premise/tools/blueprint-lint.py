#!/usr/bin/env python3
"""blueprint-lint — deterministic validator for the DIRECTIVE blueprint protocol.

Ships inside the cathedral-premise skill so `install.sh` distributes it; audits invoke it as
`python3 <skill-root>/cathedral-premise/tools/blueprint-lint.py <blueprint-root>`.

SCOPE — read this before trusting a clean run:

  Owns   the mechanical half of Directive Integrity: schema, vocabularies, sequence, placement,
         link targets, dotfile caps, and the arithmetic it can actually re-derive.
  Partly re-derives completeness: it resolves each coverage-set obligation against carrier rows
         and re-derives the **denominator**. It CANNOT re-derive the **numerator** — "verified"
         vocabularies are project-specific (Implementado / Verified / Done…) and undeclared, so
         the verified count remains self-reported and is flagged as such.
  Never  judges meaning: whether a coverage set truly proves its OC, whether an attestation is
         credible, whether implementation displaced the criteria. That stays with Owner + ROAR.

A clean run is necessary and never sufficient.

    python3 blueprint-lint.py <blueprints-root> [--quiet]

Exit 0 = clean, 1 = errors, 2 = usage. Findings print as `LEVEL path: message`.
"""
import os
import re
import sys

STATES = {"UNMAPPED", "NOT STARTED", "IN PROGRESS", "BLOCKED", "FAILED", "MET"}
ASSURANCE = {"REPLAYABLE", "ATTESTED", "MIXED"}
BLOCKING_STATES = {"UNMAPPED", "BLOCKED", "FAILED"}
COMPLETE_STATUSES = {"STABLE", "CLOSED"}
REGISTER_STATES = {"OPEN", "CLEARED", "SATISFIED", "WAIVED"}
# mode → its ONE mapping carrier. Selecting "the first file that exists" accepted a carrier the
# mode does not use (a (MODULE) validating against IMPLEMENTATION_PLAN.md).
SKILL_MODES = {
    "business": {"MODULE": "TRACEABILITY_MATRIX.md", "LIBRARY": "TRACEABILITY_MATRIX.md",
                 "BRIDGE": "IMPLEMENTATION_ORDER.md"},
    "systems":  {"SUBSYSTEM": "TRACEABILITY.md", "FEATURE": "IMPLEMENTATION_PLAN.md",
                 "PATCH": "CHANGESET.md"},
}
MODE_CARRIER = {**SKILL_MODES["business"], **SKILL_MODES["systems"]}
CARRIERS = list(dict.fromkeys(MODE_CARRIER.values()))
STATUS_WORD_SOFT = 60         # a status file is a status, not a changelog
STATUS_WORD_HARD = 150        # above this it is unambiguously a changelog
OBLIGATION_ID = re.compile(r"\b([A-Z][A-Z0-9]{1,15}-[0-9][0-9A-Za-z/]*)\b")

findings = []


def add(level, path, msg):
    findings.append((level, path, msg))


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def rows(block):
    """Physical data rows of a markdown table: '| … |' minus header and separator."""
    out = []
    for ln in (block or "").splitlines():
        s = ln.strip()
        if s.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", s):
            out.append(s)
    return out


def physical_rows(block):
    """Physical data rows of a section, whichever form it uses: markdown table rows (minus the
    header) or checklist items. Real plans use checklists; real matrices use tables."""
    checks = [l for l in (block or "").splitlines() if re.match(r"\s*[-*]\s*\[[ xX]\]", l)]
    if checks:
        return len(checks)
    tbl = rows(block)
    return max(len(tbl) - 1, 0)


def cells(row):
    return [c.strip() for c in row.strip("|").split("|")]


def section(text, heading_re):
    """Body of the first heading matching heading_re, up to the next heading of the SAME OR
    SHALLOWER level. Stopping at *any* heading truncated sections at their own subheadings."""
    lines = (text or "").splitlines()
    start = level = None
    for i, ln in enumerate(lines):
        m = re.match(r"(#{1,6})\s", ln)          # only headings — a prose mention is not a section
        if m and re.search(heading_re, ln):
            level = len(m.group(1))
            start = i + 1
            break
    if start is None:
        return None
    for j in range(start, len(lines)):
        m = re.match(r"(#{1,6})\s", lines[j])
        if m and len(m.group(1)) <= level:
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


def foreign_kind(val):
    """Contractual distinction: a mode from the OTHER skill's catalog is a different finding from
    a value outside every catalog. Conflating them mislabels genuinely unknown values."""
    return "another skill's catalog" if val in MODE_CARRIER else "outside every known catalog"


def brief_mode(bp, catalog):
    """BRIEF `Mode` declaration per the recognizer: a `Mode` field in the HEADER REGION (before
    the first `##`), as `| Mode | X |` or inline `Mode: X`, bold markers allowed, bare literal."""
    text = read(os.path.join(bp, "BRIEF.md")) or ""
    header = re.split(r"^##\s", text, maxsplit=1, flags=re.M)[0]
    m = (re.search(r"\|\s*\*{0,2}Mode\*{0,2}\s*\|\s*\*{0,2}([A-Z]+)\*{0,2}\s*\|", header)
         or re.search(r"\*{0,2}Mode\*{0,2}\s*[:：]\s*\*{0,2}([A-Z]+)", header))
    if not m:
        return None, None
    val = m.group(1)
    return (val, None) if val in catalog else (None, val)


def index_mode(root, bp_dir, catalog):
    """INDEX declaration: the Mode column of this blueprint's row, else the section→mode map
    (*Active Bridges* ⇒ BRIDGE). Other sections declare nothing."""
    text = read(os.path.join(root, "INDEX.md")) or read(os.path.join(root, "index.md")) or ""
    sec, mode_col = None, None
    for ln in text.splitlines():
        if ln.startswith("## "):
            sec, mode_col = ln, None
            continue
        if not ln.strip().startswith("|"):
            continue
        cs = [c.strip().strip("*") for c in ln.strip("|").split("|")]
        if mode_col is None and any(c.lower() == "mode" for c in cs):
            mode_col = next(i for i, c in enumerate(cs) if c.lower() == "mode")
            continue                       # header row: learn the column, never read values here
        # row identity is the FIRST cell only — `bp_dir in ln` matched any row that merely
        # *mentioned* the blueprint (e.g. in another row's Notes)
        if bp_dir not in cs[0]:
            continue
        if mode_col is not None and mode_col < len(cs):
            val = cs[mode_col]
            if val in catalog:
                return val, None
            if re.fullmatch(r"[A-Z][A-Z_]{2,}", val):
                return None, val           # a foreign declaration, not "declares nothing"
        if sec and re.search(r"Active Bridges", sec, re.I) and "BRIDGE" in catalog:
            return "BRIDGE", None
        return None, None
    return None, None


def reconcile_mode(root, bp, name, catalog):
    """Cathedral Mode Reconciliation over its three sources, with precedence
    BRIEF > unambiguous suffix > INDEX > ambiguous-suffix default, and drift reporting."""
    sfx = re.search(r"\(([A-Z]+)\)\s*$", name)
    suffix = sfx.group(1) if sfx else None
    foreign_sfx = suffix if suffix and suffix not in catalog else None
    ambiguous = suffix == "MODULE" and "LIBRARY" in catalog     # legacy LIBRARY may wear (MODULE)

    b_mode, b_foreign = brief_mode(bp, catalog)
    i_mode, i_foreign = index_mode(root, name, catalog)

    decls = {k: v for k, v in (("BRIEF", b_mode),
                               ("suffix", None if (ambiguous or foreign_sfx) else suffix),
                               ("INDEX", i_mode)) if v}
    drift = len(set(decls.values())) > 1
    resolved = b_mode or (None if (ambiguous or foreign_sfx) else suffix) or i_mode \
        or (suffix if suffix in catalog else None)
    # an ambiguous `(MODULE)` is not a blank cheque: its possible set is {MODULE, LIBRARY}. A
    # resolved mode outside that set contradicts the directory and is drift.
    if ambiguous and resolved and resolved not in {"MODULE", "LIBRARY"}:
        drift = True
        decls["suffix(ambiguous)"] = "MODULE|LIBRARY"
    return {"mode": resolved, "foreign_suffix": foreign_sfx, "foreign_brief": b_foreign,
            "foreign_index": i_foreign, "drift": drift, "decls": decls}


def designated_skill(root):
    """The project's blueprint skill, from its CLAUDE.md cathedral config. Classifying against the
    global mode union would borrow a foreign contract — cathedral forbids that."""
    for up in (os.path.join(root, ".."), root, os.path.join(root, "..", "..")):
        p = os.path.join(up, "CLAUDE.md")
        m = re.search(r"Blueprint skill:\s*(\S+)", read(p) or "")
        if m:
            val = m.group(1).strip().strip("`\"'")
            known = {"business-blueprint-workflow": "business", "business": "business",
                     "systems-blueprint-workflow": "systems", "systems": "systems"}
            if val in known:                     # exact enum — substring matching accepted
                return known[val], None          # values like "unrelated-business-tool"
            return None, f"declared blueprint skill '{val}' is not a known catalog"
    return None, "no `Blueprint skill:` declared in CLAUDE.md"


def check_directive(bp, name):
    d = read(os.path.join(bp, "DIRECTIVE.md"))
    if d is None:
        return None                       # non-adopter: check 1 is severity-tiered, not ours
    auth = re.search(r"^\*\*Authority:\*\*\s*(\S+)", d, re.M)
    if not auth:
        # a DIRECTIVE that exists but has no Authority field is MALFORMED, never "legacy"
        add("ERROR", name, "DIRECTIVE.md has no `**Authority:**` header field")
        return {"state": None, "revision": None, "ocs": [], "text": d}
    state = auth.group(1)
    if state not in {"DRAFT", "APPROVED", "REVOKED"}:
        add("ERROR", name, f"Authority '{state}' outside DRAFT|APPROVED|REVOKED")
    rev = re.search(r"^\*\*Revision:\*\*\s*(\d+)", d, re.M)
    if not rev:
        add("ERROR", name, "DIRECTIVE.md has no `**Revision:**` field")
    ocs = re.findall(r"^-\s*(OC-\d+):", d, re.M)
    if not ocs:
        add("ERROR", name, "DIRECTIVE.md declares no `OC-##` outcome criteria")
    dup = {o for o in ocs if ocs.count(o) > 1}
    if dup:
        add("ERROR", name, f"duplicate OC ids in DIRECTIVE.md: {sorted(dup)}")
    cut = d.find("## Amendment History")
    body = d[:cut] if cut > 0 else d
    n = len([l for l in body.splitlines() if l.strip()])
    if n > 45:
        add("WARN", name, f"DIRECTIVE normative body is {n} non-blank lines (one-screen cap ~30)")
    if state == "APPROVED" and not re.search(r"Approved by:\*\*\s*@\S", d):
        add("ERROR", name, "Authority APPROVED but no `Approved by: @…` recorded")
    return {"state": state, "revision": int(rev.group(1)) if rev else None,
            "ocs": ocs, "text": d}


# -------------------------------------------- amendment lineage (both storages)
def check_lineage(bp, name, directive):
    if not directive or directive["state"] == "DRAFT":
        return
    ledger = read(os.path.join(bp, "LEDGER.md"))
    seq = [int(m.group(1)) for m in re.finditer(r"DIRECTIVE R(\d+):", ledger or "")]
    hist = [int(m.group(1)) for m in
            re.finditer(r"^-\s*R(\d+)\s", section(directive["text"], r"^##\s+Amendment History") or "", re.M)]
    combined = seq or hist          # cathedral uses LEDGER; non-cathedral uses Amendment History
    store = "LEDGER" if seq else ("Amendment History" if hist else None)
    if not combined:
        add("ERROR", name, "adopted directive has neither a `DIRECTIVE R<N>:` ledger row nor an "
                           "Amendment History R-line")
        return
    if len(combined) != len(set(combined)):
        add("ERROR", name, f"duplicate R numbers in {store}: {sorted(combined)}")
    if sorted(set(combined)) != list(range(1, max(combined) + 1)):
        add("ERROR", name, f"R-sequence in {store} not contiguous from 1: {sorted(set(combined))}")
    if directive["revision"] is not None and max(combined) != directive["revision"]:
        add("ERROR", name, f"highest amendment R{max(combined)} != DIRECTIVE Revision {directive['revision']}")

    cur = None
    for ln in (ledger or "").splitlines():
        if ln.startswith("## "):
            cur = ln.strip()
        elif "DIRECTIVE R" in ln and cur and re.search(r"RECHAZAD|REJECTED", cur, re.I):
            add("ERROR", name, f"a `DIRECTIVE R<N>:` approval record sits under '{cur}'")


# ------------------------------------------------------------ baseline snapshot
def check_baseline(bp, name, carrier_text):
    """Re-count counted section scopes recorded as `§"<section>" — N …`."""
    ledger = read(os.path.join(bp, "LEDGER.md")) or ""
    directive = read(os.path.join(bp, "DIRECTIVE.md")) or ""
    for src in (ledger, directive):
        for fname, sec_name, declared in re.findall(
                r'(?:([\w./-]+\.md)\s*)?§\s*"([^"]+)"\s*[—-]\s*(\d+)', src):
            host = read(os.path.join(bp, fname)) if fname else carrier_text
            if host is None:
                add("ERROR", name, f'baseline-exempt names {fname}, which does not exist')
                continue
            body = section(host, re.escape(sec_name))
            if body is None:
                add("ERROR", name, f'baseline-exempt cites §"{sec_name}" — no such section in '
                                   f'{fname or "the carrier"}')
                continue
            actual = physical_rows(body)
            if actual != int(declared):
                add("ERROR", name, f'baseline-exempt §"{sec_name}" declares {declared} physical rows, '
                                   f"carrier now has {actual} — recount mismatch")


def check_mode(root, bp, name, catalog, approved):
    """Mode reconciliation runs for EVERY blueprint, adopted or not — a foreign source must never
    be silently accepted with another skill's contract."""
    r = reconcile_mode(root, bp, name, catalog)
    lvl = "ERROR" if approved else "WARN"
    if r["foreign_suffix"]:
        add(lvl, name, f"suffix ({r['foreign_suffix']}) is from {foreign_kind(r['foreign_suffix'])} "
                       f"— unclassified here")
    if r["foreign_brief"]:
        add(lvl, name, f"BRIEF declares Mode '{r['foreign_brief']}' — "
                       f"{foreign_kind(r['foreign_brief'])}")
    if r["foreign_index"]:
        add(lvl, name, f"INDEX declares Mode '{r['foreign_index']}' — "
                       f"{foreign_kind(r['foreign_index'])}")
    if r["drift"]:
        add(lvl, name, "mode-drift: sources disagree — "
                       + ", ".join(f"{k}={v}" for k, v in sorted(r["decls"].items())))
    if not r["mode"] and not r["foreign_suffix"]:
        add("WARN", name, "unclassified blueprint: no mode declared by BRIEF, suffix or INDEX")
    return r


# ------------------------------------------- Directive Completeness rollup
def check_rollup(bp, name, directive, catalog, recon):
    if not directive or directive["state"] is None:
        return None
    mode = recon.get("mode") if recon else None
    if mode is None:
        # unclassified: without a mode there is no defined carrier to validate against. The
        # unclassified finding itself is raised by check_mode().
        return None
    carrier = MODE_CARRIER[mode]
    if not os.path.exists(os.path.join(bp, carrier)):
        other = [c for c in CARRIERS if c != carrier and os.path.exists(os.path.join(bp, c))]
        if other:
            add("ERROR", name, f"{mode} mode requires carrier '{carrier}' — found '{other[0]}'")
            return None
        # --- B: the carrier is created mid-pipeline (MODULE Step 7, B4, …). Its absence is a
        # finding only once implementation is under way; before that the blueprint is simply
        # not there yet.
        status = (read(os.path.join(bp, ".blueprint-status")) or "").split(":")[0].strip().upper()
        lvl = "ERROR" if status in {"ACTIVE", "FOCUSED", "STABLE", "CLOSED", "DRIFTED"} else "NOTE"
        add(lvl, name, f"{mode} carrier '{carrier}' not present"
                       + (f" while status={status}" if lvl == "ERROR" else " (created mid-pipeline)"))
        return None
    text = read(os.path.join(bp, carrier))
    body = section(text, r"Directive Completeness")
    if body is None:
        add("ERROR", name, f"{carrier} has no `## Directive Completeness` rollup (check 3b)")
        return text

    # every obligation id that exists anywhere in the carrier, for resolution
    known = set()
    for r in rows(text):
        c = cells(r)
        if c:
            known.update(OBLIGATION_ID.findall(c[0]))

    seen, states = {}, {}
    for r in rows(body):
        c = cells(r)
        m = re.match(r"\*{0,2}(OC-\d+)\*{0,2}$", c[0]) if c else None
        if not m:
            continue
        oc = m.group(1)
        if oc in seen:
            add("ERROR", name, f"rollup has duplicate row for {oc}")
        seen[oc] = c
        if len(c) < 5:
            add("ERROR", name, f"rollup row {oc} has {len(c)} columns, expected >=5")
            continue
        cover, frac, st, assur = c[1], c[2], c[3].strip("*"), c[4].strip("*")
        if st not in STATES:
            add("ERROR", name, f"{oc} state '{st}' outside the closed model {sorted(STATES)}")
        states[oc] = st
        if assur not in ASSURANCE:
            add("ERROR", name, f"{oc} assurance '{assur}' outside {sorted(ASSURANCE)}")
        if not cover:
            add("ERROR", name, f"{oc} has an empty coverage set")
            continue

        # --- re-derive the DENOMINATOR from the coverage set -------------------
        ids = OBLIGATION_ID.findall(cover)
        self_ref = [i for i in ids if i.startswith("OC-")]
        if self_ref:
            add("ERROR", name, f"{oc} coverage set cites outcome criteria {self_ref} as "
                               f"obligations — a criterion cannot prove itself")
        ids = [i for i in ids if not i.startswith("OC-")]
        unresolved = [i for i in ids if i not in known]
        for u in unresolved:
            add("ERROR", name, f"{oc} coverage set cites '{u}' — no such row in {carrier}")
        # free-text obligations (e.g. "smoke e2e en vivo") are COUNTED, never resolved — there is
        # no oracle for prose. Delimiters are `,` `+` `·`; anything else is one segment.
        free = [seg for seg in re.split(r"[,+·]", cover)
                if seg.strip() and not OBLIGATION_ID.search(seg)]
        derived = len(ids) + len(free)
        fm = re.match(r"(\d+)\s*/\s*(\d+)$", frac)
        if not fm:
            add("WARN", name, f"{oc} verified column '{frac}' is not an N/M fraction")
            continue
        v, t = int(fm.group(1)), int(fm.group(2))
        if t != derived:
            add("ERROR", name, f"{oc} declares {t} obligations but its coverage set resolves to "
                               f"{derived} ({len(ids)} ids + {len(free)} free-text)")
        if v > t:
            add("ERROR", name, f"{oc} verified {v} > obligations {t}")
        if st == "MET" and v != t:
            add("ERROR", name, f"{oc} is MET but only {v}/{t} obligations verified")

        # --- attestations: per-OC block, all five identity fields -------------
        if assur in {"ATTESTED", "MIXED"}:
            blk, lines_ = None, body.splitlines()
            for i, ln in enumerate(lines_):
                if re.search(rf"^-\s*\*{{0,2}}{oc}\b", ln.strip()):
                    j = i + 1
                    while j < len(lines_) and not re.match(r"\s*-\s", lines_[j]) and lines_[j].strip():
                        j += 1
                    blk = "\n".join(lines_[i:j])       # the whole block, wrapped lines included
                    break
            if blk is None:
                add("ERROR", name, f"{oc} is {assur} but has no `- {oc} …` attestation line in the rollup")
            else:
                missing = [f for f, pat in (
                    ("actor", r"@\w"),
                    ("date", r"\d{4}-\d{2}-\d{2}"),
                    ("exact result", r"\d+\s*(/|of|de)\s*\d+|\b\d+\s+(passed|ok|green)\b"),
                    ("environment", r"\b(prod|producci|staging|stage|dev|entorno|environment)"),
                    ("identity", r"(SHA|commit|`[0-9a-f]{7,}`)")) if not re.search(pat, blk, re.I)]
                if missing:
                    add("ERROR", name, f"{oc} attestation lacks required field(s): {', '.join(missing)}")

    for oc in directive["ocs"]:
        if oc not in seen:
            add("ERROR", name, f"{oc} declared in DIRECTIVE has no rollup row (check 3b: UNMAPPED)")
    for oc in seen:
        if oc not in directive["ocs"]:
            add("ERROR", name, f"rollup row {oc} is not declared in DIRECTIVE.md")

    if seen:
        add("NOTE", name, "verified counts are self-reported, and free-text obligations are counted "
                          "but never resolved (no oracle for prose) — the validator re-derives the "
                          "denominator only for recognized ids; the rest needs Owner/ROAR review")

    status = (read(os.path.join(bp, ".blueprint-status")) or "").strip().split(":")[0].strip().upper()
    if status in COMPLETE_STATUSES and directive["state"] != "APPROVED":
        add("ERROR", name, f".blueprint-status={status} while DIRECTIVE authority is "
                           f"{directive['state']} — a completion claim cannot rest on absent authority")
    if status in COMPLETE_STATUSES:
        bad = {o: s for o, s in states.items() if s in BLOCKING_STATES}
        if bad:
            add("ERROR", name, f".blueprint-status={status} while {bad} — a completion claim cannot stand")
    return text


# --------------------------------------------- blocker / dependency registers
def check_registers(bp, name, carrier_text, directive):
    # (heading, id pattern, column holding LOCAL OC refs, column holding the state)
    for heading, id_pat, local_col, state_col in (("Blockers", r"BLK-\d+", 1, 5),
                                                  ("Dependencies", r"DEP-\d+", 1, 4)):
        body = section(carrier_text or "", rf"^##+\s+{heading}\b")
        if body is None:
            continue                                   # registers are pilot-scoped, not mandatory
        ids = []
        for r in rows(body):
            c = cells(r)
            if not c or not re.match(id_pat, c[0].strip("*")):
                continue
            ids.append(c[0].strip("*"))
            st = (c[state_col] if len(c) > state_col else c[-1]).strip("*").upper()
            if st not in REGISTER_STATES:
                add("ERROR", name, f"{heading} {c[0]} state '{st}' outside {sorted(REGISTER_STATES)}")
            if directive:
                # only the LOCAL column is validated against this blueprint's OCs; a Target may
                # legitimately name another blueprint's criterion (Other:OC-04)
                local = c[local_col] if len(c) > local_col else ""
                for oc in re.findall(r"(?<![:\w])OC-\d+", local):
                    if oc not in directive["ocs"]:
                        add("ERROR", name, f"{heading} {c[0]} references {oc}, not declared in DIRECTIVE.md")
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            add("ERROR", name, f"{heading} has duplicate ids: {sorted(dup)}")


# ----------------------------------------------------------- execution dotfile
def check_execution(bp, name, directive):
    text = read(os.path.join(bp, ".blueprint-execution"))
    if text is None:
        if directive:
            add("ERROR", name, "adopted blueprint has no `.blueprint-execution`")
        return
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) > 7:
        add("ERROR", name, f".blueprint-execution has {len(lines)} lines (cap 7)")
    if not re.search(r"^-\s*Active:", text, re.M):
        add("ERROR", name, ".blueprint-execution has no `- Active:` line")
    depth = len(re.findall(r"^-\s*Excursion\[(\d+)\]", text, re.M))
    if depth > 3:
        add("ERROR", name, f"excursion depth {depth} exceeds the hard cap of 3 — stop and surface")
    if directive:
        for oc in set(re.findall(r"OC-\d+", text)):
            if oc not in directive["ocs"]:
                add("ERROR", name, f".blueprint-execution cites {oc}, not declared in DIRECTIVE.md")


# ------------------------------------------------------------- status hygiene
def check_status(bp, name, adopted):
    text = read(os.path.join(bp, ".blueprint-status"))
    if text is None:
        add("WARN", name, "no `.blueprint-status` file")
        return
    body = text.strip()
    if body.count("\n"):
        # pre-DIRECTIVE convention → WARN (severity policy); only the *narrative* row has a
        # documented migration trigger and escalates once approved
        add("WARN", name, ".blueprint-status is not a single line")
    words = len(body.split())
    if words > STATUS_WORD_HARD:
        # narrative status migrates AT adoption (migration map); an untouched legacy blueprint is
        # not in violation — it is simply not migrated yet.
        add("ERROR" if adopted else "NOTE", name,
            f".blueprint-status carries {words} words — a status file is a status, not a "
                           "changelog; move narrative to AUDIT/LEDGER and current work to "
                           "`.blueprint-execution`")
    elif words > STATUS_WORD_SOFT and adopted:
        add("WARN", name, f".blueprint-status carries {words} words (soft cap {STATUS_WORD_SOFT})")


# ------------------------------------------------------------- footer targets
def check_footers(bp, name):
    """Footer hygiene is a WORKFLOW CONVENTION that predates the DIRECTIVE mechanism — there is no
    migration trigger for it, so it is never gated on adoption. Severity policy: ERROR is reserved
    for DIRECTIVE-protocol contract violations; pre-existing workflow conventions report WARN so
    they stay visible without blocking a corpus that never opted in."""
    for fn in sorted(os.listdir(bp)):
        if not fn.endswith(".md"):
            continue
        text = read(os.path.join(bp, fn)) or ""
        # the footer is what follows the LAST thematic break — not just the last N lines,
        # which caught opcode notation like `rA:K[B](rA+1, …)` in technical tables
        # rule: the nav footer is the LAST content in the file. Check it directly rather than
        # inferring from thematic breaks — appended history can carry its own `---`.
        lines_ = text.splitlines()
        # LAST occurrence: a nav bar repeated at top and bottom is a legitimate convention
        fidx = next((i for i in range(len(lines_) - 1, -1, -1)
                     if "← Index" in lines_[i] or "Index](" in lines_[i]), None)
        if fidx is None:
            # the workflow requires a nav footer on every artifact; absence was previously
            # invisible because the check only ran when one already existed
            # footer hygiene is a workflow convention enforced from adoption forward; an
            # untouched legacy artifact is not in violation, it is simply not migrated yet
            add("WARN", f"{name}/{fn}", "artifact has no navigation footer")
            continue
        if any(l.strip() for l in lines_[fidx + 1:]):
            add("WARN", f"{name}/{fn}", "navigation footer is not the last content in the file "
                                        "(content appears after it)")
        scope = "\n".join(lines_[fidx:])      # from the footer onward — not a `---`-derived tail,
        for label, target in re.findall(          # which is empty when no thematic break precedes it
                r"\[([^\]]+)\]\(((?:[^()]|\([^()]*\))+)\)", scope):
            target = target.split("#")[0].strip()
            if not target or target.startswith(("http", "mailto:")):
                continue
            if not re.match(r"^[\w./\-() ]+\.\w+$", target):
                continue                                  # not a file path — skip notation
            if not os.path.exists(os.path.normpath(os.path.join(bp, target))):
                add("WARN", f"{name}/{fn}", f"footer link '{label}' → missing target '{target}'")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root, quiet = argv[1], "--quiet" in argv
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    skill, skill_problem = designated_skill(root)
    if skill_problem:
        # without a designated skill the union of catalogs would silently accept a foreign mode
        add("ERROR" if "not a known" in skill_problem else "WARN", "<project>",
            f"{skill_problem} — modes validated against the union of catalogs, so a foreign mode "
            "cannot be detected here")
    catalog = SKILL_MODES.get(skill, MODE_CARRIER)
    bps = sorted(d for d in os.listdir(root)
                 if os.path.isdir(os.path.join(root, d))
                 and os.path.exists(os.path.join(root, d, "BRIEF.md")))
    for d in bps:
        bp = os.path.join(root, d)
        directive = check_directive(bp, d)
        approved = bool(directive and directive.get("state") == "APPROVED")
        recon = check_mode(root, bp, d, catalog, approved)   # must precede carrier resolution
        check_lineage(bp, d, directive)
        carrier_text = check_rollup(bp, d, directive, catalog, recon)
        if carrier_text:
            check_baseline(bp, d, carrier_text)
            check_registers(bp, d, carrier_text, directive)
        check_execution(bp, d, directive)
        check_status(bp, d, approved)
        check_footers(bp, d)

    errs = [f for f in findings if f[0] == "ERROR"]
    for level, path, msg in findings:
        print(f"{level} {path}: {msg}")
    if not quiet:
        adopted = sum(1 for d in bps
                      if re.search(r"^\*\*Authority:\*\*\s*APPROVED",
                                   read(os.path.join(root, d, "DIRECTIVE.md")) or "", re.M))
        print(f"\nskill: {skill or 'undeclared (validating against the union of catalogs)'}")
        print(f"{len(bps)} blueprints ({adopted} approved) · {len(errs)} errors · "
              f"{len(findings) - len(errs)} warnings/notes")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
