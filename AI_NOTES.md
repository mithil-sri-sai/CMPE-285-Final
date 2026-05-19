# AI_NOTES.md — AI Usage Reflection

## How I used AI overall

I treated the AI as a **pair-programming assistant**, not a substitute for reading code or making decisions. I chose the theme (adoptable pets), sketched the screens, picked Flask + SQLite, and verified every requirement myself on a real device. The AI helped most with **boilerplate, first drafts, and speeding up repetitive work**. I reviewed, changed, and often replaced its output before it went into the submission.

---

## What I designed and built myself

- **Product scope:** 100-item swipe deck, yes/no voting, global results, sign-in, analytics — mapped to Section 3.1 and stretch goals before coding.
- **Architecture:** Flask API + `pets.json` seed + single-page frontend; `sessionStorage` for session ID; server as source of truth for votes.
- **Idempotency strategy:** `UNIQUE(session_id, item_id)` with update-on-duplicate so users can change a vote and undo works correctly — I specified this after rejecting a silent-ignore approach.
- **Stack pivot:** Dropped Node/`better-sqlite3` when native build failed locally; moved to Python/`sqlite3` — my call, AI helped rewrite handlers afterward.
- **UX polish I added:** Image load fade-in (`.loading` / `.loaded`), pointer-based swipe with horizontal vs vertical gesture split, swipe-down for results, undo stack, matches tab, 15s results polling, per-sign-in fresh deck with global aggregates.
- **Data & images:** Ran `seed.py`, fixed broken Unsplash URLs, switched pets 80–100 to reliable cat images on placecats.com.
- **Testing:** Ran the app end-to-end (swipe, buttons, results tabs, sign-in, stats, reload) and fixed what failed in practice.

---

## Where AI helped (first drafts / snippets only)

| Area | AI role | What I did after |
|------|---------|------------------|
| `server.py` | Drafted route stubs and SQL shape | Rewrote validation, auth, analytics, `DELETE /vote`, serving frontend at `/` |
| `seed.py` | Loop/template for 100 pets | Adjusted breeds, image URL strategy, regenerated `pets.json` |
| `index.html` | Starting layout + swipe math idea | Tuned thresholds, pointer events, all overlays, sign-in/analytics UI |
| Results CSS | Basic list layout | Asked for bars, %, sort tabs, empty states; wired all five tabs myself |
| README | Structure and checklist | Edited trade-offs, stretch list, run steps to match final app |

I did **not** paste a full AI dump and submit it. Every file in the repo was read and run locally.

---

## One concrete pushback (required reflection)

**Idempotency on `/vote`:** The AI’s first version used `try/except` on `INSERT` and silently ignored duplicate votes. I realized that would block vote changes (yes → no) and break undo semantics. I changed it to insert-or-update on `IntegrityError` so one row per user per pet can be updated — aligned with undo and fair re-voting.

---

## One thing AI did better than I expected

Rough swipe math (delta → translate + rotate + hint opacity) came back usable in one pass. I still tested on desktop and mobile and adjusted the down-swipe vs left/right discrimination myself, but it saved time on the fiddly pointer math.

---

## One thing AI did worse than I expected

The initial results view was purely a list with no visual hierarchy but just pet names and raw counts. I had to explicitly ask for a percentage bar and colour-coded yes percentage, and specify that the rank number, breed, and divisiveness sort should all be separate fields.

---

## Other AI tools

No other AI tools were used alongside Claude for this submission.
