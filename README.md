# PawPal+ (Module 2 Project)

**PawPal+** is a smart pet care management system that helps pet owners plan and organize care tasks for their furry friends.

## 🎯 Project Overview

- **Course:** AI110 - Foundations of AI Engineering
- **Project:** Module 2 - Show What You Know
- **Due:** Sunday, March 29th at 11:59PM PDT

## 📋 What We Built

PawPal+ is a complete pet care management system with:

- **OOP Design**: Modular Python classes (Owner, Pet, Task, PawPalSystem)
- **Scheduling Algorithm**: Priority-based task scheduling with time constraints
- **Conflict Detection**: Identifies overlapping tasks
- **Recurring Tasks**: Support for daily, weekly, biweekly, monthly tasks
- **Streamlit UI**: Interactive web interface for managing pets and tasks
- **Comprehensive Tests**: 15 pytest test cases covering core functionality

## 🏗️ Architecture

### Core Classes

```
Owner → Pet → Task
   ↓
PawPalSystem (manages all)
```

### Key Features

1. **Owner Management**: Create owners with email and track their pets
2. **Pet Profiles**: Track multiple pets with species, breed, age
3. **Task Management**: Create tasks with duration, priority, type, scheduled time
4. **Smart Scheduling**: Generate daily plans based on priority and time available
5. **Conflict Detection**: Automatically detect overlapping tasks
6. **Recurring Tasks**: Support for daily, weekly, biweekly, monthly patterns

## 🚀 Getting Started

### Setup

```bash
# Clone the repository
git clone https://github.com/OldMack/ai110-module2show-pawpal-starter.git
cd ai110-module2show-pawpal-starter

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# Run Streamlit UI
streamlit run app.py

# Or run CLI demo
python cli_demo.py
```

### Running Tests

```bash
# Run all tests
python -m pytest test_pawpal.py -v

# Run with coverage
python -m pytest test_pawpal.py -v --cov
```

## 📁 Project Structure

```
.
├── app.py              # Streamlit UI (frontend)
├── pawpal_system.py    # Core OOP system (backend logic)
├── cli_demo.py         # Command-line demo script
├── test_pawpal.py      # Pytest test suite (15 tests)
├── UML.md             # System design diagram
├── README.md          # This file
├── requirements.txt    # Python dependencies
└── reflection.md      # AI collaboration reflection
```

## 🧪 Test Results

All 15 tests passing:

- ✅ Task creation and management
- ✅ Pet creation and task assignment  
- ✅ Owner management
- ✅ Priority sorting
- ✅ Conflict detection
- ✅ Daily plan generation
- ✅ Time constraint handling
- ✅ Recurring task generation

## 🎓 Learning Outcomes

- Designed modular system using Python OOP
- Implemented scheduling algorithms
- Created UML diagrams with Mermaid.js
- Built interactive Streamlit UI
- Wrote comprehensive pytest tests
- Documented design decisions

## 👥 Collaboration

This project was completed with AI assistance using iterative prompts for:
- UML diagram generation
- Class structure design
- Algorithm implementation
- Test case development

See `reflection.md` for detailed reflection on AI-human collaboration.
