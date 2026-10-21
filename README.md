# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Pet and task management:** Add pets, then add care tasks to a specific pet. Each task has a description, duration, priority (`low`, `medium`, `high`), start time, frequency, and due date.
- **Input validation:** A task is rejected if its duration is zero or less, its priority or frequency is unknown, or its time is not in 24-hour `HH:MM` format. The app also blocks blank names and duplicate pet names.
- **Priority-based daily plan:** `Scheduler.generate_plan()` orders pending tasks by priority (high first), breaking ties by shorter duration. It then adds each task that still fits in the owner's available minutes. A task that doesn't fit is skipped, but smaller tasks after it can still be added.
- **Plan explanation:** `Scheduler.explain_plan()` names each skipped task and says it was skipped for lack of time, or confirms that all pending tasks fit.
- **Sorting by start time:** `Scheduler.sort_by_time()` lists tasks from earliest to latest. The app uses it to show the schedule in time order.
- **Filtering:** `Scheduler.filter_tasks()` finds tasks by pet name (not case-sensitive), by completion status, or both. This is available in the backend and shown in `main.py`; the app does not have filter controls yet.
- **Conflict warnings:** `Scheduler.detect_conflicts()` finds tasks whose time ranges overlap, including tasks for different pets, since one owner does them all. Back-to-back tasks are allowed. The app shows each conflict as a yellow warning.
- **Recurring tasks:** `Pet.complete_task()` marks a task done and creates its next occurrence: 1 day later for `daily` tasks, 7 days later for `weekly` tasks, and none for `as_needed` tasks. Completing the same task twice does not create a duplicate. This is implemented and tested in the backend, but it is not yet available in the app or `main.py`.

### Current Limitations

- In the app, the owner's available time is fixed at 60 minutes, and new tasks always use the `daily` frequency with today's due date.
- The scheduler does not check due dates, so a future recurring task would be planned along with today's tasks.
- Owner preferences and pet special needs are stored but not yet used by the scheduler.
- The app cannot edit, remove, or complete tasks. Pets and tasks last only while the browser session is open.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 📐 Smarter Scheduling

PawPal+ includes additional scheduling features to help pet owners organize care tasks more effectively.

### Sorting Tasks

The `Scheduler.sort_by_time()` method sorts tasks by their scheduled start time, from earliest to latest. This makes it easier to view a daily care schedule in chronological order.

### Filtering Tasks

The `Scheduler.filter_tasks()` method filters tasks using optional criteria:
- **Pet name:** Shows tasks belonging to a specific pet. Pet names are matched without distinguishing uppercase and lowercase letters.
- **Completion status:** Shows completed tasks or pending tasks.
- Both filters can be used together.

### Conflict Detection

The `Scheduler.detect_conflicts()` method checks whether scheduled tasks overlap based on their start times and durations. It returns warning messages describing conflicting tasks rather than stopping the program with an error. Tasks scheduled back-to-back are allowed.

The method sorts tasks by start time and stops checking later tasks when they can no longer overlap with the current task.

### Recurring Tasks

The `Pet.complete_task()` method marks a task as completed and creates its next occurrence when the task has a daily or weekly frequency. Daily tasks are scheduled one day after their due date, and weekly tasks are scheduled seven days after their due date. Tasks marked `as_needed` do not automatically repeat.

### Task Time and Date

Each `Task` has a scheduled time and a due date. The `Task.get_start_minutes()` method converts the scheduled time into minutes since midnight to support time-based calculations.

The task time is stored in `HH:MM` format using a 24-hour clock.

## Demo Walkthrough

### Running the App

```bash
streamlit run app.py
```

### What You Can Do in the App

- **Quick Demo Inputs:** Set the owner's name and add pets (name and species). Duplicate pet names are rejected.
- **Add a Care Task:** Choose a pet, then enter a task title, duration, priority, and start time. New tasks appear in the **Current Tasks** table.
- **Build Schedule:** Click **Generate schedule** to see today's plan as a table sorted by start time, followed by conflict warnings and schedule notes.

### Example Workflow

