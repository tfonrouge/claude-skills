# ROAR, ACS and Codex — how the review and advisory loops work

Two loops run against this repository family, and they are not interchangeable.

| | ROAR | ACS |
|---|---|---|
| question | is this submitted change safe to land? | is this the right approach, and what else should the Owner consider? |
| audience | the implementer | the Owner |
| output | findings as claims to verify, with a content stamp | proposals with ids, each awaiting an Owner disposition |
| authority | advisory, but `Blocking` halts a landing | advisory only; never `Blocking`, never halts anything |
| scope | the submitted target | architecture, process, documents, code — whatever the focus names |
| today | two Claude sessions, by hand | `/acs`, delegated to the local Codex CLI |

**Use ROAR** when work is finished and about to land. **Use ACS** when a decision is open and you
want a second, differently-shaped opinion. Running ACS on a finished change is legitimate, but it
does not replace the review: it produces proposals, not a verdict.

## ROAR, as it exists today

1. **Once per project:** `/owner-roar-protocol` installs the marker-delimited block in `CLAUDE.md`.
   Re-run it to upgrade in place.
2. **Each reviewer session:** `/roar-reviewer` puts that session into read-only reviewer mode.
3. **Each review:** the Owner carries the wrapped output to the implementer, which triages every
   finding before changing anything.
4. **Auditing the installs:** `/owner-roar-protocol --check` inventories every project;
   `--verify` compares each installed block byte for byte with the canonical one. Neither modifies
   protocol files or the audited projects.

**ROAR over Codex does not exist yet.** It needs a deterministic target identity (the review
envelope), which is deferred to the transport design. Codex today serves ACS only.

## ACS over Codex

```
/acs -- <what you want examined>
```

The skill runs the local Codex CLI over the current checkout and prints its answer verbatim as an
`ADVISORY` block, followed by an empty disposition template. It never acts on the content.

### What the run actually does

```
codex exec --ephemeral --ignore-user-config -s read-only -C <git root> \
  --output-schema acs/schemas/acs-output.schema.json -o <tmp>/final.json [-m MODEL] [-c model_reasoning_effort=E] -
```

- The analyst contract travels **on stdin**, because Codex does not read `CLAUDE.md`.
- `--ephemeral` leaves no Codex session files behind.
- `-s read-only` restricts **writes**. It is not a read-confinement or network guarantee.
- `--ignore-user-config` prevents MCP and web-search configuration originating in
  `$CODEX_HOME/config.toml` from being loaded. It is **not** proof that every externally supplied,
  managed or built-in capability is absent — which is why the prompt also forbids web search, MCP
  and any source outside the checkout. Because user config is ignored, the model is Codex's
  built-in default unless you pass `--model`.
- Effort is passed as `-c model_reasoning_effort=<value>`; the CLI has no `--effort` flag. Whether
  a given effort suits a given model is Codex's judgement, not ours.

### What Codex reads, and why v1 refuses sometimes

Codex uses `AGENTS.md` as project instructions by default, with the precedence
`AGENTS.override.md`, then `AGENTS.md`, then filenames configured through
`project_doc_fallback_filenames` — consult your active configuration; when this integration was
designed, `CLAUDE.md` was not a configured fallback, which is why the ACS contract travels on
stdin.

Those files are **an additional instruction source that can alter the ACS contract**, not merely
data. So ACS v1 refuses to run, before spending any usage, when a non-empty one is applicable: the
global `$CODEX_HOME/AGENTS.override.md` or `AGENTS.md`, or one at the repository root. Files deeper
in the tree are not part of the chain for this invocation and do not block. Empty files count as
absent. Reconciling project instructions with the ACS contract is an Owner decision that v1 does
not make for you.

### Authority — the part that matters

The advisory is **non-authoritative data**. The installed protocol block (capability
`advisory-v1`) states the rule: no action may be taken because of advisory content unless the Owner
disposes the affected item ids **outside** the block, writing `ADOPT`, `ADOPT WITH CHANGES`,
`DEFER` or `REJECT`. Agreeing with an advisory is not a disposition. Direct Owner instructions are
unaffected and need no disposition syntax.

