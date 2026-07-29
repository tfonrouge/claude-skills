---
name: owner-loop-goal
metadata:
  version: 0.1.0
description: >
  MANUAL INVOCATION, PER TASK — only when the Owner explicitly requests it
  (e.g. "owner-loop-goal: <objective>  DoD: <verifiable criteria>"). Do NOT auto-activate:
  most tasks are NOT looped.

  IMPLEMENTER working mode for LONG self-verified cycles toward a goal. REQUIRES a specific,
  falsifiable GOAL with a measurable DoD — if it is missing or vague, the skill DEMANDS defining
  it before starting (the name says it: no GOAL, no loop). Each iteration the implementer runs
  its own adversarial review (anti-error checklist) before advancing. The loop runs WITHOUT
  external review; the review handoff (ROAR/Owner) happens ONCE, at loop END, whether or not
  the GOAL was reached. Never a silent "shipped".
---

# owner-loop-goal — long self-verified cycle toward a goal

Working mode for **lengthening implementation cycles** without growing the batch of errors. It
raises the quality floor *before* the handoff by internalizing the adversarial review an external
reviewer would otherwise perform, so that final review operates at the level of **design and
completeness**, not script typos or over-claiming.

> **This mode COMPLEMENTS external review — it does not replace it.** Self-review shares the
> author's blind spots; it catches the shallow (bugs, unsourced figures, over-generalization),
> not the structural (design gaps, blind spots). The final gate remains external — see §6.

---

## 0. ENTRY GATE — no falsifiable GOAL, no start

**First thing, always.** Before touching anything:

1. **Extract the GOAL and its DoD** from the invocation. The DoD must be a set of
   **verifiable/falsifiable** exit criteria, not an intention.
2. **If the DoD is missing or vague → STOP and negotiate it with the Owner.** Do not invent one.
   Do not start "to see how far I get".

| VALID DoD (measurable) | INVALID DoD (subjective) |
|------------------------|--------------------------|
| "the 83 candidates cross-checked against write-site/R-sem; census re-run clean; negative controls green" | "get F0-04 into good shape" |
| "each of the 34 tables classified attribution/FK/authorization with call-site" | "make progress on F0-05" |
| "plan with the 5 corrections from L-006 applied, ordered by dependency" | "write the migration plan" |

3. **State the GOAL and DoD in writing** to the Owner in one line before entering the loop, so
   that "done" is judged against agreed criteria, not against my judgment. **If the gate passed
   (specific + falsifiable), state it and proceed — do not wait for an acknowledgment.** Stop
   only when the gate fails.

---

## 1. The loop (no external review inside)

Repeat until termination (§5). **During the loop the ROAR is NOT invoked** — only the §2
self-review.

```
iterate:
  a. DECLARE     — record in the LOG which DoD criteria this iteration targets, before advancing
  b. ADVANCE     — implement the next coherent, finished unit toward those criteria
  c. SELF-REVIEW — run the §2 checklist on what was just produced
  d. if a check FAILS → fix and re-check (a fix cycle stays inside the same iteration);
                  never advance with an open failure
  e. record the result in the auto-review LOG (§4)
```

**An iteration = one DECLARE→LOG pass.** The §3 cap counts declared iterations; fix cycles do not
consume extra iterations. Inflating one iteration to swallow the whole GOAL is visible in the LOG
(a single iteration claiming most of the DoD is itself a flag for the final reviewer).

Work in **coherent, finished units**, not in edits that step on each other. The loop may span
many tool batches within the turn.

---

## 2. Adversarial self-review checklist (the gate of every iteration)

An abstraction of real failure modes. Each iteration, over what was just produced — **every
question hunts for the FAILURE, not the confirmation**:

| # | Check | The falsifiable question |
|---|-------|--------------------------|
| 1 | **Over-reach** | Any "all / uniform / closed / none / always" **extrapolated** from a sample? → degrade to what was proven, or prove it. |
| 2 | **Full data** | If there is a script/count: did it run over the **complete** population, not a truncated sample? Does it emit a snapshot hash/identity + the exact command? Does it run clean *now*? |
| 3 | **Falsifiable verification** | **Can my verification query fail?** Never verify with a query built to pass (e.g. grepping a phrase I wrote myself). Hunt the **counterexample**. |
| 4 | **Cross-check vs. prior data** | Does my claim/proposal **contradict data I already gathered** in this same work? (the trap where the counterexample was already in the table). |
| 5 | **Negative control** | Do my filters/guards **fire** on known-bad inputs? A filter that never rejects anything is untested. |
| 6 | **Citation & unit** | Does every figure carry its source? Is the unit right (cells ≠ rows; physical column ≠ concept; name ≠ identity)? |
| 7 | **DoD** | Does the delivered work satisfy **each** DoD criterion, line by line? Mark what does not yet. |

A failure on 1–6 **blocks advancing** until fixed. Item 7 governs termination.

