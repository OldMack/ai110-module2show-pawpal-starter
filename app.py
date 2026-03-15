"""
PawPal+ Streamlit UI
Connects the Streamlit UI to the PawPal+ backend system
"""

import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import (
    PawPalSystem, Owner, Pet, Task,
    Priority, TaskType, RecurrencePattern
)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = PawPalSystem()
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("*Smart Pet Care Management System*")

# Sidebar for owner info
with st.sidebar:
    st.header("👤 Owner Info")
    owner_name = st.text_input("Owner Name", value="John")
    owner_email = st.text_input("Owner Email", value="john@example.com")
    
    st.header("🐕 Add Pet")
    pet_name = st.text_input("Pet Name", value="Buddy")
    pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Fish", "Other"])
    pet_breed = st.text_input("Breed", value="Golden Retriever")
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=3)
    
    if st.button("Add Pet"):
        # Create pet and add to system
        pet = Pet(pet_name, pet_species, pet_breed, pet_age)
        
        # Check if owner exists
        owner = st.session_state.system.get_owner_by_email(owner_email)
        if not owner:
            owner = Owner(owner_name, owner_email)
            st.session_state.system.add_owner(owner)
        
        owner.add_pet(pet)
        st.success(f"Added {pet_name} ({pet_species})!")

# Main content
with st.expander("📋 Current Pets & Tasks", expanded=True):
    owner = st.session_state.system.get_owner_by_email(owner_email)
    if owner:
        st.write(f"**Owner:** {owner.name} ({owner.email})")
        st.write(f"**Pets:** {len(owner.pets)}")
        
        for pet in owner.pets:
            st.write(f"  - {pet.name} ({pet.species}, {pet.breed}, age {pet.age})")
            pet_tasks = pet.get_all_tasks()
            if pet_tasks:
                st.write(f"    Tasks: {len(pet_tasks)}")
    else:
        st.info("Add a pet in the sidebar to get started!")

# Add task section
st.header("➕ Add Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task Title", value="Morning Walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=5, max_value=240, value=30)
with col3:
    priority = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"], index=0)

col4, col5 = st.columns(2)
with col4:
    task_type = st.selectbox("Task Type", [t.name for t in TaskType])
with col5:
    scheduled_time = st.time_input("Scheduled Time", value=None)

# Recurring options
is_recurring = st.checkbox("Recurring Task?")
recurrence = None
if is_recurring:
    recurrence = st.selectbox("Repeat", [r.name for r in RecurrencePattern])

if st.button("Add Task"):
    # Get or create owner and pet
    owner = st.session_state.system.get_owner_by_email(owner_email)
    if not owner:
        owner = Owner(owner_name, owner_email)
        st.session_state.system.add_owner(owner)
    
    if not owner.pets:
        st.error("Please add a pet first!")
    else:
        # Add to first pet (simplified)
        pet = owner.pets[0]
        
        # Convert priority string to enum
        priority_enum = Priority[priority]
        task_type_enum = TaskType[task_type]
        
        # Convert time to datetime
        scheduled_dt = None
        if scheduled_time:
            now = datetime.now()
            scheduled_dt = now.replace(
                hour=scheduled_time.hour,
                minute=scheduled_time.minute,
                second=0
            )
        
        # Create recurrence enum if needed
        recurrence_enum = None
        if is_recurring and recurrence:
            recurrence_enum = RecurrencePattern[recurrence]
        
        task = Task(
            title=task_title,
            task_type=task_type_enum,
            duration_minutes=duration,
            priority=priority_enum,
            scheduled_time=scheduled_dt,
            is_recurring=is_recurring,
            recurrence=recurrence_enum
        )
        
        pet.add_task(task)
        st.success(f"Added task: {task_title} ({duration} min, {priority} priority)")

# Display current tasks
if owner and owner.pets:
    st.subheader("📝 Today's Tasks")
    
    today = datetime.now()
    all_tasks = owner.get_all_tasks()
    
    if all_tasks:
        # Sort by priority
        sorted_tasks = st.session_state.system.sort_tasks_by_priority(all_tasks)
        
        for task in sorted_tasks:
            time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "No time"
            st.write(f"• **{task.title}** ({task.task_type.value}) - {task.duration_minutes} min - {task.priority.name} - {time_str}")
    else:
        st.info("No tasks yet. Add some above!")

# Generate Schedule section
st.divider()
st.header("📅 Generate Daily Plan")

col_plan1, col_plan2 = st.columns(2)
with col_plan1:
    plan_date = st.date_input("Date", value=datetime.now().date())
with col_plan2:
    time_available = st.slider("Time Available (minutes)", 60, 480, 120, step=30)

if st.button("🎯 Generate Schedule"):
    if not owner or not owner.pets:
        st.error("Please add a pet first!")
    else:
        plan_date_dt = datetime.combine(plan_date, datetime.min.time())
        plan = st.session_state.system.generate_daily_plan(
            owner_email, 
            plan_date_dt, 
            time_available_minutes=time_available
        )
        
        if "error" in plan:
            st.error(plan["error"])
        else:
            st.success(f"Generated plan for {plan['date']}!")
            
            st.metric("Total Time", f"{plan['total_time_minutes']} min")
            st.metric("Time Available", f"{plan['time_available']} min")
            st.metric("Unscheduled", plan['unscheduled_tasks'])
            
            st.subheader("✅ Scheduled Tasks")
            for i, task in enumerate(plan['scheduled_tasks'], 1):
                time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "TBD"
                st.write(f"{i}. **{time_str}** - {task.title} ({task.task_type.value}) - {task.duration_minutes} min")
            
            if plan['conflicts']:
                st.warning(f"⚠️ {len(plan['conflicts'])} conflict(s) detected!")

# Algorithm explanation
with st.expander("🔍 How the Scheduling Algorithm Works"):
    st.markdown("""
    ### Algorithm Overview
    
    1. **Task Collection**: Gather all tasks for the owner's pets on the specified date
    
    2. **Priority Sorting**: Sort tasks by:
       - Priority (HIGH → MEDIUM → LOW)
       - Scheduled time
    
    3. **Conflict Detection**: Check for overlapping tasks and flag conflicts
    
    4. **Time-Constrained Scheduling**: 
       - Start with highest priority tasks
       - Add tasks until time budget is exhausted
       - Track unscheduled tasks
    
    ### Key Design Decisions
    
    - Uses **greedy algorithm** for task selection
    - Prioritizes HIGH priority tasks first
    - Respects user's time availability constraint
    - Reports unscheduled tasks count
    """)

# Reflection prompt
with st.expander("📝 Reflection"):
    st.markdown("""
    ### AI Collaboration Reflection
    
    How did you use AI in this project?
    
    1. What prompts did you use to help design the system?
    2. How did AI help (or not help) with the UML design?
    3. What challenges did you face when implementing the scheduling logic?
    4. How would you improve the AI-human collaboration for future projects?
    """)
