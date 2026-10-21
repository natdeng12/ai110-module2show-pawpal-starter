# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

For Challenge 1, I asked Claude Code (in VS Code) to add a **next available time slot** feature. My instructions were to inspect the existing `Scheduler`, `Task`, and conflict-detection code first, plan a minimal design that reuses that code, implement a `Scheduler` method that finds the earliest time a task of a given length fits without overlapping existing tasks (returning a clear result when nothing fits), add tests for a normal slot, an overlap, and no available slot, run `python -m pytest`, and avoid unrelated refactoring.

**Files modified**

- `pawpal_system.py`: added `Scheduler.find_next_available_slot()`.
- `tests/test_pawpal.py`: added 7 tests for the new method.
- `ai_interactions.md`: this section.

**What did the agent do?**

1. Read `pawpal_system.py` and reviewed `Task.get_start_minutes()`, `Scheduler.sort_by_time()`, and `Scheduler.detect_conflicts()`.
2. Chose a design that reuses them:
   - Tasks are passed in as `(pet, task)` pairs, the same way as `detect_conflicts()`.
   - The search starts at a given `start_time` (default `"00:00"`).
   - Back-to-back tasks are allowed, matching `detect_conflicts()`.
   - The new task must end by midnight (24:00).
   - `None` is returned when no gap is long enough.
   - An invalid duration or start time raises `ValueError`, reusing `Task`'s existing validation.
3. Added `Scheduler.find_next_available_slot()` to `pawpal_system.py`. No existing methods were changed.
4. Added 7 tests to `tests/test_pawpal.py`:
   - an empty schedule
   - using a gap between tasks
   - skipping several overlapping tasks and a gap that is too short
   - a start time inside an existing task
   - no slot left before midnight
   - a slot ending exactly at midnight
   - an invalid duration
5. Ran the test suite with the project's virtual environment: **40 passed**.

**What did you have to verify or fix manually?**

<!-- TODO: Describe what you reviewed, tested, or changed yourself (for example, rerunning the tests or trying the method in main.py). -->

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
