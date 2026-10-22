from datetime import date

from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    equipment_needed = fields.Bool(required=True)

    @validates_schema
    def validate_exercise(self, data, **kwargs):
        if not data.get("name", "").strip():
            raise ValidationError(
                {"name": ["Name cannot be empty or whitespace."]}
            )

        if not data.get("category", "").strip():
            raise ValidationError(
                {"category": ["Category cannot be empty or whitespace."]}
            )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    exercise = fields.Nested(
        ExerciseSchema,
        only=("id", "name", "category", "equipment_needed"),
        dump_only=True
    )

    @validates_schema
    def validate_exercise_details(self, data, **kwargs):
        if not any(
            data.get(field) is not None
            for field in ("reps", "sets", "duration_seconds")
        ):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.Str(allow_none=True, load_default=None)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )

    @validates_schema
    def validate_workout_date(self, data, **kwargs):
        workout_date = data.get("date")

        if workout_date and workout_date > date.today():
            raise ValidationError(
                {"date": ["Workout date cannot be in the future."]}
            )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
