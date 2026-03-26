# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design centered on four main classes: `Task`, `Pet`, `Owner`, and `PawPalSystem`. I also introduced three enums — `Priority` (HIGH, MEDIUM, LOW), `TaskType` (FEEDING, GROOMING, EXERCISE, MEDICATION, PLAY, OTHER), and `RecurrencePattern` (DAILY, WEEKLY, BIWEEKLY, MONTHLY) — to avoid raw strings and make the code self-documenting. The diagram showed `Owner` aggregating a list of `Pet` objects, each `Pet` owning a list of `Task` objects, and `PawPalSystem` acting as the top-level manager that holds all owners and exposes the scheduling interface.

**b. What classes did you include and why?**

I included `Task` as a dataclass to hold all scheduling-relevant attributes: name, task type, duration, start time, priority, recurrence, and a completion flag. `Pet` groups the tasks that belong to a specific animal and provides a `mark_task_complete()` method so completion state lives close to the data. `Owner` aggregates pets and is the natural unit for daily plan generation since real owners schedule care across all their animals. `PawPalSystem` is the application façade — it keeps a registry of owners and exposes `generate_daily_plan()` and `generate_schedule()` so callers never need to manipulate pets or tasks directly. The enums were included because priority comparison is numeric (HIGH=3, MEDIUM=2, LOW=1) and that ordering drives the greedy scheduler.

**c. What changes did you make from your initial design and why?**

The most significant change from the initial design was adding `get_next_occurrence()` as a helper method on `Task`. Originally I planned to handle recurrence logic in `PawPalSystem.generate_schedule()`, but having recurrence intrinsically understood by the task itself made the multi-day schedule generation much cleaner — the caller just asks each task when it next fires and doesn't need to know the recurrence rules. I also added the `time_available_minutes` parameter to `generate_daily_plan()` after realizing that without a time budget the plan could schedule more tasks than a day actually allows.

---

## 2. Scheduling Logic and Tradeoffs

**a. How does your scheduling algorithm work?**

`generate_daily_plan()` uses a greedy priority-first approach. Given a list of pending tasks (those not yet completed), it sorts them in descending priority order (HIGH → MEDIUM → LOW). It then iterates through the sorted list and, for each task, checks two conditions before including it: (1) adding the task's duration would not exceed `time_available_minutes`, and (2) the task's time window does not overlap with any already-selected task. Overlap is detected by checking whether `[start, start+duration)` intervals intersect. Tasks that pass both checks are added to the plan; those that fail either check are skipped.

**b. What tradeoffs did you make?**

The greedy priority-first approach is simple and transparent but not globally optimal. It can produce a shorter total plan than necessary when a low-priority task that fits perfectly is skipped in favor of a high-priority task that causes a later high-value task to be dropped due to conflict. A more sophisticated approach would use dynamic programming or constraint satisfaction, but those are overkill for a personal pet-care app where the schedule rarely has more than 10–15 tasks per day. I also chose to skip conflicting tasks rather than rescheduling them to the next available slot, which keeps the implementation simple but means a conflict silently removes a task from the plan instead of moving it.

**c. What would you do differently with more time?**

With more time I would replace the greedy skip with a "reschedule to next open slot" strategy: if a task conflicts, try to push its start time to the end of the conflicting block and re-check. I would also add a notification/reminder system (currently the app has no alerting) and allow tasks to be assigned to a specific pet rather than requiring the caller to know which pet's list to modify.

---

## 3. AI Collaboration

**a. How did you use AI assistance in this project?**

I used AI assistance to scaffold the initial UML class diagram in Mermaid.js syntax, which helped me visualize the ownership relationships between `Owner`, `Pet`, and `Task` before writing any code. I also used AI to draft the docstrings and type annotations across the dataclasses, which kept the interface documentation consistent. For the Streamlit app I used AI to suggest the `st.session_state` pattern for preserving the `PawPalSystem` object between reruns, since Streamlit's execution model (re-runs the whole script on every interaction) requires explicit state management.

