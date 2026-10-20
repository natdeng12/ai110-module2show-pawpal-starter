# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
The PawPal+ app should allow users to do the following core actions:
- Manage pet information: Users can enter basic information about their pets, such as the pet's type  and name.
- Manage pet care tasks: Users can add and edit care tasks, such as walking, feeding, grooming, and giving medicine. Each task should include its duration and priority.
- Generate a daily care plan: Users can generate a daily schedule that organizes care tasks based on their available time and the importance of each task.

I designed the PawPal+ system around four classes: Owner, Pet, Task, and Scheduler.

Owner: Stores the owner's name, available time for pet care, and list of pets. It can add pets and assign tasks to them.

Pet: Stores a pet's name, species, age, special needs, and care tasks.

Task: Stores the task title, duration, priority, and completion status. It will support marking tasks as complete or incomplete.

Scheduler: Collects care tasks and organizes them into a daily plan based on task priority and the owner's available time.

The relationships are that one owner can manage multiple pets, each pet can have multiple tasks, and the scheduler uses the owner, pets, and tasks to generate a daily care plan.

I used Python dataclasses for Owner, Pet, and Task to make storing their information simpler. The methods are currently placeholders and will be implemented later.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
After reviewing my initial class skeleton with an AI coding assistant, I made several improvements.

I updated the scheduler's task collections to store pairs of pets and tasks. This allows the daily plan to identify which pet each care task belongs to, even when different pets have tasks with the same name.

I added a preferences attribute to the Owner class to better represent the owner's needs and preferences.

I renamed available_time to available_minutes to make the time unit explicit and consistent with Task.duration_minutes.

I used Python's Literal type to specify the allowed task priorities: low, medium, and high.

I added skipped_tasks to the scheduler so it can eventually explain which tasks were left out of a daily plan.

I added remove_pet() and get_pets() to the Owner class to better match the UML design.

These changes make the relationships clearer and prepare the system for implementing the scheduling logic. The methods remain placeholders because this stage focuses on the class structure rather than full functionality.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

### AI Collaboration Reflection

I used an AI coding assistant to help develop the PawPal+ class structure and implement the core logic. The assistant helped me understand how the `Owner`, `Pet`, `Task`, and `Scheduler` classes work together. It also identified a design issue: tasks needed to remain associated with their pets so that the schedule could identify which pet each task belonged to.

I accepted the suggestion to add `Owner.get_all_tasks()` so the scheduler could retrieve tasks across multiple pets. I also used dataclasses to organize object information and added basic automated tests for task completion and task addition.

To verify the implementation, I ran the demo script with `python main.py` and ran the automated tests with `python -m pytest`. The tests helped me check that the implemented methods behaved as expected. I learned that AI-generated code still needs to be reviewed and tested rather than accepted without verification.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
