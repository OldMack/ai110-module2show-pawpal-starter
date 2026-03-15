"""
PawPal+ CLI Demo Script
Demonstrates the core functionality of the PawPal+ system
"""

from pawpal_system import (
    PawPalSystem, Owner, Pet, Task,
    Priority, TaskType, RecurrencePattern
)
from datetime import datetime, timedelta


def create_sample_data():
    """Create sample data for demonstration"""
    system = PawPalSystem()
    
    # Create owner
    owner = Owner("John Smith", "john@example.com")
    system.add_owner(owner)
    
    # Create pets
    dog = Pet("Buddy", "Dog", "Golden Retriever", age=3)
    cat = Pet("Whiskers", "Cat", "Persian", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create tasks for the dog
    tasks = [
        Task("Morning Walk", TaskType.WALK, 30, Priority.HIGH, 
             scheduled_time=datetime.now().replace(hour=7, minute=0)),
        Task("Breakfast Feeding", TaskType.FEEDING, 15, Priority.HIGH,
             scheduled_time=datetime.now().replace(hour=8, minute=0)),
        Task("Midday Medication", TaskType.MEDICATION, 10, Priority.HIGH,
             scheduled_time=datetime.now().replace(hour=12, minute=0),
             is_recurring=True, recurrence=RecurrencePattern.DAILY),
        Task("Afternoon Walk", TaskType.WALK, 30, Priority.MEDIUM,
             scheduled_time=datetime.now().replace(hour=15, minute=0)),
        Task("Evening Walk", TaskType.WALK, 30, Priority.MEDIUM,
             scheduled_time=datetime.now().replace(hour=18, minute=0)),
        Task("Dinner Feeding", TaskType.FEEDING, 15, Priority.HIGH,
             scheduled_time=datetime.now().replace(hour=19, minute=0)),
        Task("Grooming Session", TaskType.GROOMING, 45, Priority.LOW,
             scheduled_time=datetime.now().replace(hour=14, minute=0)),
    ]
    
    for task in tasks:
        dog.add_task(task)
    
    # Create tasks for the cat
    cat_tasks = [
        Task("Morning Feeding", TaskType.FEEDING, 10, Priority.HIGH,
             scheduled_time=datetime.now().replace(hour=7, minute=30)),
        Task("Evening Feeding", TaskType.FEEDING, 10, Priority.HIGH,
             scheduled_time=datetime.now().replace(hour=18, minute=30)),
        Task("Litter Box Clean", TaskType.GROOMING, 15, Priority.MEDIUM,
             scheduled_time=datetime.now().replace(hour=10, minute=0)),
    ]
    
    for task in cat_tasks:
        cat.add_task(task)
    
    return system


def demo_basic_operations():
    """Demonstrate basic system operations"""
    print("\n" + "="*60)
    print("DEMO 1: Basic Operations")
    print("="*60)
    
    system = create_sample_data()
    owner = system.get_owner_by_email("john@example.com")
    
    print(f"\nOwner: {owner.name}")
    print(f"Email: {owner.email}")
    print(f"\nPets:")
    for pet in owner.pets:
        print(f"  - {pet.name} ({pet.species}, {pet.breed}, age {pet.age})")
        print(f"    Tasks: {len(pet.get_all_tasks())}")


def demo_sorting():
    """Demonstrate task sorting by priority"""
    print("\n" + "="*60)
    print("DEMO 2: Task Sorting by Priority")
    print("="*60)
    
    system = create_sample_data()
    owner = system.get_owner_by_email("john@example.com")
    
    all_tasks = owner.get_all_tasks()
    sorted_tasks = system.sort_tasks_by_priority(all_tasks)
    
    print("\nTasks sorted by priority (HIGH -> LOW):")
    for i, task in enumerate(sorted_tasks, 1):
        print(f"  {i}. {task.title} - {task.priority.name} ({task.duration_minutes} min)")


def demo_conflict_detection():
    """Demonstrate conflict detection"""
    print("\n" + "="*60)
    print("DEMO 3: Conflict Detection")
    print("="*60)
    
    system = create_sample_data()
    owner = system.get_owner_by_email("john@example.com")
    
    all_tasks = owner.get_all_tasks()
    conflicts = system.detect_conflicts(all_tasks)
    
    if conflicts:
        print("\nConflicts detected:")
        for task1, task2 in conflicts:
            print(f"  - {task1.title} overlaps with {task2.title}")
    else:
        print("\nNo conflicts detected!")


def demo_daily_plan():
    """Demonstrate daily plan generation"""
    print("\n" + "="*60)
    print("DEMO 4: Daily Plan Generation")
    print("="*60)
    
    system = create_sample_data()
    today = datetime.now()
    
    plan = system.generate_daily_plan("john@example.com", today, time_available_minutes=120)
    
    print(f"\nDate: {plan['date']}")
    print(f"Owner: {plan['owner']}")
    print(f"Total scheduled time: {plan['total_time_minutes']} minutes")
    print(f"Time available: {plan['time_available']} minutes")
    print(f"Unscheduled tasks: {plan['unscheduled_tasks']}")
    
    print("\nScheduled Tasks:")
    for task in plan['scheduled_tasks']:
        time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "TBD"
        print(f"  [{time_str}] {task.title} ({task.task_type.value}) - {task.duration_minutes} min")


def demo_recurring_tasks():
    """Demonstrate recurring task generation"""
    print("\n" + "="*60)
    print("DEMO 5: Recurring Tasks")
    print("="*60)
    
    system = create_sample_data()
    owner = system.get_owner_by_email("john@example.com")
    
    # Find the recurring task
    recurring_task = None
    for pet in owner.pets:
        for task in pet.get_all_tasks():
            if task.is_recurring:
                recurring_task = task
                print(f"\nOriginal task: {task.title}")
                print(f"  Recurrence: {task.recurrence.value}")
                print(f"  Scheduled: {task.scheduled_time}")
                break
    
    if recurring_task:
        print("\nNext occurrences:")
        for i in range(3):
            next_task = recurring_task.get_next_occurrence()
            if next_task:
                print(f"  {i+1}. {next_task.title} at {next_task.scheduled_time}")
                recurring_task = next_task


def demo_multi_day_schedule():
    """Demonstrate multi-day schedule generation"""
    print("\n" + "="*60)
    print("DEMO 6: Multi-Day Schedule")
    print("="*60)
    
    system = create_sample_data()
    start_date = datetime.now()
    
    schedule = system.generate_schedule("john@example.com", start_date, days=3)
    
    for date_key, plan in schedule.items():
        print(f"\n{date_key}:")
        print(f"  Total time: {plan['total_time_minutes']} min")
        print(f"  Tasks: {len(plan['scheduled_tasks'])}")


def main():
    """Run all demos"""
    print("\n" + "#"*60)
    print("# PawPal+ CLI Demo - Smart Pet Care Management")
    print("#"*60)
    
    demo_basic_operations()
    demo_sorting()
    demo_conflict_detection()
    demo_daily_plan()
    demo_recurring_tasks()
    demo_multi_day_schedule()
    
    print("\n" + "#"*60)
    print("# Demo Complete!")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()
