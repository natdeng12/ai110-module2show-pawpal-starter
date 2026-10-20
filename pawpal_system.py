
from dataclasses import dataclass, field
from typing import Literal


Priority = Literal["low", "medium", "high"]
Frequency = Literal["daily", "weekly", "as_needed"]


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: Priority = "medium"
    frequency: Frequency = "daily"
    is_completed: bool = False

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


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner, skipping it if it is already added."""
        if pet not in self.pets:
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
