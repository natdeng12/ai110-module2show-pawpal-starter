
from dataclasses import dataclass, field
from typing import Literal
from datetime import date, timedelta


Priority = Literal["low", "medium", "high"]
Frequency = Literal["daily", "weekly", "as_needed"]


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: Priority = "medium"
    frequency: Frequency = "daily"
    is_completed: bool = False
    time: str = "08:00"
    due_date: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        """Check that the duration, priority, and frequency are valid after creation."""
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")

        if self.priority not in ("low", "medium", "high"):
            raise ValueError("Priority must be low, medium, or high.")

        if self.frequency not in ("daily", "weekly", "as_needed"):
            raise ValueError(
                "Frequency must be daily, weekly, or as_needed."
            )
        if (
        len(self.time) != 5
        or self.time[2] != ":"
        or not self.time[:2].isdigit()
        or not self.time[3:].isdigit()
        or not (0 <= int(self.time[:2]) <= 23)
        or not (0 <= int(self.time[3:]) <= 59)
    ):
            raise ValueError("Time must be in HH:MM format (00:00 to 23:59).")

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not done yet."""
        self.is_completed = False

    def get_priority_value(self) -> int:
        """Return the priority as a number (low=1, medium=2, high=3) for sorting."""
        priority_values = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }
        return priority_values[self.priority]
    
    def get_start_minutes(self) -> int:
        """Return the task's start time as minutes since midnight.

        For example, "08:15" becomes 8 * 60 + 15 = 495. This assumes
        `time` is a valid "HH:MM" string, which __post_init__ checks
        when the task is created.
        """
        hours = int(self.time[:2])
        minutes = int(self.time[3:])
        return hours * 60 + minutes


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's list if it is there."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return a copy of all of this pet's tasks, done or not."""
        return self.tasks.copy()

    def get_pending_tasks(self) -> list[Task]:
        """Return only the tasks that are not completed yet."""
        return [
            task for task in self.tasks
            if not task.is_completed
        ]
    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and schedule its next occurrence if it repeats.

        Daily tasks get a new copy due 1 day after the old due date, and
        weekly tasks get one due 7 days after. The completed task stays in
        the list as history. Returns the new task, or None for "as_needed"
        tasks, which do not repeat, and for tasks that were already completed.

        Raises ValueError if the task does not belong to this pet.
        """
        if not any(saved_task is task for saved_task in self.tasks):
            raise ValueError("This task does not belong to this pet.")

        if task.is_completed:
            return None

        task.mark_complete()

        if task.frequency == "daily":
            next_date = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = task.due_date + timedelta(days=7)
        else:
            return None

        next_task = Task(
            description=task.description,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            time=task.time,
            due_date=next_date,
        )

        self.add_task(next_task)
        return next_task


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner, skipping it if it is already added."""
        if not any(existing_pet is pet for existing_pet in self.pets):
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner if it is there."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return a copy of this owner's list of pets."""
        return self.pets.copy()

    def add_task(self, pet: Pet, task: Task) -> None:
        """Add a task to one of this owner's pets, or raise an error if the pet isn't theirs."""
        if pet not in self.pets:
            raise ValueError("This pet does not belong to the owner.")
        pet.add_task(task)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every pending task across all pets as (pet, task) pairs."""
        all_tasks = []

        for pet in self.pets:
            for task in pet.get_pending_tasks():
                all_tasks.append((pet, task))

        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        """Create a scheduler for an owner with an empty plan and skipped list."""
        self.owner = owner
        self.daily_plan: list[tuple[Pet, Task]] = []
        self.skipped_tasks: list[tuple[Pet, Task]] = []

    def collect_tasks(self) -> list[tuple[Pet, Task]]:
        """Gather all pending (pet, task) pairs from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_priority(
        self, tasks: list[tuple[Pet, Task]]
    ) -> list[tuple[Pet, Task]]:
        """Return tasks sorted by highest priority first, then shortest duration."""
        return sorted(
            tasks,
            key=lambda item: (
                -item[1].get_priority_value(),
                item[1].duration_minutes,
            ),
        )
        
    def sort_by_time(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return a new list of (pet, task) pairs sorted by time, earliest first.

        Times are compared as "HH:MM" text, which sorts correctly because
        hours and minutes always have two digits. Tasks with the same time
        keep their original order. Due dates are not considered, and the
        original list is not changed.
        """
        return sorted(tasks, key=lambda item: item[1].time)

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs that match the given filters.

        Leave a filter as None to skip it. The pet name match ignores
        capitalization, so "mochi" matches "Mochi". Unlike collect_tasks(),
        this looks at all tasks, including completed ones, so
        completed=True can find finished tasks.
        """
        matching_tasks = []

        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                if pet_name is not None and pet.name.lower() != pet_name.lower():
                    continue

                if completed is not None and task.is_completed != completed:
                    continue

                matching_tasks.append((pet, task))

        return matching_tasks
    

    def detect_conflicts(
        self,
        tasks: list[tuple[Pet, Task]],
    ) -> list[str]:
        """Return a warning message for each pair of tasks that overlap in time.

        Tasks overlap when one starts before the other ends. Back-to-back
        tasks (one ends at 08:30, the next starts at 08:30) are allowed.
        Tasks for different pets still count, since one owner does them all.
        Returns an empty list if there are no conflicts.

        Limitation: due dates are ignored, so tasks on different days at
        the same time are reported as conflicts. Pass in only one day's
        tasks to avoid this.
        """
        sorted_tasks = self.sort_by_time(tasks)
        conflicts = []

        for i in range(len(sorted_tasks)):
            pet1, task1 = sorted_tasks[i]
            start1 = task1.get_start_minutes()
            end1 = start1 + task1.duration_minutes

            for j in range(i + 1, len(sorted_tasks)):
                pet2, task2 = sorted_tasks[j]
                start2 = task2.get_start_minutes()

                # Later tasks cannot overlap once they start
                # at or after the current task's end.
                if start2 >= end1:
                    break

                conflicts.append(
                    f"{task1.description} ({pet1.name}) overlaps "
                    f"{task2.description} ({pet2.name})."
                )

        return conflicts

    def find_next_available_slot(
        self,
        tasks: list[tuple[Pet, Task]],
        duration_minutes: int,
        start_time: str = "00:00",
    ) -> str | None:
        """Return the earliest "HH:MM" time when a task of this length fits.

        The search starts at `start_time` and skips past any task that
        would overlap, using the same rule as detect_conflicts():
        back-to-back tasks are allowed. The new task must finish by
        midnight (24:00). Returns None if no gap is long enough.

        Raises ValueError if the duration or start time is invalid.

        Limitation: due dates are ignored, like detect_conflicts().
        Pass in only one day's tasks.
        """
        # Reuse Task's checks for a positive duration and a valid time.
        start = Task("slot", duration_minutes, time=start_time).get_start_minutes()
        end_of_day = 24 * 60

        candidate = start

        for _, task in self.sort_by_time(tasks):
            task_start = task.get_start_minutes()
            task_end = task_start + task.duration_minutes

            # This task ends before the candidate slot begins.
            if task_end <= candidate:
                continue

            # The gap before this task is long enough.
            if task_start >= candidate + duration_minutes:
                break

            # The task overlaps the candidate slot, so try right after it.
            candidate = task_end

        if candidate + duration_minutes > end_of_day:
            return None

        return f"{candidate // 60:02d}:{candidate % 60:02d}"


    def generate_plan(self) -> list[tuple[Pet, Task]]:
        """Build today's plan by adding sorted tasks that fit in the owner's available time."""
        self.daily_plan = []
        self.skipped_tasks = []

        remaining_minutes = self.owner.available_minutes
        tasks = self.sort_by_priority(self.collect_tasks())

        for pet, task in tasks:
            if task.duration_minutes <= remaining_minutes:
                self.daily_plan.append((pet, task))
                remaining_minutes -= task.duration_minutes
            else:
                self.skipped_tasks.append((pet, task))

        return self.daily_plan.copy()

    def display_plan(self) -> None:
        """Print the current daily plan, or a message if no tasks fit."""
        if not self.daily_plan:
            print("No tasks fit into the available time.")
            return

        print(f"Daily care plan for {self.owner.name}:")

        for pet, task in self.daily_plan:
            print(
                f"- {task.description} ({pet.name}) - "
                f"{task.duration_minutes} minutes "
                f"[{task.priority}]"
            )

    def explain_plan(self) -> str:
        """Return a sentence explaining which tasks were skipped for lack of time."""
        if not self.skipped_tasks:
            return "All pending tasks fit into the available time."

        explanations = []

        for pet, task in self.skipped_tasks:
            explanations.append(
                f"{task.description} for {pet.name} was skipped "
                f"because there was not enough time."
            )

        return " ".join(explanations)
