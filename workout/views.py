""" Views for workout app"""
#pylint: disable=no-name-in-module
#pylint: disable=too-few-public-methods
#pylint: disable=no-member
#pylint: disable=unused-argument
from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Workout, WorkoutExercise
from .forms import WorkoutForm, WorkoutExerciseForm
from .reports import WorkoutReport, ExerciseReport


class StartWorkout(View):
    """View for adding a new Workout session"""

    # Reference to the form class for the model class Workout
    workout_form_class = WorkoutForm
    # Reference to the form class for the model class ExerciseSet
    workout_exercise_form_class = WorkoutExerciseForm
    # Reference to the template for this view
    template_name = "start_workout.html"
    # Process a GET-Request

    def get(self, request, *args, **kwargs):
        """Process the GET-Request"""
        # If the user is not logged in, then redirect them to the login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect("accounts/login/")
        # Instantiate the forms.
        # The prefix is mandatory when using several forms in the same view.
        # When initializing a form, using the data in the POST-request object, prefix
        # helps setting the forms apart, as you can see in the post method below.
        workout_form = self.workout_form_class(prefix="workout")
        # Render the dedicated template
        return render(request, self.template_name,{"workout_form": workout_form})

    def post(self, request, *args, **kwargs):
        """Process the POST-Request"""
        # Instantiate the forms.
        workout_form = self.workout_form_class(request.POST, prefix="workout")
        # If both forms are valid
        if workout_form.is_valid():
            # Assign the form to the current user.
            # The instance property of the forms is a reference to the model class
            # that is being used and allows us to access its properties and methods
            workout_form.instance.user = request.user
            # Commit the model object to the database
            workout_form.save()            

            return HttpResponseRedirect(
                reverse("edit_workout", kwargs={'workout_id': workout_form.instance.id}))

        # If the form was not valid, render the template. The workout_from will contain 
        # the validation messages for the user, which had been generated upon calling the 
        # is_valid() method
        return render(request, self.template_name, {"workout_form": workout_form})



class EditWorkout(View):
    """class for editing the list of exercises that the workout session is comprised of"""

    # Reference to the name of the form class for the model class Workout
    workout_form_class = WorkoutForm
    # Reference to the name of the form class for the model class WorkoutExercise
    workout_exercise_form_class = WorkoutExerciseForm

    # Reference to the template for this view
    template_name = "edit_workout.html"
    # Process a GET-Request

    def get(self, request, *args, **kwargs):#
        """Process the GET-Request"""
        # If the user is not logged in, then redirect them to the login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect("accounts/login/")

        # Pull the workout.id from kwargs
        workout_id = kwargs['workout_id']
        # Instantiate the forms.
        # The prefix is mandatory whhen using several forms in the same view.
        # When initializing a form, using the data in the POST-request object, prefix
        # helps setting the forms apart, as you can see in the post method below.
        workout = Workout.objects.get(id=workout_id)
        # Create form for the workout object
        workout_form = self.workout_form_class(
            instance=workout, prefix="workout")

        workout_exercise_list = WorkoutExercise.objects.filter(
            workout_id=workout.id)
        # Create a form for the last WrokoutExercise object
        workout_exercise_form = self.workout_exercise_form_class(
            user_id=request.user.id, prefix="workout_exercise")

        # Render the dedicated template
        return render(
            request, self.template_name, {"workout_form": workout_form,
                                          "workout_exercise_list": workout_exercise_list,
                                          "workout_exercise_form": workout_exercise_form})

    def post(self, request, workout_id, *args, **kwargs):
        """Process a POST-Request"""
        # @parameter : id = workout_id
        # Get the workout using the id parameter
        workout = Workout.objects.get(id=workout_id)
        # Instantiate the forms.
        workout_form = self.workout_form_class(
            request.POST, prefix="workout", instance=workout)

        workout_exercise_form = self.workout_exercise_form_class(
            request.POST, user_id=request.user.id, prefix="workout_exercise")
        # save the forms and render a template
        return self.__save_forms(request, workout_form, workout_exercise_form)

    def __save_forms(self, request, workout_form, workout_exercise_form):
        """Save both forms and render a response"""
        if workout_form.is_valid():
            # Assign the form to the current user.
            # The instance property of the forms is a reference to the model class
            # that is being used and allows us to access its properties and methods
            workout_form.instance.user = request.user
            # Commit the model object to the database
            workout_form.save()

        if workout_exercise_form.is_valid():
            workout_exercise_form.instance.workout_id = workout_form.instance.id
            workout_exercise = WorkoutExercise.objects.create(owner=request.user,
            workout_id=workout_form.instance.id,\
                exercise_id=workout_exercise_form.instance.exercise_id)
            workout_exercise.exercise_id = workout_exercise_form.instance.exercise_id
            workout_exercise.save()

        return HttpResponseRedirect(reverse('edit_workout',\
            kwargs={'workout_id': workout_form.instance.id}))


