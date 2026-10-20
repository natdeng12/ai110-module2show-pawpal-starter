
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

    # Create three care tasks with different durations
    owner.add_task(
        buddy,
        Task("Morning walk", 30, "high", "daily"),
    )
    owner.add_task(
        buddy,
        Task("Grooming", 20, "low", "weekly"),
    )
    owner.add_task(
        mochi,
        Task("Feed breakfast", 10, "high", "daily"),
    )

    # Generate and print the schedule
    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    print("Today's Schedule")
    print("================")
    scheduler.display_plan()

    print("\nSchedule Notes")
    print("==============")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
