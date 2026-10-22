# Workout Application API

## Description

A Flask REST API for managing workouts and exercises. The application uses Flask-SQLAlchemy for database operations, Flask-Migrate for database migrations, and Marshmallow for request validation.

## Features

- View all workouts.
- View a single workout and its exercises.
- Create and delete workouts.
- View all exercises.
- View a single exercise.
- Create and delete exercises.
- Add exercises to workouts with sets, repetitions, and duration.
- Validate incoming request data.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite

## Installation

Navigate to the server directory:

```bash
cd server
```

Install the project dependencies:

```bash
pipenv install
```

## Database Setup

Apply the database migrations:

```bash
pipenv run flask --app app db upgrade
```

Seed the database:

```bash
pipenv run python seed.py
```

## Run the Application

Start the development server:

```bash
pipenv run flask --app app run --port 5555
```

The API will be available at:

`http://127.0.0.1:5555`

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Retrieve one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Request Bodies

### Create an Exercise

```json
{
  "name": "Plank",
  "category": "Core",
  "equipment_needed": false
}
```

### Create a Workout

```json
{
  "date": "2026-10-22",
  "duration_minutes": 30,
  "notes": "Full body workout"
}
```

### Add an Exercise to a Workout

```json
{
  "sets": 3,
  "reps": 12,
  "duration_seconds": 60
}
```

The accepted field names for workout exercises should match those implemented in the application.

## License

This project was developed for educational purposes.
