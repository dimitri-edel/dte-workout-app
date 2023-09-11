"""Classes for summaries """
#pylint: disable=too-few-public-methods
#pylint: disable=no-name-in-module
from weight_lifting.models import WeightLifting
from running.models import Running
from endurance.models import Endurance

class WorkoutSummary:
    """A class for storing a summary of a workout"""
    workout = None
    """Model object of type Workout"""
    exercise_reports = None
    """Array of objects of type ExerciseReport"""

    def __init__(self, workout):
        self.exercise_reports = []
        self.workout = workout
        self.__get_exercise_reports()

    def __get_exercise_reports(self):
        for workout_exercise in self.workout.exercise_list:
            report = ExerciseReport(workout_exercise)
            self.exercise_reports.append(report)


class ExerciseReport:
    """Class for storing summary of a workload """
    workout_exercise = None
    """Model object of type WorkoutExercise"""
    summaries = None
    """Array of string objects that summarize a sets / workloads of one exercise
    in a workout session"""

    def __init__(self, workout_exercise) -> None:
        self.workout_exercise = workout_exercise
        self.summaries = []
        self.__get_summaries()

    def __get_summaries(self):
        """Add workload summaries according to the exercise type """
        # If the relationships points to an exercise with exercise type Weight-Lifting
        if self.workout_exercise.exercise.exercise_type == 0: # Weight-Lifting
            self.__get_weightlifting_reports()
        # If the relationships points to an exercise with exercise type Running
        elif self.workout_exercise.exercise.exercise_type == 1: # Running
            self.__get_running_reports()
        # If the relationships points to an exercise with exercise type Endurance
        elif self.workout_exercise.exercise.exercise_type == 2: # Endurance
            self.__get_endurance_reports()

    def __get_weightlifting_reports(self):
        weight_lifting_list = WeightLifting.objects.filter(workout_exercise=self.workout_exercise)
        for weight_lifting in weight_lifting_list:
            self.summaries.append(f"{weight_lifting.reps} x {weight_lifting.weight} kg")

    def __get_running_reports(self):
        running_list = Running.objects.filter(workout_exercise=self.workout_exercise)
        for running in running_list:
            self.summaries.append(f"{running.distance} km in {running.time} hours")

    def __get_endurance_reports(self):
        endurance_list = Endurance.objects.filter(workout_exercise=self.workout_exercise)
        for endurance in endurance_list:
            self.summaries.append(f"{endurance.reps} reps in {endurance.time} hours")


class Summarizer:
    """A class that assembles summaries for the WorkoutList"""
    def __init__(self, workouts):
        self.workouts = workouts
        self.reports = []

    def get_reports(self):
        """The main method that assembles and returns the reports"""
        self.__add_workouts_to_reports()
        return self.reports

    def __add_workouts_to_reports(self):
        # Iterate through the workouts
        for workout in self.workouts:
            # Make a summary for each workout
            workout_summary = WorkoutSummary(workout)            
            # Append the workout summary to the reports
            self.reports.append(workout_summary)
