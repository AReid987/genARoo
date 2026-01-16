# Roo Code Persistence API

A FastAPI-based database persistence layer for Roo Code application.

## Features

- **Project Management**: Create, read, update, and delete projects
- **Epic Management**: Manage epics within projects
- **Task Management**: Handle individual tasks within epics
- **Agent State Management**: Track AI agent states and context
- **RESTful API**: Clean, well-documented REST endpoints
- **Data Validation**: Pydantic schemas for request/response validation
- **Database ORM**: SQLAlchemy for robust database operations
- **Automatic Documentation**: Swagger UI and ReDoc integration
- **Comprehensive Testing**: Full test suite with pytest

## API Endpoints

### Projects
- `POST /api/v1/projects/` - Create a new project
- `GET /api/v1/projects/` - List projects with pagination and filtering
- `GET /api/v1/projects/{id}` - Get a specific project
- `GET /api/v1/projects/{id}/with-epics` - Get project with associated epics
- `PUT /api/v1/projects/{id}` - Update a project
- `DELETE /api/v1/projects/{id}` - Delete a project

### Epics
- `POST /api/v1/epics/` - Create a new epic
- `GET /api/v1/epics/` - List epics with pagination and filtering
- `GET /api/v1/epics/{id}` - Get a specific epic
- `GET /api/v1/epics/{id}/with-tasks` - Get epic with associated tasks
- `PUT /api/v1/epics/{id}` - Update an epic
- `DELETE /api/v1/epics/{id}` - Delete an epic

### Tasks
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/` - List tasks with pagination and filtering
- `GET /api/v1/tasks/{id}` - Get a specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `PATCH /api/v1/tasks/{id}/status` - Update task status only
- `PATCH /api/v1/tasks/{id}/assignee` - Update task assignee only
- `DELETE /api/v1/tasks/{id}` - Delete a task

### Agent States
- `POST /api/v1/agent-states/` - Create a new agent state
- `GET /api/v1/agent-states/` - List agent states
- `GET /api/v1/agent-states/{agent_id}` - Get agent state by agent ID
- `PUT /api/v1/agent-states/{agent_id}` - Update agent state
- `PATCH /api/v1/agent-states/{agent_id}/activity` - Update last activity
- `DELETE /api/v1/agent-states/{agent_id}` - Delete agent state

### System
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Data Models

### Project
- `id`: Unique identifier
- `name`: Project name
- `description`: Project description
- `status`: Project status (planning, active, on_hold, completed, cancelled)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Epic
- `id`: Unique identifier
- `title`: Epic title
- `description`: Epic description
- `status`: Epic status (backlog, planned, in_progress, review, done, cancelled)
- `project_id`: Associated project ID
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Task
- `id`: Unique identifier
- `title`: Task title
- `description`: Task description
- `status`: Task status (todo, in_progress, review, done, blocked, cancelled)
- `priority`: Task priority (low, medium, high, urgent)
- `complexity`: Complexity score (1-10)
- `epic_id`: Associated epic ID
- `assignee`: Task assignee
- `estimated_hours`: Estimated hours
- `actual_hours`: Actual hours
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `completed_at`: Completion timestamp

### Agent State
- `id`: Unique identifier
- `agent_id`: Unique agent identifier
- `current_task_id`: Current task ID
- `current_project_id`: Current project ID
- `context_data`: Agent context data (JSON)
- `last_activity`: Last activity timestamp
- `is_active`: Whether agent is active
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Development

### Setup
```bash
# Install dependencies
pdm install

# Initialize database
pdm run init-db
```

### Running
```bash
# Development mode
pdm run uvicorn app.main:app --reload

# Or using the npm script
pnpm dev
```

### Testing
```bash
# Run tests
pdm run pytest

# Run with coverage
pdm run pytest --cov=app --cov-report=html
```

### Code Quality
```bash
# Format code
pdm run black .
pdm run isort .

# Lint code
pdm run flake8 .

# Type checking
pdm run mypy app
```

## Environment Variables

- `DATABASE_URL`: Database connection URL (default: `sqlite:///./roo_code_data.db`)
- `DEBUG`: Enable debug mode (default: `false`)

## Database

The application uses SQLite by default for simplicity. The database file will be created as `roo_code_data.db` in the application directory.

For production, you can configure a different database by setting the `DATABASE_URL` environment variable:

```bash
# PostgreSQL example
DATABASE_URL=postgresql://user:password@localhost/roo_code

# MySQL example  
DATABASE_URL=mysql://user:password@localhost/roo_code
```
