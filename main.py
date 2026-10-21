
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create an owner with 60 minutes available for pet care
    owner = Owner(
        name="Alex",
        available_minutes=60,
        preferences=["morning walks"],
    )

    # Create two pets
    buddy = Pet(name="Buddy", species="dog", age=3)
    mochi = Pet(name="Mochi", species="cat", age=2)

    # Add the pets to the owner
    owner.add_pet(buddy)
    owner.add_pet(mochi)

    # Add tasks OUT OF TIME ORDER to test sorting
    owner.add_task(
        buddy,
        Task("Morning walk", 30, "high", "daily", time="08:30"),
    )
    owner.add_task(
        buddy,
        Task("Grooming", 20, "low", "weekly", time="10:00"),
    )
    owner.add_task(
        mochi,
        Task("Feed breakfast", 10, "high", "daily", time="08:30"),
    )

    # Create the scheduler
    scheduler = Scheduler(owner)

    # Generate and print the original schedule
    scheduler.generate_plan()

    print("Today's Schedule")
    print("================")
    scheduler.display_plan()

    print("\nSchedule Notes")
    print("==============")
    print(scheduler.explain_plan())

    # -----------------------------------------
    # NEW: Demonstrate sorting and filtering
    # -----------------------------------------

    # Get all tasks for both pets
    all_tasks = scheduler.collect_tasks()

    # Sort tasks by scheduled time
    print("\nTasks Sorted by Time")
    print("====================")
    sorted_tasks = scheduler.sort_by_time(all_tasks)

    for pet, task in sorted_tasks:
        print(f"{task.time} - {task.description} ({pet.name})")

    # Filter tasks by pet name
    print("\nTasks for Buddy")
    print("===============")
    buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")

    for pet, task in buddy_tasks:
        print(f"{task.time} - {task.description}")

    # Filter tasks by completion status
    print("\nPending Tasks")
    print("=============")
    pending_tasks = scheduler.filter_tasks(completed=False)

    for pet, task in pending_tasks:
        print(f"{task.time} - {task.description} ({pet.name})")


    # Detect and print scheduling conflicts
    print("\nTask Conflict Warnings")
    print("======================")

    all_tasks = scheduler.collect_tasks()
    conflicts = scheduler.detect_conflicts(all_tasks)

    if conflicts:
        for warning in conflicts:
            print(f"WARNING: {warning}")
    else:
        print("No scheduling conflicts detected.")


if __name__ == "__main__":
    main()
