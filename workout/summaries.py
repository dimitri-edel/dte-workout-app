"""Classes for summaries """
#pylint: disable=too-few-public-methods
#pylint: disable=no-name-in-module
from workload.models import Workload

class WorkoutSummary:
    """A class for storing a summary of a workout"""
    # Model object of type Workout
    workout = None
    # Array of objects of type WorkloadReport
    reports = None

    def __init__(self) -> None:        
        self.reports = []


class WorkloadReport:
    """Class for storing summary of a workload """
    # Model object of type WorkoutExercise
    workout_exercise = None
    # Array of string objects that summarize a sets / workloads of one exercise
    # in a workout session
    summaries = []


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
        for workout in self.workouts:
            workout_summary = WorkoutSummary()
            workout_summary.workout = workout
            workout_exercise_list = workout.exercise_list
            for workout_exercise in workout_exercise_list:                
                self.__add_workout_exercise_to_report(workout_exercise, workout_summary)
            self.reports.append(workout_summary)

    def __add_workout_exercise_to_report(self, workout_exercise, workout_summary):
        workload_report = WorkloadReport()
        workload_report.workout_exercise = workout_exercise
        workload_summaries = []
        self.__add_workload_summaries(workout_exercise, workload_summaries)
        workload_report.summaries = workload_summaries
        workout_summary.reports.append(workload_report)

    def __add_workload_summaries(self, workout_exercise, workload_summaries):
        if workout_exercise.exercise.exercise_type == 0: # Weight-Lifting
            self.__get_weightlifting_report(workout_exercise, workload_summaries)
        elif workout_exercise.exercise.exercise_type == 1: # Running
            self.__get_running_report(workout_exercise, workload_summaries)
        elif workout_exercise.exercise.exercise_type == 2: # Endurance
            self.__get_endurance_report(workout_exercise, workload_summaries)

    def __get_weightlifting_report(self, workout_exercise, workload_summaries):
        workloads = Workload.objects.filter(workout_exercise=workout_exercise)
        for workload in workloads:
            workload_summaries.append(f"{workload.reps} x {workload.weight} kg")

    def __get_running_report(self, workout_exercise, workload_summaries):
        workloads = Workload.objects.filter(workout_exercise=workout_exercise)
        for workload in workloads:
            workload_summaries.append(f"{workload.distance} x {workload.time} hours")

    def __get_endurance_report(self, workout_exercise, workload_summaries):
        workloads = Workload.objects.filter(workout_exercise=workout_exercise)
        for workload in workloads:
            workload_summaries.append(f"{workload.reps} x {workload.time} hours")