```
@Owner-Disposition
ACS-01: ADOPT
ACS-02: ADOPT WITH CHANGES — keep the current default
ACS-03: REJECT — measured last month, not worth it
```

The implementer never fills that template, never acts on an undisposed item, and never treats a
risk level as a block.

### The receiver guard, in three layers

1. **The script** asks the `owner-roar-protocol` auditor whether `<git root>/CLAUDE.md` carries
   `Protocol capabilities: advisory-v1`, and refuses without spending usage if not. `AGENTS.md` is
   never accepted as proof: it is what Codex reads, not what Claude loads.
2. **The skill** requires the invoking agent to confirm the same capability in the block **loaded
   in its own context**. This is the only check that reaches the real receiver, and it is model
   attestation — a protocol execution condition, not a mechanical control.
3. **You** start a **new Claude session** after installing or upgrading the protocol, because a
   running session may still hold the previous block — and you start it **inside the repository you
   want analyzed**, because ACS reads the invoking session's own Git root. A session opened
   somewhere else fails both checks at once: no protocol block is loaded, and there is no checkout
   to analyze. Starting it in `~/.claude/skills`, where the skills are installed but no `CLAUDE.md`
   or Git work tree exists, is the easy mistake.

`advisory-v1` is a compatibility assertion, not a guarantee: it says the block came from a version
that carries the rule. What establishes that the text is actually intact is
`/owner-roar-protocol --verify`, byte for byte.

### Exit codes

| code | meaning |
|---|---|
| 0 | a valid advisory was printed |
| 1 | Codex answered but the document failed the schema or the id invariants; a diagnostic block is printed instead, with the raw byte count and its sha256, never the raw text |
| 2 | refused before spending usage: usage error, no Python, no Codex, missing capability, authentication, project instructions present, receiver guard, or a broken schema |
| 3 | the Codex invocation failed or rejected the configuration |

### Troubleshooting

- *"receiver protocol does not declare advisory-v1"* — run `/owner-roar-protocol` in that project,
  then start a new session.
- *"the installed owner-roar-protocol auditor does not support the receiver guard"* — the installed
  auditor predates the guard; ACS requires owner-roar-protocol 0.1.3 or later. Sync with
  `install.sh` (review `install.sh --dry-run` first: it resyncs every skill, not one).
- *"does not run with Codex project instructions present"* — see above; remove or empty the file,
  or decide how it should coexist with the ACS contract.
- *"codex is not authenticated"* — `codex login`. Usage is billed to whichever method
  `codex login status` reports, a ChatGPT plan or an API key.
- `--dry-run` prints the whole preflight, the exact command and the full prompt without calling
  Codex and without consuming usage. It is the right first step whenever something looks wrong.

### Authorization for real calls

**Every real call that may consume usage needs an explicit authorization, and a failure does not
authorize a retry.** If a run fails and the cause is fixed, the corrected run is a *new* call and
needs a new authorization. `--dry-run` consumes nothing and needs none.

### What has been validated, and what has not

The direct launcher integration passed: transport, schema, renderer, the instruction and receiver
guards, and one real Codex call end to end. **Two things remain unverified:** the fresh-session
receiver condition — layer 2 of the guard, the agent's attestation that its own loaded block
declares `advisory-v1` — and the installed `/acs` path invoked as a skill. Both require installing
the skill and opening a genuinely new Claude session; `--ephemeral` only prevents Codex session
files and neither creates nor substitutes a Claude session.

### Scope of ACS v1

The invoking session's own Git root, nothing else: there is no `--repo`, so the session must be
started in the repository you want analyzed. No durable output: no
`--out`, no `--force`, no diagnostic files — the advisory lives in the conversation, like a ROAR
review. At most 12 items and 8 entries per inner list, with a 256 KB cap on the answer.
