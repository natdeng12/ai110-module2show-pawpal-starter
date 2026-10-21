
from pawpal_system import Pet, Task, Scheduler, Owner
from datetime import date

def test_task_completion():
    task = Task("Feed breakfast", 10, "high")

    task.mark_complete()

    assert task.is_completed is True


def test_pet_add_task():
    pet = Pet("Buddy", "dog", 3)
    task = Task("Morning walk", 30, "high")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task

import pytest
from pawpal_system import Task


def test_task_accepts_valid_time():
    task = Task("Feed breakfast", 10, time="09:15")
    assert task.time == "09:15"


def test_task_rejects_invalid_time():
    with pytest.raises(ValueError):
        Task("Feed breakfast", 10, time="9am")
        

def test_sort_by_time():
    owner = Owner("Alex", 60)
    pet = Pet("Buddy", "dog", 3)

    late_task = Task("Grooming", 20, time="18:00")
    early_task = Task("Feeding", 10, time="07:30")
    middle_task = Task("Walking", 30, time="08:00")

    tasks = [
        (pet, late_task),
        (pet, early_task),
        (pet, middle_task),
    ]

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.time for pet, task in sorted_tasks] == [
        "07:30",
        "08:00",
        "18:00",
    ]
    
def test_filter_tasks_by_pet():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)
    mochi = Pet("Mochi", "cat", 2)
    owner.add_pet(buddy)
    owner.add_pet(mochi)

    owner.add_task(buddy, Task("Walk", 20))
    owner.add_task(mochi, Task("Feed", 10))

    scheduler = Scheduler(owner)
    result = scheduler.filter_tasks(pet_name="mochi")

    assert len(result) == 1
    assert result[0][0].name == "Mochi"


def test_filter_tasks_by_completion():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)
    owner.add_pet(buddy)

    finished = Task("Feed", 10)
    unfinished = Task("Walk", 20)
    finished.mark_complete()

    owner.add_task(buddy, finished)
    owner.add_task(buddy, unfinished)

    scheduler = Scheduler(owner)
    result = scheduler.filter_tasks(completed=True)

    assert len(result) == 1
    assert result[0][1].description == "Feed"
    
def test_detect_conflicts_finds_overlap():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)
    mochi = Pet("Mochi", "cat", 2)

    walk = Task("Walk", 30, time="08:00")
    feed = Task("Feed", 10, time="08:15")

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts([
        (buddy, walk),
        (mochi, feed),
    ])

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0]
    assert "Feed" in conflicts[0]


def test_detect_conflicts_allows_back_to_back_tasks():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)

    walk = Task("Walk", 30, time="08:00")
    feed = Task("Feed", 10, time="08:30")

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts([
        (buddy, walk),
        (buddy, feed),
    ])

    assert conflicts == []
    
def test_complete_daily_task_creates_next_occurrence():
    pet = Pet("Buddy", "dog", 3)
    task = Task(
        "Feed breakfast",
        10,
        frequency="daily",
        due_date=date(2026, 10, 20),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.is_completed is True
    assert len(pet.tasks) == 2
    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 21)
    assert next_task.is_completed is False


def test_complete_as_needed_task_does_not_repeat():
    pet = Pet("Buddy", "dog", 3)
    task = Task("Give medicine", 5, frequency="as_needed")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.is_completed is True
    assert len(pet.tasks) == 1
    assert next_task is None
    

def test_complete_task_rejects_separate_lookalike_task():
    buddy = Pet("Buddy", "dog", 3)
    saved_task = Task(
        "Feed",
        10,
        due_date=date.today(),
    )
    buddy.add_task(saved_task)

    # This is a separate object with the same details.
    lookalike_task = Task(
        "Feed",
        10,
        due_date=date.today(),
    )

    with pytest.raises(ValueError):
        buddy.complete_task(lookalike_task)

    # The original task must remain unchanged.
    assert saved_task.is_completed is False
    assert len(buddy.get_tasks()) == 1


def test_owner_can_add_two_identical_pets():
    owner = Owner("Alex", 60)

    buddy_one = Pet("Buddy", "dog", 3)
    buddy_two = Pet("Buddy", "dog", 3)

    owner.add_pet(buddy_one)
    owner.add_pet(buddy_two)

    assert len(owner.get_pets()) == 2



