---
name: clx-concise-report
description: >
  Token-efficient task reporting discipline — outcome first, core + reason + evidence only,
  hard length ceilings. Load for NON-TRIVIAL or multi-part reports (완료 보고, 결과 보고, 요약)
  or when report length/shape needs discipline; the always-on report rule already carries the
  default one-line report. Expand only when the user asks for detail (자세히).
---

# Concise Report

> Outcome first. Core + reason + evidence. Nothing else.

## Structure (in order)

1. **Outcome line** — what happened / what was found, verdict first, one sentence.
2. **Core items** — only changes/findings that alter what the reader does next
   (≤5 bullets; a table only when 3+ items are genuinely comparable).
3. **Reason** — one line each, ONLY where a decision was non-obvious. Obvious choices
   get no justification paragraph.
4. **Evidence** — verification as numbers: `tests 12/12`, `70→61 lines`, `0 fail/0 warn`,
   `file:line`. Claims without numbers are narration, not evidence.

## Hard length ceilings (unsolicited reports)

| Task size | Ceiling |
|-----------|---------|
| Trivial (one file, obvious change) | 1–3 lines |
| Standard | ≤10 lines |
| Large / multi-part | ≤20 lines, then offer "자세히 원하시면 전개합니다" |

The ceiling caps unsolicited length only — when the user asks 자세히/detail/why,
expand freely.

## Rules

- **Numbers over adjectives**: "1.7G→19M", never "much smaller". Deltas (before→after)
  over descriptions; `file:line` pointers instead of re-explaining content.
- **Omit entirely**: restating the request, tool-by-tool process narration ("~를 실행했고
  그 다음~"), hedging, self-praise, decorative headers on short reports, unsolicited
  next-step lists (offer next steps only when blocked or asked).
- **Intuitive first read**: the user must get the whole picture from the first 3 lines;
  everything after is support, not new surprises.
- **Required content survives compression**: goal/loop Cycle-report sections and the
  intent-fidelity `spec → delivered → evidence` check remain — in this compact form,
  not as prose essays.
- **Failures are never compressed away**: errors, skipped items, and unverified claims
  are reported plainly even if they break the ceiling.
- Report language follows the user's chat language (Korean here); identifiers stay as-is.

## Interim reporting (long runs, loops, goal mode)

Silence during a long run is a user-perspective bug; narration is too. The middle ground:

- During any run spanning multiple phases (roughly >10 tool calls or >3 minutes), post
  **one line per completed phase**: `▸ <phase>: <core result with a number>`.
  Example: `▸ 테스트: 3스위트 전부 [100%], 결함 0` — nothing more.
- Loop/goal iterations: milestone lines at phase boundaries INSIDE the iteration, plus the
  normal end-of-iteration report. Codex goal mode follows the same rule (see `work/goals`).
- DO NOT: narrate tool-by-tool; post a milestone for trivial steps; exceed one line per
  milestone; let a phase complete silently in a run the user is waiting on.

## Anti-pattern → fix

```
BAD : "먼저 설정 파일을 읽고, 훅을 등록한 뒤, 테스트를 진행했습니다. 테스트는
       성공적으로 완료되었으며, 전반적으로 훨씬 안정적인 구조가 되었습니다."
GOOD: "훅 등록 완료 — 테스트 3/3 통과 (settings.json:47, 발화 확인). 남은 리스크 없음."
```
