from datetime import date, timedelta

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():
    # Clear existing sample data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create exercises
    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    db.session.add_all([pushups, squats, running])
    db.session.commit()

    # Create workouts
    workout1 = Workout(
        date=date.today() - timedelta(days=2),
        duration_minutes=30,
        notes="Upper body workout"
    )

    workout2 = Workout(
        date=date.today() - timedelta(days=1),
        duration_minutes=45,
        notes="Cardio and lower body workout"
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    # Connect exercises to workouts
    db.session.add_all([
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=pushups.id,
            reps=12,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=squats.id,
            reps=15,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=running.id,
            duration_seconds=1800
        )
    ])

    db.session.commit()

    print("Database seeded successfully!")
