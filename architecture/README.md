# 🏗️ Salonist Architecture

> A sophisticated multi-agent system for intelligent salon booking management, featuring dynamic service selection, policy management, and automated scheduling.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-1.7+-blue.svg)](https://python-poetry.org/)

This directory contains the comprehensive architecture documentation and visualization for the Salonist project, a sophisticated multi-agent system designed for intelligent salon booking management.

## 📚 Documentation Structure

- 📋 [Booking Workflow](booking_workflow.md) - Detailed technical documentation of the multi-agent booking workflow
- 🎨 [Workflow Diagram](workflow_diagram.png) - Visual representation of the booking process and agent interactions

## 🚀 Quick Start

To regenerate the workflow diagram:

```bash
poetry run python architecture/generate_workflow_diagram.py
```

## 🏢 System Architecture

The Salonist project implements a sophisticated multi-agent architecture to handle the complete booking workflow:

### 1. Service Selection Agent
- **Purpose**: Manages service presentation and selection
- **Data Model**: Integrates with the `Service` database model
- **Key Features**:
  - Dynamic service presentation
  - Service details and pricing
  - Service availability checking

### 2. Policy Selection Agent
- **Purpose**: Handles policy selection for chosen services
- **Data Model**: Works with the `Policy` database model
- **Key Features**:
  - Policy presentation and comparison
  - Coverage amount management
  - Premium calculation

### 3. Date Selection Agent
- **Purpose**: Manages date selection and availability
- **Key Features**:
  - Calendar integration
  - Availability checking
  - Date validation

### 4. Slot Selection Agent
- **Purpose**: Handles time slot selection and booking
- **Key Features**:
  - Real-time slot availability
  - Conflict detection
  - Booking confirmation

### 5. Supervisor Agent
- **Purpose**: Orchestrates the entire conversation flow
- **Key Features**:
  - Context management
  - State transitions
  - Error handling
  - Booking finalization

## 🔄 Workflow

The system follows a structured workflow:
1. User initiates booking request
2. Service Selection Agent presents available services
3. Policy Selection Agent shows relevant policies
4. Date Selection Agent handles date picking
5. Slot Selection Agent manages time slot selection
6. Supervisor Agent finalizes the booking

## 📖 Detailed Documentation

For comprehensive technical details about each component, their interactions, and implementation specifics, please refer to the [Booking Workflow](booking_workflow.md) documentation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 