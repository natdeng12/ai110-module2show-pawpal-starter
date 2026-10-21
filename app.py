import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Alex",
        available_minutes=60,
    )

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()


st.divider()

st.subheader("Quick Demo Inputs")

owner_name = st.text_input("Owner name", value="Jordan")
st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    if not pet_name.strip():
        st.error("Please enter a pet name.")
    elif any(
        pet.name.lower() == pet_name.strip().lower()
        for pet in st.session_state.owner.pets
    ):
        st.warning("A pet with that name already exists.")
    else:
        new_pet = Pet(
            name=pet_name.strip(),
            species=species,
            age=0,
        )
        st.session_state.owner.add_pet(new_pet)
        st.success(f"{pet_name} was added!")

st.markdown("### Your Pets")

if st.session_state.owner.pets:
    for pet in st.session_state.owner.get_pets():
        st.write(f"🐾 {pet.name} — {pet.species}")
else:
    st.info("No pets yet. Add a pet above.")

st.divider()

st.subheader("Add a Care Task")

owner = st.session_state.owner

if owner.pets:
    selected_pet = st.selectbox(
        "Which pet is this task for?",
        owner.pets,
        format_func=lambda pet: pet.name,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        task_title = st.text_input(
            "Task title",
            value="Morning walk",
        )

    with col2:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20,
        )

    with col3:
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=2,
        )

    if st.button("Add task"):
        if not task_title.strip():
            st.error("Please enter a task title.")
        else:
            new_task = Task(
                description=task_title.strip(),
                duration_minutes=int(duration),
                priority=priority,
            )
            owner.add_task(selected_pet, new_task)
            st.success(f"Added '{task_title}' for {selected_pet.name}!")

    st.markdown("### Current Tasks")

    task_rows = []

    for pet in owner.get_pets():
        for task in pet.get_tasks():
            task_rows.append({
                "Pet": pet.name,
                "Task": task.description,
                "Duration (minutes)": task.duration_minutes,
                "Priority": task.priority,
                "Completed": task.is_completed,
            })

    if task_rows:
        st.table(task_rows)
    else:
        st.info("No tasks yet. Add a task above.")

else:
    st.info("Add a pet first, then you can assign care tasks.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_plan()

    if schedule:
        st.markdown("### Today's Schedule")

        for pet, task in schedule:
            st.write(
                f"🐾 **{pet.name}** — {task.description} "
                f"({task.duration_minutes} minutes, {task.priority} priority)"
            )
    else:
        st.info("No pending tasks fit into the available time.")

    st.markdown("### Schedule Notes")
    st.write(scheduler.explain_plan())
