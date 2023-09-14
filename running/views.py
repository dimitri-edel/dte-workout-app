""" Views for Workload. Displaying, adding and deleting sets of an exercise in a workout session"""
# pylint: disable=no-name-in-module
# pylint: disable=no-member
# pylint: disable=unused-argument
from django.shortcuts import render, reverse
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from exercise.models import Exercise
from workout.models import WorkoutExercise
from workout.forms import WorkoutExerciseForm
from .models import Running
from .forms import RunningForm


class RunningList(View):
    """List weight-lifting sets in an exercise. Add sets to an workout session"""

    workout_exercise_form_class = WorkoutExerciseForm
    running_form_class = RunningForm
    template = "running-list.html"

    def get(self, request, *args, **kwargs):
        """Process GET-Request. Retrieve the requested data and pass it to the template"""
        print("weight lifting in progress!!!!!!!!!!!")
        # If the user is not logged in, then redirect them to the login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect("accounts/login/")

        workout_exercise_id = kwargs["workout_exercise_id"]

        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)

        # Empty form for adding a new set
        running_form = self.running_form_class()

        # Retrieve list of exercise_sets for the template
        running_list = Running.objects.filter(
            workout_exercise_id=workout_exercise_id
        ).order_by("id")

        # Retrieve exercise for the template
        exercise = Exercise.objects.get(id=workout_exercise.exercise_id)

        return render(
            request,
            self.template,
            {
                "exercise": exercise,
                "workout_exercise": workout_exercise,
                "running_form": running_form,
                "running_list": running_list,
            },
        )

    def post(self, request, workout_exercise_id, *args, **kwargs):
        """Process the POST-Request. Validate the posted data and commit to database"""
        # Retrieve workout_exercise using the workout_exercise_id
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)

        # Retrieve the execise_set_form from the request oobject
        running_form = self.running_form_class(request.POST)
        # Retrieve list of exercise_sets for the template
        running_list = Running.objects.filter(
            workout_exercise_id=workout_exercise_id
        ).order_by("id")
        # Retrieve an exercise object for the template
        exercise = Exercise.objects.get(id=workout_exercise.exercise_id)
        # If the form is valid save it
        if running_form.is_valid():
            return self.__save_form(request, workout_exercise, running_form)

        return render(
            request,
            self.template,
            {
                "exercise": exercise,
                "workout_exercise": workout_exercise,
                "running_form": running_form,
                "running_list": running_list,
            },
        )

    def __save_form(self, request, workout_exercise, running_form):
        # Create a new object of type ExerciseSet
        running = Running.objects.create(
            owner=request.user, workout_exercise_id=workout_exercise.id
        )
        # Copy fields from the form to the created object
        running.time = running_form.instance.time
        running.distance = running_form.instance.distance
        # Save the object
        running.save()

        return HttpResponseRedirect(
            reverse("running_list", kwargs={"workout_exercise_id": workout_exercise.id})
        )


class DeleteRunning(View):
    """Delete an set of running"""

    def get(self, request, workout_exercise_id, exercise_set_id, *args, **kwargs):
        """Process the GET-Request and delete the requested dataset"""
        running = Running.objects.get(id=exercise_set_id, owner=request.user)
        running.delete()
        return HttpResponseRedirect(
            reverse("running_list", kwargs={"workout_exercise_id": workout_exercise_id})
        )
