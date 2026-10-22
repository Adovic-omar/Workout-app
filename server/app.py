from flask import Flask, jsonify, request
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


def get_request_data():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None

    return data


@app.route("/")
def home():
    return jsonify({
        "message": "Workout Application API is running."
    }), 200


# -------------------- WORKOUT ROUTES --------------------

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = get_request_data()

    if data is None:
        return jsonify({
            "error": "Request body must contain a valid JSON object."
        }), 400

    try:
        validated_data = workout_schema.load(data)
        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database constraint violation."}), 400


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    db.session.delete(workout)
    db.session.commit()

    return "", 204


# -------------------- EXERCISE ROUTES --------------------

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = get_request_data()

    if data is None:
        return jsonify({
            "error": "Request body must contain a valid JSON object."
        }), 400

    try:
        validated_data = exercise_schema.load(data)
        exercise = Exercise(**validated_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "An exercise with this name may already exist."
        }), 400


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    db.session.delete(exercise)
    db.session.commit()

    return "", 204


# -------------------- WORKOUT EXERCISE ROUTE --------------------

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    data = get_request_data()

    if data is None:
        return jsonify({
            "error": "Request body must contain a valid JSON object."
        }), 400

    try:
        validated_data = workout_exercise_schema.load(data)

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **validated_data
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify({
            "id": workout_exercise.id,
            "workout_id": workout_exercise.workout_id,
            "exercise_id": workout_exercise.exercise_id,
            "reps": workout_exercise.reps,
            "sets": workout_exercise.sets,
            "duration_seconds": workout_exercise.duration_seconds,
            "exercise": exercise_schema.dump(exercise),
        }), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "This exercise may already be in the workout, or the data violates a database constraint."
        }), 400


if __name__ == "__main__":
    app.run(debug=True, port=5555)
