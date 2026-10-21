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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:


## Sample Output

Running `python main.py` produces the following output:

```text
Today's Schedule
================
Daily care plan for Alex:
- Morning walk (Buddy) - 30 minutes [high]
- Feed breakfast (Mochi) - 10 minutes [high]
- Grooming (Buddy) - 20 minutes [low]

Schedule Notes
==============
All pending tasks fit into the available time.
```


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

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

Paste the complete terminal output from your successful `python -m pytest` run here:

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
