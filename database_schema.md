# Database Schema - Project Management System

## Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────────────┐    ┌─────────────────────┐
│     stages      │    │         tasks           │    │      projects       │
├─────────────────┤    ├─────────────────────────┤    ├─────────────────────┤
│ - id            │◄───┤ - id                    │    │ - id (pk)           │
│ - name          │    │ - title                 │    │ - name              │
│ (TO_DO,         │    │ - description           │    │ - description       │
│  Done,          │    │ - assignee_id           │    │ - created_at        │
│  Finished)      │    │ - stage_id              │────┤                     │
│ - order_no      │    │ - created_at            │    │                     │
└─────────────────┘    │ - updated_at            │    │                     │
                       └─────────────────────────┘    └─────────────────────┘
```

## Table Definitions

### 1. Projects Table
| Field | Type | Description |
|-------|------|-------------|
| id | Primary Key | Unique identifier for each project |
| name | String | Project name |
| description | Text | Project description |
| created_at | DateTime | When the project was created |

### 2. Tasks Table
| Field | Type | Description |
|-------|------|-------------|
| id | Primary Key | Unique identifier for each task |
| title | String | Task title |
| description | Text | Task description |
| assignee_id | Foreign Key | Reference to user assigned to task |
| stage_id | Foreign Key | Reference to current stage |
| created_at | DateTime | When the task was created |
| updated_at | DateTime | When the task was last updated |

### 3. Stages Table
| Field | Type | Description |
|-------|------|-------------|
| id | Primary Key | Unique identifier for each stage |
| name | String | Stage name (TO_DO, Done, Finished) |
| order_no | Integer | Order/sequence number for stage |

## Relationships

- **Tasks ↔ Stages**: Many-to-One (Many tasks can be in one stage)
- **Tasks ↔ Projects**: Many-to-One (Many tasks belong to one project)
- **Projects ↔ Stages**: No direct relationship (stages are shared across projects)

## Predefined Stage Values
- TO_DO
- Done  
- Finished

This schema represents a typical project management system where:
- Projects contain multiple tasks
- Tasks are assigned to different stages
- Stages have a specific order for workflow progression