**b. What did you verify or change after AI suggestions?**

The AI's first suggestion for `generate_daily_plan()` did not include a time budget parameter — it assumed unlimited time. I added the `time_available_minutes` constraint myself after thinking through the real use case. I also changed the priority enum values: the AI originally suggested string comparisons ("high" > "low" is not meaningful in Python), and I switched to integer values (HIGH=3, MEDIUM=2, LOW=1) so that `sorted(..., key=lambda t: t.priority.value, reverse=True)` works correctly. The conflict detection logic was also written from scratch after the AI's initial version compared only start times rather than checking full interval overlaps.

**c. What did you learn about working with AI on a coding project?**

AI is most valuable for boilerplate — dataclass definitions, docstrings, Streamlit layout code — where the pattern is repetitive and getting it right is just time-consuming. It's least reliable for algorithmic correctness (the time-budget omission, the broken priority comparison) and for edge cases the AI hasn't been asked to think about. The best workflow was to let AI generate a first draft, then mentally simulate a few concrete inputs through the code to find the gaps.

---

## 4. Testing and Verification

**a. How did you test your project?**

Testing used `pytest` with 15 tests organized into four test classes: `TestTask` (task creation, default values, mark_complete, recurring task generation via `get_next_occurrence()`), `TestPet` (add task, remove task, pet attributes), `TestOwner` (owner-pet relationship, add/remove pets), and `TestPawPalSystem` (priority sorting, conflict detection, `generate_daily_plan()` with and without time constraints, multi-day `generate_schedule()`). I also ran `cli_demo.py` manually to verify end-to-end behavior across all six demo scenarios, including the conflict detection demo and the recurring-task multi-day schedule.

**b. What kinds of bugs did testing reveal?**

Testing revealed that the initial `get_next_occurrence()` implementation returned the correct date for DAILY recurrence but was off by one day for WEEKLY recurrence when the base date was a Sunday (edge case with `timedelta(weeks=1)` crossing a month boundary). The conflict detection test also caught that my initial overlap check used `>=` instead of `>` for the boundary condition, which flagged back-to-back tasks (e.g., 9:00–10:00 and 10:00–11:00) as conflicting even though they don't overlap.

**c. What would you test more thoroughly with more time?**

With more time I would add property-based tests using `hypothesis` to fuzz the conflict detection and time-budget logic with random task lists. I would also test the Streamlit app using `streamlit-testing` or Selenium to verify that state persists correctly between widget interactions, since the manual testing of the UI was not systematic.

---

## 5. Reflection

**a. What was the most challenging part of this project?**

The most challenging part was designing the scheduling algorithm to be both correct and simple. The interaction between priority ordering, conflict detection, and the time budget creates a three-way constraint, and it was easy to write a version that handled each constraint individually but broke when all three interacted. Walking through the greedy approach on paper with concrete examples (a HIGH-priority 60-minute task conflicting with a MEDIUM-priority 30-minute task when 90 minutes of budget remain) clarified the logic before I wrote any code.

**b. What are you most proud of?**

I am most proud of the recurring task system. `get_next_occurrence()` cleanly handles four recurrence patterns using Python's `timedelta` and `relativedelta` without any special-casing per pattern, and the multi-day schedule generation in `generate_schedule()` composes it naturally by asking each recurring task when it next fires relative to the current day in the loop. The result is a multi-day view that automatically places recurring tasks on the right days without any calendar logic in the caller.

**c. What would you do differently if starting over?**

I would define the `Task` dataclass with `slots=True` from the beginning (Python 3.10+) to reduce memory overhead for large task lists, and I would separate "task template" (what to do, how often) from "task instance" (scheduled occurrence on a specific day). The current design conflates these, which makes it awkward to distinguish "this recurring task fires today" from "this specific instance was completed." Separating the two would make the data model cleaner and the UI more intuitive.
