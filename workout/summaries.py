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
        # Iterate through the workouts
        for workout in self.workouts:
            # Make a summary for each workout 
            workout_summary = WorkoutSummary()
            # Attach the workout to the summary
            workout_summary.workout = workout
            # Get the list of WorkoutExercise relationships
            # that are related to the given workout
            workout_exercise_list = workout.exercise_list
            # Iterate through the list of relationships
            for workout_exercise in workout_exercise_list:
                self.__add_workout_exercise_to_report(workout_exercise, workout_summary)
            
            # Append the workout summary to the reports
            self.reports.append(workout_summary)

    def __add_workout_exercise_to_report(self, workout_exercise, workout_summary):
        """Attach the instance of the WorkoutExercise Model to a WorkloadReport.\
            Then attach the instance of WorkloadReport to the workout_summary"""
        # Instantiate the workload report
        workload_report = WorkloadReport()
        # Attach the instance or WorkoutExercise to the workload_report
        workload_report.workout_exercise = workout_exercise
        # Create a list for workload summaries
        workload_summaries = []
        # Get the summaries for all the sets in of the exercise (workloads)
        self.__add_workload_summaries(workout_exercise, workload_summaries)

        # Attach the workload summaries to the workload report
        workload_report.summaries = workload_summaries
        # Append the workload report to reports in the workout summary
        workout_summary.reports.append(workload_report)

    def __add_workload_summaries(self, workout_exercise, workload_summaries):
        """Add workload summaries according to the exercise type """
        # If the relationships points to an exercise with exercise type Weight-Lifting
        if workout_exercise.exercise.exercise_type == 0: # Weight-Lifting
            self.__get_weightlifting_report(workout_exercise, workload_summaries)
        # If the relationships points to an exercise with exercise type Running
        elif workout_exercise.exercise.exercise_type == 1: # Running
            self.__get_running_report(workout_exercise, workload_summaries)
        # If the relationships points to an exercise with exercise type Endurance
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