def test_generate_plan_includes_all_tasks_that_fit():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)

    low_task = Task("Grooming", 20, priority="low")
    high_task = Task("Walk", 30, priority="high")
    medium_task = Task("Feeding", 10, priority="medium")

    buddy.add_task(low_task)
    buddy.add_task(high_task)
    buddy.add_task(medium_task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert len(plan) == 3
    assert [task.priority for pet, task in plan] == [
        "high",
        "medium",
        "low",
    ]
    assert scheduler.skipped_tasks == []



def test_generate_plan_skips_tasks_that_do_not_fit():
    owner = Owner("Alex", 25)
    buddy = Pet("Buddy", "dog", 3)

    high_task = Task("Long walk", 30, priority="high")
    medium_task = Task("Feeding", 10, priority="medium")

    buddy.add_task(high_task)
    buddy.add_task(medium_task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert len(plan) == 1
    assert plan[0][1].description == "Feeding"
    assert scheduler.skipped_tasks == [(buddy, high_task)]



def test_generate_plan_includes_task_that_exactly_fits():
    owner = Owner("Alex", 30)
    buddy = Pet("Buddy", "dog", 3)

    walk_task = Task("Walk", 30, priority="high")
    buddy.add_task(walk_task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert len(plan) == 1
    assert plan[0] == (buddy, walk_task)
    assert scheduler.skipped_tasks == []


def test_generate_plan_skips_large_task_but_schedules_smaller_tasks():
    owner = Owner("Alex", 25)
    buddy = Pet("Buddy", "dog", 3)

    walk_task = Task("Long walk", 30, priority="high")
    grooming_task = Task("Grooming", 15, priority="medium")
    feeding_task = Task("Feeding", 10, priority="low")

    buddy.add_task(walk_task)
    buddy.add_task(grooming_task)
    buddy.add_task(feeding_task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert [task.description for pet, task in plan] == [
        "Grooming",
        "Feeding",
    ]
    assert scheduler.skipped_tasks == [(buddy, walk_task)]


def test_generate_plan_with_zero_available_minutes():
    owner = Owner("Alex", 0)
    buddy = Pet("Buddy", "dog", 3)
    walk_task = Task("Walk", 10, priority="high")

    buddy.add_task(walk_task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert plan == []
    assert scheduler.skipped_tasks == [(buddy, walk_task)]


def test_generate_plan_with_no_pets_or_tasks():
    owner = Owner("Alex", 60)
    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert plan == []
    assert scheduler.skipped_tasks == []


def test_generate_plan_excludes_completed_tasks():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)

    completed_task = Task("Breakfast", 10, priority="high")
    pending_task = Task("Walk", 30, priority="medium")

    completed_task.mark_complete()

    buddy.add_task(completed_task)
    buddy.add_task(pending_task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert len(plan) == 1
    assert plan[0] == (buddy, pending_task)
    assert all(
        not task.is_completed
        for pet, task in plan
    )


def test_explain_plan_reports_when_all_tasks_fit():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)
    buddy.add_task(Task("Feeding", 10, priority="high"))
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    explanation = scheduler.explain_plan()

    assert explanation == "All pending tasks fit into the available time."


def test_explain_plan_reports_skipped_tasks():
    owner = Owner("Alex", 10)
    buddy = Pet("Buddy", "dog", 3)
    walk_task = Task("Long walk", 30, priority="high")
    buddy.add_task(walk_task)
    owner.add_pet(buddy)

    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    explanation = scheduler.explain_plan()

    assert "Long walk" in explanation
    assert "Buddy" in explanation
    assert "skipped" in explanation
    assert "not enough time" in explanation



def test_sort_by_time_with_empty_list():
    owner = Owner("Alex", 60)
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time([]) == []


def test_sort_by_time_keeps_tasks_with_equal_times():
    owner = Owner("Alex", 60)
    pet = Pet("Buddy", "dog", 3)

    first_task = Task("Feeding", 10, time="08:00")
    second_task = Task("Walking", 20, time="08:00")
    third_task = Task("Grooming", 15, time="08:00")

    tasks = [
        (pet, first_task),
        (pet, second_task),
        (pet, third_task),
    ]

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.description for pet, task in sorted_tasks] == [
        "Feeding",
        "Walking",
        "Grooming",
    ]


def test_sort_by_time_does_not_change_original_list():
    owner = Owner("Alex", 60)
    pet = Pet("Buddy", "dog", 3)

    late_task = Task("Grooming", 20, time="18:00")
    early_task = Task("Feeding", 10, time="07:30")
    middle_task = Task("Walking", 30, time="08:00")

    tasks = [
        (pet, late_task),
        (pet, early_task),
        (pet, middle_task),
    ]
    original_tasks = tasks.copy()

    scheduler = Scheduler(owner)
    scheduler.sort_by_time(tasks)

    assert tasks == original_tasks


def test_filter_tasks_by_pet_and_completion_together():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)
    mochi = Pet("Mochi", "cat", 2)
    owner.add_pet(buddy)
    owner.add_pet(mochi)

    buddy_done = Task("Feed Buddy", 10)
    buddy_pending = Task("Walk Buddy", 20)
    mochi_done = Task("Feed Mochi", 10)

    buddy_done.mark_complete()
    mochi_done.mark_complete()

    owner.add_task(buddy, buddy_done)
    owner.add_task(buddy, buddy_pending)
    owner.add_task(mochi, mochi_done)

    scheduler = Scheduler(owner)
    result = scheduler.filter_tasks(pet_name="Buddy", completed=True)

    assert len(result) == 1
    assert result[0] == (buddy, buddy_done)


def test_filter_tasks_by_unknown_pet_returns_empty_list():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)
    owner.add_pet(buddy)
    owner.add_task(buddy, Task("Walk", 20))

    scheduler = Scheduler(owner)
    result = scheduler.filter_tasks(pet_name="Unknown")

    assert result == []


def test_filter_tasks_without_filters_returns_all_tasks():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "dog", 3)
    owner.add_pet(buddy)

    finished = Task("Feed", 10)
    pending = Task("Walk", 20)
    finished.mark_complete()

    owner.add_task(buddy, finished)
    owner.add_task(buddy, pending)

    scheduler = Scheduler(owner)
    result = scheduler.filter_tasks()

    assert len(result) == 2
    assert (buddy, finished) in result
    assert (buddy, pending) in result


