"""Reports that are used by WorkoutList view"""
#pylint: disable=too-few-public-methods

# They are the items that get displayed when the user navigates to 'Workouts'
# They are used in the template workout_list.html to enable displaying the name of the workout
# and providing a link to the workout by using its id.
# Also, the reports store summaries of each exercise in the workout.
# And hold the id of WorkoutExercise, which can be used to provide a link to the WorkoutExercise
# with all of its ExerciseSets
class WorkoutReport:
    """A class for storing reports for each workout. Each report\
        contains a summary of the workout session. It will also \
            accommodate an array of exercise reports, which summarize\
                the workload of each exercise in the workout session,\
                    such as number of sets, repetitions in each set etc."""
    workout_id = 0
    date = None
    name = None
    exercise_reports = None

    def __init__(self) -> None:
        self.date = ""
        self.name = ""
        self.exercise_reports = []


class ExerciseReport:
    """A Summary of the workload of an exercise in a workout"""
    workout_exercise_id = 0
    report = ""