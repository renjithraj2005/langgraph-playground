# LangGraph Playground

A Flask application that demonstrates various LangGraph workflows for conversational AI applications. Built with Flask, LangChain, and Claude AI.

## Features

- Search workflow using LangGraph and Claude
- Booking assistant using LangGraph state management
- RESTful API with Flask-RESTX
- Documentation with Swagger UI

## Getting Started

### Prerequisites

- Python 3.10+
- Poetry

### Installation

```bash
# Clone the repository
git clone https://github.com/renjithraj2005/langgraph-playground.git
cd langgraph-playground

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running the application

```bash
# Run the application
make run
```

Visit `http://localhost:8000/docs` to view the API documentation.

## API Endpoints

- `/api/search` - Search endpoint that utilizes Claude AI and Tavily search
- `/api/booking` - Booking assistant powered by Claude AI

## License

MIT 