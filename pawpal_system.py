"""
PawPal+ System - Core OOP Implementation
Module 2 Project - AI110
"""

from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum
import heapq


# Enumerations
class Priority(Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class TaskType(Enum):
    FEEDING = "feeding"
    WALK = "walk"
    MEDICATION = "medication"
    GROOMING = "grooming"
    ENRICHMENT = "enrichment"
    APPOINTMENT = "appointment"


class RecurrencePattern(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


# Data Classes
class Task:
    """Represents a single pet care task"""
    
    def __init__(
        self,
        title: str,
        task_type: TaskType,
        duration_minutes: int,
        priority: Priority = Priority.MEDIUM,
        description: str = "",
        scheduled_time: Optional[datetime] = None,
        is_recurring: bool = False,
        recurrence: Optional[RecurrencePattern] = None,
    ):
        self.id = id(self)
        self.title = title
        self.task_type = task_type
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.description = description
        self.scheduled_time = scheduled_time
        self.is_completed = False
        self.is_recurring = is_recurring
        self.recurrence = recurrence
        self.pet = None  # Will be set when assigned to a pet
    
    def mark_complete(self):
        """Mark task as completed"""
        self.is_completed = True
    
    def get_next_occurrence(self) -> Optional['Task']:
        """Get next occurrence for recurring tasks"""
        if not self.is_recurring or not self.recurrence:
            return None
        
        # Create next task based on recurrence pattern
        next_time = self.scheduled_time
        if self.recurrence == RecurrencePattern.DAILY:
            next_time = self.scheduled_time + timedelta(days=1)
        elif self.recurrence == RecurrencePattern.WEEKLY:
            next_time = self.scheduled_time + timedelta(weeks=1)
        elif self.recurrence == RecurrencePattern.BIWEEKLY:
            next_time = self.scheduled_time + timedelta(weeks=2)
        elif self.recurrence == RecurrencePattern.MONTHLY:
            next_time = self.scheduled_time + timedelta(days=30)
        
        return Task(
            title=self.title,
            task_type=self.task_type,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            description=self.description,
            scheduled_time=next_time,
            is_recurring=True,
            recurrence=self.recurrence,
        )
    
    def __repr__(self):
        return f"Task({self.title}, {self.task_type.value}, {self.priority.name})"


class Pet:
    """Represents a pet with care tasks"""
    
    def __init__(self, name: str, species: str, breed: str = "", age: int = 0):
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.tasks: List[Task] = []
        self.owner = None  # Will be set when assigned to owner
    
    def add_task(self, task: Task):
        """Add a task to this pet"""
        task.pet = self
        self.tasks.append(task)
    
    def get_tasks_for_day(self, date: datetime) -> List[Task]:
        """Get all tasks scheduled for a specific day"""
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        return [
            task for task in self.tasks
            if task.scheduled_time and day_start <= task.scheduled_time < day_end
        ]
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks for this pet"""
        return self.tasks
    
    def __repr__(self):
        return f"Pet({self.name}, {self.species})"


class Owner:
    """Represents a pet owner"""
    
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []
        self.assigned_tasks: List[Task] = []  # Tasks assigned directly to owner
    
    def add_pet(self, pet: Pet):
        """Add a pet to this owner"""
        pet.owner = self
        self.pets.append(pet)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets"""
        tasks = list(self.assigned_tasks)
        for pet in self.pets:
            tasks.extend(pet.get_all_tasks())
        return tasks
    
    def __repr__(self):
        return f"Owner({self.name}, {self.email})"


class PawPalSystem:
    """Main system for managing pet care and generating plans"""
    
    def __init__(self):
        self.owners: List[Owner] = []
    
    def add_owner(self, owner: Owner):
        """Add an owner to the system"""
        self.owners.append(owner)
    
    def get_owner_by_email(self, email: str) -> Optional[Owner]:
        """Find owner by email"""
        for owner in self.owners:
            if owner.email == email:
                return owner
        return None
    
    def get_all_owners(self) -> List[Owner]:
        """Get all owners"""
        return self.owners
    
    def get_all_tasks_for_owner(self, owner_email: str) -> List[Task]:
        """Get all tasks for a specific owner"""
        owner = self.get_owner_by_email(owner_email)
        if owner:
            return owner.get_all_tasks()
        return []
    
    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high to low), then by time"""
        return sorted(
            tasks,
            key=lambda t: (t.priority.value, t.scheduled_time or datetime.max),
            reverse=True
        )
    
    def detect_conflicts(self, tasks: List[Task]) -> List[tuple]:
        """Detect scheduling conflicts (tasks that overlap)"""
        conflicts = []
        sorted_tasks = sorted(
            [t for t in tasks if t.scheduled_time],
            key=lambda t: t.scheduled_time
        )
        
        for i in range(len(sorted_tasks) - 1):
            current = sorted_tasks[i]
            next_task = sorted_tasks[i + 1]
            
            if current.scheduled_time and next_task.scheduled_time:
                current_end = current.scheduled_time + timedelta(minutes=current.duration_minutes)
                if current_end > next_task.scheduled_time:
                    conflicts.append((current, next_task))
        
        return conflicts
    
    def generate_daily_plan(
        self,
        owner_email: str,
        date: datetime,
        time_available_minutes: int = 480
    ) -> dict:
        """Generate a daily care plan for an owner"""
        owner = self.get_owner_by_email(owner_email)
        if not owner:
            return {"error": "Owner not found"}
        
        # Get all tasks for the day
        all_tasks = []
        for pet in owner.pets:
            all_tasks.extend(pet.get_tasks_for_day(date))
        
        # Sort by priority
        sorted_tasks = self.sort_tasks_by_priority(all_tasks)
        
        # Check for conflicts
        conflicts = self.detect_conflicts(sorted_tasks)
        
        # Select tasks that fit within time constraint
        scheduled_tasks = []
        total_time = 0
        
        for task in sorted_tasks:
            if total_time + task.duration_minutes <= time_available_minutes:
                scheduled_tasks.append(task)
                total_time += task.duration_minutes
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "owner": owner.name,
            "total_time_minutes": total_time,
            "time_available": time_available_minutes,
            "scheduled_tasks": scheduled_tasks,
            "unscheduled_tasks": len(sorted_tasks) - len(scheduled_tasks),
            "conflicts": conflicts,
        }
    
    def generate_schedule(
        self,
        owner_email: str,
        start_date: datetime,
        days: int = 7
    ) -> dict:
        """Generate schedule for multiple days"""
        schedule = {}
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_key = date.strftime("%Y-%m-%d")
            schedule[date_key] = self.generate_daily_plan(owner_email, date)
        
        return schedule


# Demo function
def demo():
    """Demonstrate PawPal+ functionality"""
    # Create system
    system = PawPalSystem()
    
    # Create owner
    owner = Owner("Yong Hao", "yong.hao@example.com")
    system.add_owner(owner)
    
    # Create pets
    pet1 = Pet("Buddy", "Dog", "Golden Retriever", age=3)
    pet2 = Pet("Whiskers", "Cat", "Persian", age=2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    # Create tasks
    task1 = Task(
        title="Morning Walk",
        task_type=TaskType.WALK,
        duration_minutes=30,
        priority=Priority.HIGH,
        scheduled_time=datetime.now().replace(hour=8, minute=0, second=0)
    )
    
    task2 = Task(
        title="Feed Breakfast",
        task_type=TaskType.FEEDING,
        duration_minutes=15,
        priority=Priority.HIGH,
        scheduled_time=datetime.now().replace(hour=7, minute=0, second=0)
    )
    
    task3 = Task(
        title="Evening Walk",
        task_type=TaskType.WALK,
        duration_minutes=30,
        priority=Priority.MEDIUM,
        scheduled_time=datetime.now().replace(hour=18, minute=0, second=0)
    )
    
    task4 = Task(
        title="Medication",
        task_type=TaskType.MEDICATION,
        duration_minutes=10,
        priority=Priority.HIGH,
        scheduled_time=datetime.now().replace(hour=12, minute=0, second=0),
        is_recurring=True,
        recurrence=RecurrencePattern.DAILY
    )
    
    # Add tasks to pets
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task3)
    pet2.add_task(task4)
    
    # Generate plan
    today = datetime.now()
    plan = system.generate_daily_plan(owner.email, today)
    
    print("=" * 50)
    print("PawPal+ Daily Plan Demo")
    print("=" * 50)
    print(f"Owner: {plan['owner']}")
    print(f"Date: {plan['date']}")
    print(f"Total Time: {plan['total_time_minutes']} minutes")
    print(f"Time Available: {plan['time_available']} minutes")
    print("-" * 50)
    print("Scheduled Tasks:")
    for task in plan['scheduled_tasks']:
        print(f"  - {task.title} ({task.task_type.value}) - {task.duration_minutes} min - {task.priority.name}")
    print("-" * 50)
    print(f"Unscheduled Tasks: {plan['unscheduled_tasks']}")
    print(f"Conflicts Detected: {len(plan['conflicts'])}")
    print("=" * 50)
    
    return system


if __name__ == "__main__":
    demo()
