# PawPal+ System Design

## UML Class Diagram

```mermaid
classDiagram
    class Owner {
        +str name
        +str email
        +List[Pet] pets
        +List[Task] assigned_tasks
        +add_pet(pet: Pet)
        +get_all_tasks()
    }
    
    class Pet {
        +str name
        +str species
        +str breed
        +int age
        +Owner owner
        +List[Task] tasks
        +add_task(task: Task)
        +get_tasks_for_day(date)
    }
    
    class Task {
        +str title
        +str description
        +int duration_minutes
        +Priority priority
        +TaskType task_type
        +datetime scheduled_time
        +Pet pet
        +bool is_completed
        +bool is_recurring
        +RecurrencePattern recurrence
        +mark_complete()
        +get_next_occurrence()
    }
    
    class Priority {
        <<enumeration>>
        HIGH
        MEDIUM
        LOW
    }
    
    class TaskType {
        <<enumeration>>
        FEEDING
        WALK
        MEDICATION
        GROOMING
        ENRICHMENT
        APPOINTMENT
    }
    
    class RecurrencePattern {
        <<enumeration>>
        DAILY
        WEEKLY
        BIWEEKLY
        MONTHLY
    }
    
    class PawPalSystem {
        +List[Owner] owners
        +add_owner(owner: Owner)
        +get_owner_by_email(email)
        +generate_daily_plan(owner, date, time_available)
        +detect_conflicts(tasks)
        +sort_tasks_by_priority(tasks)
    }
    
    Owner "1" -- "*" Pet : owns
    Pet "1" -- "*" Task : has
    Task "*" -- "1" Pet : for
    PawPalSystem "1" -- "*" Owner : manages
    PawPalSystem ..> Task : uses for planning
```

## Key Design Decisions

1. **Owner-Pet-Task Relationship**: Owner has multiple Pets, each Pet has multiple Tasks
2. **Task Properties**: duration_minutes, priority, task_type, scheduled_time
3. **Recurring Tasks**: Support for daily, weekly, biweekly, monthly patterns
4. **Scheduling Algorithm**: Sort by priority, detect conflicts, fit within time constraints

## Core Classes to Implement

1. `Owner` - Pet owner with contact info and assigned tasks
2. `Pet` - Pet with species, breed, age and associated tasks  
3. `Task` - Individual care task with scheduling info
4. `PawPalSystem` - Main system for managing owners, pets, and generating plans
5. Enums: `Priority`, `TaskType`, `RecurrencePattern`