> **When the loop's output is a test or harness**, the Owner/ROAR protocol's named axes —
> behavior, negative path, cleanup/ownership, concurrency, process correlation, claim-to-oracle
> alignment — join this checklist for those iterations. They are not deferred to the handoff.

---

## 3. Hard-stop rule — prefer STOPPING over guessing

- If I **cannot verify** something the DoD requires → **stop and surface it** to the Owner. Never
  assert the unverified; write "not verified — blocked on X".
- If an **Owner decision** appears (trade-off, scope, priority), distinguish two cases:
  - **Point decision** — small, does not invalidate the GOAL/DoD (a naming choice, a local
    trade-off): surface the question, **park** the criteria that depend on it, and continue on
    independent DoD criteria; **resume** the parked work when answered. If no independent
    criteria remain, the loop **suspends** until the answer — it does not terminate.
  - **GOAL-invalidating** — the answer could change the GOAL or the DoD themselves: stop → §6.
- **Hard cap — maximum iterations.** Default: **6 iterations** (the Owner may set another value
  in the invocation). On reaching it, **stop** with partial state + LOG and go to the handoff
  (§6). **Reaching the cap is a SIGNAL, not a mechanical failure:** it may indicate the GOAL is
  **unreachable or impractical** and needs **joint re-examination with the Owner** — surface it
  that way, not as "I ran out of iterations" but as "the GOAL may need revisiting".

---

## 4. Auto-review LOG (so the final review attacks what I did NOT check)

Keep the working LOG **in a scratchpad file during the loop** — never in a repo file (findings
and triage stay out of durable artifacts) — so it survives long sessions and context
summarization. Deliver its contents in chat at the handoff.

Per iteration: the **declared target criteria**, **which checks ran and their results**, and
**what stayed out of scope / unverified**. The external reviewer uses it to know what to trust
and **where to look** — the self-review declares its limits, it does not hide them.

**Close the LOG with a content stamp** of the final state — commit hash, plus worktree
object-hash and/or untracked blob-hashes per the Owner/ROAR stamp rules — so the final review
has byte-identity for what it reviews.

```
Auto-review log — <GOAL>
- iter N: targets: <DoD criteria> · [1 ok][2 ok, census full-scan sha=…][3 ok, falsifiable query][4 ok][5 ok][6 ok][7 3/5 DoD]
  out of scope: <what was NOT cross-checked / NOT verified>
Final state: <commit-hash>[ + worktree <object-hash>][ + untracked <path>@<blob-hash> …]
```

---

## 5. Termination

The loop ends at the first of:

- **DoD complete** (§2 #7 at 100%) with a clean §2 checklist.
- **Blocked** (§3: unverifiable DoD requirement, or a GOAL-invalidating decision) — surface and stop.
- **Iteration cap reached** (§3) — stop with partial state + the GOAL-re-examination signal.

In **all three cases** proceed to the §6 handoff. The loop never "ships" or closes on its own.

---

## 6. Handoff — at loop END, ALWAYS, whether or not the GOAL was reached

When the loop ends (any of §5's three paths), **deliver to external review (ROAR/Owner)** the
result + the auto-review LOG — **once, at the end**, whether the GOAL was met, the loop was
blocked, or the cap was hit.

- **No external review during the loop** — that is the mode's premise (long cycles; the ROAR
  reviews the complete unit at once, not fragments).
- **The handoff is a submission for review: the Owner/ROAR implementer preflight applies in
  full.** Run it before submitting.
- **`owner-loop-goal` never closes on its own.** The final handoff is mandatory even with an
  apparently mechanical DoD; the Owner decides whether the result needs ROAR or the LOG suffices.
- Respect the repo's flows (blueprint/spec/commit); no commit/push unless the DoD or the Owner
  says so. **The Owner MAY grant per-iteration WIP commits on a work branch in the invocation**
  (protects long loops against work loss); the default is no commits.
- **The mode ENDS with the handoff.** Subsequent work returns to the normal working/review
  cadence; each invocation is a per-task instance with its own GOAL/DoD, never a standing
  session mode — only a new explicit Owner invocation opens another loop.

---

## Relation to the Owner/ROAR protocol

- **Requires `owner-roar-protocol` v5+ installed.** This skill references three concepts introduced
  in v5: the **named test axes** (§2 — behavior, negative path, cleanup/ownership, concurrency,
  process correlation, claim-to-oracle alignment), the **content-identifying stamp / object-hash**
  stamp rules (§4), and the **implementer preflight** (§6). On a project still on v4, those
  references dangle — install/upgrade the protocol to v5+ before relying on this mode.
- The Owner/ROAR protocol governs **message authority** (Owner directive vs. ROAR
  finding-to-verify) and the triage circuit breaker. `owner-loop-goal` is an **implementer
  working mode**, orthogonal to it — which is why it lives as a skill, not inside that protocol.
- The ROAR enters **at the end** of the loop (§6); its block is processed with the protocol's
  normal triage, and its Confirmed findings open — if the Owner so directs — a **new**
  `owner-loop-goal` (with its own GOAL/DoD), not a mid-loop review of the previous one.
