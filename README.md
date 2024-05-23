# Task Board Application

This is a simple task management application built with Flask and SQLAlchemy. The application allows users to create task lists, add tasks to lists, update tasks, delete tasks and lists, and move tasks between lists.

## Features

- Create, retrieve, update, and delete task lists.
- Create, retrieve, update, and delete tasks within a list.
- Update tasks and move tasks between lists.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- pytest (for testing)

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/taskboard.git
    cd taskboard
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

The application should now be running on `http://127.0.0.1:5000`.

## API Endpoints

### List Endpoints

- `GET /lists` - Retrieve all lists.
- `POST /lists` - Create a new list. JSON payload should include `name`.

### Task Endpoints

- `POST /lists/<list_id>/tasks` - Create a new task in a list. JSON payload should include `name` and `description`.
- `PUT /tasks/<task_id>` - Update an existing task. JSON payload should include `name` and `description`.
- `DELETE /tasks/<task_id>` - Delete an existing list.
- `DELETE /tasks/<task_id>` - Delete an existing task.
- `PUT /tasks/<task_id>/move` - Move a task to a different list. JSON payload should include `list_id`.


### Example Requests

- Create a new list:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "New List"}' http://127.0.0.1:5000/lists
    ```

- Create a new task in a list:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "New Task", "description": "Task description"}' http://127.0.0.1:5000/lists/1/tasks
    ```

- Move a task to a different list:

    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"list_id": 2}' http://127.0.0.1:5000/tasks/1/move
    ```

- Update a task:

    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{'name': 'Updated Task', 'description': 'Updated description'}' http://127.0.0.1:5000/tasks/1
    ```

Alternatively, use Postman to test a running application.

## Running Tests

To run the tests, you need to have `pytest` installed. You can install it via pip:

```bash
pip install pytest
```

Run the tests using the following command:

```bash
pytest
```

The tests cover the following scenarios:

* Retrieving all lists.

* Creating a task in a list.

* Updating a task.

* Deleting a task.

* Deleting a list.

* Moving a task to a different list.

## Docker Setup and Instructions

### Prerequisites

Make sure you have the following installed on your machine:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Build Docker Image


This command builds the Docker image for your Flask application based on the Dockerfile.

```bash
docker-compose build
```

### Start Docker Containers

This command starts the application using Docker Compose. It will create and start the defined services.

```bash
docker-compose up
```

### Access the Application:

Once the containers are up and running, you can access the application in your web browser at http://localhost:5000.