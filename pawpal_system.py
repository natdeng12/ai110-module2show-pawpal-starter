
from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    is_completed: bool = False

    def mark_complete(self) -> None:
        pass

    def mark_incomplete(self) -> None:
        pass

    def get_priority_value(self) -> int:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass

    def get_pending_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_time: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, pet: Pet, task: Task) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.daily_plan: list[Task] = []

    def collect_tasks(self) -> list[Task]:
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass

    def generate_plan(self) -> list[Task]:
        pass

    def display_plan(self) -> None:
        pass

    def explain_plan(self) -> str:
        pass