class DeleteWorkoutExercise(View):
    """Remove an exercise from a workout session"""
    def get(self, request, workout_exercise_id, workout_id, *args, **kwargs):
        """Process a GET-Request to remove an exercise from a workout session"""
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        # Only allow owners of the workout to remove exercises from the list
        if workout_exercise.owner == request.user:
            workout_exercise.delete()
        return HttpResponseRedirect(reverse('edit_workout', kwargs={'workout_id': workout_id}))


class WorkoutList(View):
    """List of workout sessions"""

    model = Workout
    template_name = "workout_list.html"
    paginate_by = 2
    # Constants for exercise.type
    WEIGHTLIFTING = 0
    RUNNING = 1
    ENDURANCE = 2

    def get(self, request, *args, **kwargs):
        """Process GET-Request"""
        # If the user is not logged in, then redirect them to the login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect("accounts/login/")

        # Only retrieve datasets related to the user
        self.model.objects.filter(user_id=self.request.user.id)
        # Generate Roports
        reports = self.__generate_reports()
        # Create paginator and load it with reports
        paginator = Paginator(reports, self.paginate_by)
        # Retrieve page number from the GET-Request-object
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
        }
        return render(request, self.template_name, context=context)

    # Create Reports

    def __generate_reports(self):
        reports = []
        workout_list = self.model.objects.filter(user_id=self.request.user.id)
        for workout in workout_list:
            # Create w wokrout report for each workout
            workout_exercises = WorkoutExercise.objects.filter(
                workout_id=workout.id)
            report = WorkoutReport()
            report.workout_id = workout.id
            report.date = workout.date
            report.name = workout.name

            for workout_exercise in workout_exercises:
                # Create an exercise report for each exercise
                # and attach it to the workout report
                exercise_report = ExerciseReport()
                exercise_report.workout_exercise_id = workout_exercise.id
                # Now attach the exercise type to the report in form of a string
                if workout_exercise.exercise.exercise_type == self.WEIGHTLIFTING:
                    exercise_report.exercise_type = "WEIGHTLIFTING"
                elif workout_exercise.exercise.exercise_type == self.RUNNING:
                    exercise_report.exercise_type = "RUNNING"
                else:
                    exercise_report.exercise_type = "ENDURANCE"
                exercise_report.report += f"{workout_exercise.exercise.name}:"
                # exercise_report.report += self.__generate_report(
                #     workout_exercise)
                report.exercise_reports.append(exercise_report)

            reports.append(report)
        return reports


class DeleteWorkout(View):
    """Delete a workout session"""
    def get(self, request, workout_id, *args, **kwargs):
        """Process a GET-Request for deleting a Workout"""
        workout = Workout.objects.get(id=workout_id)
        if workout.user == request.user:
            workout.delete()
        return HttpResponseRedirect(reverse('workout_list'))
