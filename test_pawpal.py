"""
PawPal+ Test Suite
Automated tests for core functionality
"""

import pytest
from datetime import datetime, timedelta
from pawpal_system import (
    PawPalSystem, Owner, Pet, Task,
    Priority, TaskType, RecurrencePattern
)


@pytest.fixture
def sample_system():
    """Create a sample system for testing"""
    system = PawPalSystem()
    owner = Owner("Test User", "test@example.com")
    system.add_owner(owner)
    
    dog = Pet("Buddy", "Dog", "Golden Retriever", 3)
    cat = Pet("Whiskers", "Cat", "Persian", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    return system, owner, dog, cat


class TestTask:
    """Tests for Task class"""
    
    def test_task_creation(self):
        """Test that a task can be created with correct attributes"""
        task = Task(
            title="Morning Walk",
            task_type=TaskType.WALK,
            duration_minutes=30,
            priority=Priority.HIGH
        )
        
        assert task.title == "Morning Walk"
        assert task.task_type == TaskType.WALK
        assert task.duration_minutes == 30
        assert task.priority == Priority.HIGH
        assert task.is_completed is False
        assert task.is_recurring is False
    
    def test_mark_complete(self):
        """Test marking a task as complete"""
        task = Task("Test", TaskType.FEEDING, 10)
        assert task.is_completed is False
        
        task.mark_complete()
        assert task.is_completed is True
    
    def test_recurring_task_generation(self):
        """Test generating next occurrence for recurring tasks"""
        task = Task(
            title="Daily Meds",
            task_type=TaskType.MEDICATION,
            duration_minutes=10,
            scheduled_time=datetime(2026, 3, 14, 8, 0),
            is_recurring=True,
            recurrence=RecurrencePattern.DAILY
        )
        
        next_task = task.get_next_occurrence()
        
        assert next_task is not None
        assert next_task.title == task.title
        assert next_task.scheduled_time == datetime(2026, 3, 15, 8, 0)


class TestPet:
    """Tests for Pet class"""
    
    def test_pet_creation(self):
        """Test pet creation"""
        pet = Pet("Buddy", "Dog", "Golden Retriever", 3)
        
        assert pet.name == "Buddy"
        assert pet.species == "Dog"
        assert pet.breed == "Golden Retriever"
        assert pet.age == 3
        assert len(pet.tasks) == 0
    
    def test_add_task(self):
        """Test adding a task to a pet"""
        pet = Pet("Buddy", "Dog")
        task = Task("Walk", TaskType.WALK, 30)
        
        pet.add_task(task)
        
        assert len(pet.tasks) == 1
        assert task.pet == pet
    
    def test_get_tasks_for_day(self):
        """Test filtering tasks by day"""
        pet = Pet("Buddy", "Dog")
        today = datetime(2026, 3, 14)
        
        task1 = Task("Morning Walk", TaskType.WALK, 30, scheduled_time=today.replace(hour=8))
        task2 = Task("Evening Walk", TaskType.WALK, 30, scheduled_time=today.replace(hour=18))
        task3 = Task("Tomorrow Walk", TaskType.WALK, 30, scheduled_time=today.replace(hour=8) + timedelta(days=1))
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        today_tasks = pet.get_tasks_for_day(today)
        
        assert len(today_tasks) == 2


class TestOwner:
    """Tests for Owner class"""
    
    def test_owner_creation(self):
        """Test owner creation"""
        owner = Owner("John", "john@example.com")
        
        assert owner.name == "John"
        assert owner.email == "john@example.com"
        assert len(owner.pets) == 0
    
    def test_add_pet(self):
        """Test adding a pet to owner"""
        owner = Owner("John", "john@example.com")
        pet = Pet("Buddy", "Dog")
        
        owner.add_pet(pet)
        
        assert len(owner.pets) == 1
        assert pet.owner == owner
    
    def test_get_all_tasks(self):
        """Test getting all tasks across pets"""
        owner = Owner("John", "john@example.com")
        dog = Pet("Buddy", "Dog")
        cat = Pet("Whiskers", "Cat")
        
        dog_task = Task("Walk", TaskType.WALK, 30)
        cat_task = Task("Feed", TaskType.FEEDING, 10)
        
        dog.add_task(dog_task)
        cat.add_task(cat_task)
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        all_tasks = owner.get_all_tasks()
        
        assert len(all_tasks) == 2


class TestPawPalSystem:
    """Tests for PawPalSystem class"""
    
    def test_add_owner(self):
        """Test adding owner to system"""
        system = PawPalSystem()
        owner = Owner("John", "john@example.com")
        
        system.add_owner(owner)
        
        assert len(system.owners) == 1
    
    def test_get_owner_by_email(self):
        """Test finding owner by email"""
        system = PawPalSystem()
        owner = Owner("John", "john@example.com")
        system.add_owner(owner)
        
        found = system.get_owner_by_email("john@example.com")
        
        assert found is not None
        assert found.name == "John"
    
    def test_sort_by_priority(self):
        """Test sorting tasks by priority"""
        system = PawPalSystem()
        
        tasks = [
            Task("Low", TaskType.WALK, 30, Priority.LOW),
            Task("High", TaskType.WALK, 30, Priority.HIGH),
            Task("Medium", TaskType.WALK, 30, Priority.MEDIUM),
        ]
        
        sorted_tasks = system.sort_tasks_by_priority(tasks)
        
        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[1].priority == Priority.MEDIUM
        assert sorted_tasks[2].priority == Priority.LOW
    
    def test_detect_conflicts(self):
        """Test conflict detection"""
        system = PawPalSystem()
        
        task1 = Task("Walk 1", TaskType.WALK, 60, scheduled_time=datetime(2026, 3, 14, 8, 0))
        task2 = Task("Walk 2", TaskType.WALK, 30, scheduled_time=datetime(2026, 3, 14, 8, 30))
        
        conflicts = system.detect_conflicts([task1, task2])
        
        assert len(conflicts) == 1
    
    def test_generate_daily_plan(self):
        """Test daily plan generation"""
        system = PawPalSystem()
        owner = Owner("John", "john@example.com")
        system.add_owner(owner)
        
        dog = Pet("Buddy", "Dog")
        owner.add_pet(dog)
        
        task1 = Task("Walk", TaskType.WALK, 30, Priority.HIGH, scheduled_time=datetime(2026, 3, 14, 8, 0))
        task2 = Task("Feed", TaskType.FEEDING, 15, Priority.HIGH, scheduled_time=datetime(2026, 3, 14, 9, 0))
        dog.add_task(task1)
        dog.add_task(task2)
        
        plan = system.generate_daily_plan("john@example.com", datetime(2026, 3, 14))
        
        assert plan['owner'] == "John"
        assert plan['total_time_minutes'] == 45
        assert len(plan['scheduled_tasks']) == 2
    
    def test_generate_daily_plan_time_constraint(self):
        """Test that time constraints are respected"""
        system = PawPalSystem()
        owner = Owner("John", "john@example.com")
        system.add_owner(owner)
        
        dog = Pet("Buddy", "Dog")
        owner.add_pet(dog)
        
        # Add many tasks across multiple days
        for i in range(10):
            hour = 8 + (i // 2)
            minute = (i % 2) * 30
            task = Task(f"Task {i}", TaskType.WALK, 30, scheduled_time=datetime(2026, 3, 14, hour, minute))
            dog.add_task(task)
        
        # Limit to 60 minutes
        plan = system.generate_daily_plan("john@example.com", datetime(2026, 3, 14), time_available_minutes=60)
        
        assert plan['total_time_minutes'] <= 60
        assert plan['unscheduled_tasks'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