1. Add a cat named **Mochi** and a dog named **Buddy**. Both appear under **Your Pets**.
2. Add these tasks. Each one appears in **Current Tasks** after you click **Add task**:

   | Pet   | Task           | Duration | Priority | Start |
   |-------|----------------|----------|----------|-------|
   | Mochi | Feed breakfast | 10 min   | high     | 08:00 |
   | Buddy | Morning walk   | 30 min   | high     | 08:00 |
   | Buddy | Grooming       | 30 min   | low      | 10:00 |

3. Click **Generate schedule**. The app shows:
   - **Today's Schedule:** Feed breakfast (Mochi) at 08:00 and Morning walk (Buddy) at 08:00.
   - **Schedule Conflict Warnings:** "Feed breakfast (Mochi) overlaps Morning walk (Buddy). Please review the start times and reschedule a task if necessary."
   - **Schedule Notes:** "Grooming for Buddy was skipped because there was not enough time."

### How the Scheduler Shapes These Results

- **Choosing tasks (priority):** The three tasks need 70 minutes, but only 60 are available. The two high-priority tasks are added first (40 minutes). Grooming needs 30 more minutes, but only 20 remain, so it is skipped.
- **Ordering the table (time):** The chosen tasks are displayed by start time. Tasks with the same start time keep their priority order.
- **Finding conflicts (overlap):** Feed breakfast runs 08:00–08:10 and Morning walk runs 08:00–08:30. Their times overlap, so a warning appears even though they belong to different pets.

### Command-Line Demo

Run `main.py` from the project root, with the virtual environment activated:

```bash
python main.py
```

It creates an owner with 60 minutes, two pets, and three tasks, then demonstrates planning, sorting, filtering, and conflict detection. Sample output:

```text
Today's Schedule
================
Daily care plan for Alex:
- Feed breakfast (Mochi) - 10 minutes [high]
- Morning walk (Buddy) - 30 minutes [high]
- Grooming (Buddy) - 20 minutes [low]

Schedule Notes
==============
All pending tasks fit into the available time.

Tasks Sorted by Time
====================
08:30 - Morning walk (Buddy)
08:30 - Feed breakfast (Mochi)
10:00 - Grooming (Buddy)

Tasks for Buddy
===============
08:30 - Morning walk
10:00 - Grooming

Pending Tasks
=============
08:30 - Morning walk (Buddy)
10:00 - Grooming (Buddy)
08:30 - Feed breakfast (Mochi)

Task Conflict Warnings
======================
WARNING: Morning walk (Buddy) overlaps Feed breakfast (Mochi).
```

Notice that **Feed breakfast** comes before **Morning walk** in the plan. Both are high priority, so the shorter task goes first. In the time-sorted list, both start at 08:30, so they keep their original order. Because they start at the same time, they are reported as a conflict.

## Testing PawPal+

Run the automated test suite from the project root directory using:

```bash
python -m pytest
```

### What the Tests Cover

The automated tests verify the correctness and reliability of PawPal+ features, including:

- **Task sorting:** Checks that tasks are returned in chronological order, including edge cases such as equal times and empty lists.
- **Task filtering:** Tests filtering by pet name, completion status, and combinations of filters.
- **Recurring tasks:** Verifies that completing daily or weekly tasks creates the next occurrence with the correct date and task details.
- **Conflict detection:** Checks whether overlapping tasks are identified and back-to-back tasks are handled correctly.
- **Schedule generation:** Tests tasks that fit within the owner's available time, tasks that must be skipped, and cases with no available time.
- **Validation and edge cases:** Tests invalid task ownership, duplicate pet details, and prevents duplicate recurring tasks when a task is completed more than once.

### Successful Test Run

The latest test run completed with **33 tests passed**.

```text
==================================== test session starts =====================================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\Kenny\OneDrive\Documents\Codepath\Pawpa\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 33 items

tests\test_pawpal.py .................................                                  [100%]

===================================== 33 passed in 0.13s =====================================
```

### Confidence Level

**Confidence Level: 4/5 stars (★★★★☆)**

The test suite covers the core scheduling features and a variety of edge cases. All 33 tests passed in the latest run, increasing confidence in the system's reliability. However, passing tests cannot guarantee that every possible bug has been found, so additional testing may still be beneficial.
