""" Views for Workload. Displaying, adding and deleting sets
     of an exercise in a workout session"""
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
from .models import Endurance
from .forms import EnduranceForm


class EnduranceList(View):
    """List weight-lifting sets in an exercise. Add sets to an workout session"""

    workout_exercise_form_class = WorkoutExerciseForm
    form_class = EnduranceForm
    template = "endurance-list.html"

    def get(self, request, *args, **kwargs):
        """Process GET-Request. Retrieve the requested data
        and pass it to the template"""
        # If the user is not logged in, then redirect them to the login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect("accounts/login/")
        # Retrieve the id of the workout exercise relationship
        workout_exercise_id = kwargs["workout_exercise_id"]
        # Get the object of the relationship
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        # Empty form for adding a new set
        endurance_form = self.form_class()

        # Retrieve list of exercise_sets for the template
        endurance_list = Endurance.objects.filter(
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
                "endurance_form": endurance_form,
                "endurance_list": endurance_list,
            },
        )

    def post(self, request, workout_exercise_id, *args, **kwargs):
        """Process the POST-Request. Validate the posted data and commit to database"""
        # Retrieve workout_exercise using the workout_exercise_id
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        # Retrieve the exercise_set_form from the request object
        endurance_form = self.form_class(request.POST)
        # Retrieve list of exercise_sets for the template
        endurance_list = Endurance.objects.filter(
            workout_exercise_id=workout_exercise_id
        ).order_by("id")
        # Retrieve an exercise object for the template
        exercise = Exercise.objects.get(id=workout_exercise.exercise_id)
        # If the submitted form is valid then save it
        if endurance_form.is_valid():
            return self.__save_form(request, workout_exercise, endurance_form)
        # If the form has errors report them to the user
        if endurance_form.errors:
            messages.add_message(
                request,
                messages.SUCCESS,
                f"{endurance_form.errors.as_text()}",
            )
        # Else render the template over
        return render(
            request,
            self.template,
            {
                "exercise": exercise,
                "workout_exercise": workout_exercise,
                "endurance_form": endurance_form,
                "endurance_list": endurance_list,
            },
        )

    def __save_form(self, request, workout_exercise, endurance_form):
        # Create a new object of type ExerciseSet
        endurance = Endurance.objects.create(
            owner=request.user, workout_exercise_id=workout_exercise.id
        )
        # Copy fields from the form to the created object
        endurance.time = endurance_form.instance.time
        endurance.reps = endurance_form.instance.reps
        # Save the object
        endurance.save()

        return HttpResponseRedirect(
            reverse(
                "endurance_list", kwargs={"workout_exercise_id": workout_exercise.id}
            )
        )


class DeleteEndurance(View):
    """Delete an set of endurance"""

    def get(self, request, workout_exercise_id, exercise_set_id, *args, **kwargs):
        """Process the GET-Request and delete the requested dataset"""
        endurance = Endurance.objects.get(id=exercise_set_id, owner=request.user)
        endurance.delete()
        return HttpResponseRedirect(
            reverse(
                "endurance_list", kwargs={"workout_exercise_id": workout_exercise_id}
            )
        )
