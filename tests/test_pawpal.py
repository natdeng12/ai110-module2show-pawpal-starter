
from pawpal_system import Pet, Task


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
