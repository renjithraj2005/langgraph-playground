# Salonist Architecture

This directory contains the architecture documentation and visualization for the Salonist project.

## Contents

- [Booking Workflow](booking_workflow.md) - Detailed documentation of the multi-agent booking workflow
- [Workflow Diagram](workflow_diagram.png) - Visual representation of the booking process

## Quick Start

To regenerate the workflow diagram:

```bash
poetry run python architecture/generate_workflow_diagram.py
```

## Architecture Overview

The Salonist project uses a multi-agent architecture to handle the booking workflow:

1. **Service Selection Agent**
   - Handles service presentation and selection
   - Uses the `Service` model from the database

2. **Policy Selection Agent**
   - Manages policy selection for chosen services
   - Uses the `Policy` model from the database

3. **Date Selection Agent**
   - Handles date selection and availability

4. **Slot Selection Agent**
   - Manages time slot selection and booking

5. **Supervisor Agent**
   - Orchestrates the conversation flow
   - Maintains context and handles transitions

For detailed information about each component and their interactions, please refer to the [Booking Workflow](booking_workflow.md) documentation. 