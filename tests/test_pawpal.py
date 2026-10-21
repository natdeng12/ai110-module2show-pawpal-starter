
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