def test_filter_tasks_when_owner_has_no_pets():
    owner = Owner("Alex", 60)
    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks() == []
    assert scheduler.filter_tasks(pet_name="Buddy") == []
    assert scheduler.filter_tasks(completed=False) == []


def test_complete_weekly_task_creates_next_occurrence():
    pet = Pet("Buddy", "dog", 3)
    task = Task(
        "Grooming",
        20,
        priority="medium",
        frequency="weekly",
        due_date=date(2026, 10, 20),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 27)
    assert next_task.frequency == "weekly"
    assert len(pet.tasks) == 2


def test_complete_daily_task_across_year_boundary():
    pet = Pet("Buddy", "dog", 3)
    task = Task(
        "Feed breakfast",
        10,
        frequency="daily",
        due_date=date(2026, 12, 31),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == date(2027, 1, 1)


def test_next_occurrence_copies_original_task_details():
    pet = Pet("Buddy", "dog", 3)
    task = Task(
        "Evening walk",
        25,
        priority="high",
        frequency="daily",
        time="18:30",
        due_date=date(2026, 10, 20),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task.description == task.description
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.priority == task.priority
    assert next_task.frequency == task.frequency
    assert next_task.time == task.time
    assert next_task.due_date == date(2026, 10, 21)
    assert next_task.is_completed is False


def test_completing_same_daily_task_twice_does_not_duplicate_next_occurrence():
    pet = Pet("Buddy", "dog", 3)
    task = Task(
        "Feed breakfast",
        10,
        frequency="daily",
        due_date=date(2026, 10, 20),
    )
    pet.add_task(task)

    pet.complete_task(task)
    pet.complete_task(task)

    assert len(pet.tasks) == 2


def test_find_next_available_slot_with_no_tasks():
    scheduler = Scheduler(Owner("Alex", 60))

    assert scheduler.find_next_available_slot([], 30, start_time="08:00") == "08:00"


def test_find_next_available_slot_uses_gap_between_tasks():
    buddy = Pet("Buddy", "dog", 3)
    tasks = [
        (buddy, Task("Walk", 30, time="08:00")),
        (buddy, Task("Grooming", 20, time="09:00")),
    ]
    scheduler = Scheduler(Owner("Alex", 60))

    # 08:30 to 09:00 is free, and back-to-back tasks are allowed.
    assert scheduler.find_next_available_slot(tasks, 30, start_time="08:00") == "08:30"


def test_find_next_available_slot_skips_overlapping_tasks():
    buddy = Pet("Buddy", "dog", 3)
    mochi = Pet("Mochi", "cat", 2)
    tasks = [
        (buddy, Task("Walk", 30, time="08:00")),
        (mochi, Task("Feed", 10, time="08:20")),
        (buddy, Task("Grooming", 20, time="08:40")),
    ]
    scheduler = Scheduler(Owner("Alex", 60))

    # The 08:30-08:40 gap is too short for 15 minutes, so the
    # first fit is right after Grooming ends.
    assert scheduler.find_next_available_slot(tasks, 15, start_time="08:00") == "09:00"


def test_find_next_available_slot_when_start_is_inside_a_task():
    buddy = Pet("Buddy", "dog", 3)
    tasks = [(buddy, Task("Walk", 60, time="07:30"))]
    scheduler = Scheduler(Owner("Alex", 60))

    assert scheduler.find_next_available_slot(tasks, 10, start_time="08:00") == "08:30"


def test_find_next_available_slot_returns_none_when_day_is_full():
    buddy = Pet("Buddy", "dog", 3)
    tasks = [(buddy, Task("Overnight care", 60, time="23:00"))]
    scheduler = Scheduler(Owner("Alex", 60))

    assert scheduler.find_next_available_slot(tasks, 30, start_time="22:45") is None


def test_find_next_available_slot_can_end_exactly_at_midnight():
    scheduler = Scheduler(Owner("Alex", 60))

    assert scheduler.find_next_available_slot([], 30, start_time="23:30") == "23:30"


def test_find_next_available_slot_rejects_invalid_duration():
    scheduler = Scheduler(Owner("Alex", 60))

    with pytest.raises(ValueError):
        scheduler.find_next_available_slot([], 0)
