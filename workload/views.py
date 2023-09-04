""" Views for Workload. Displaying, adding and deleting sets of an exercise in a workout session"""
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect
from exercise.models import Exercise
from workout.forms import WorkoutExerciseForm
from workout.models import WorkoutExercise
from .models import Workload
from .forms import WorkloadForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import ProtectedError
from django.core.paginator import Paginator


class WorkloadList(View):
    workout_exercise_form_class = WorkoutExerciseForm
    exercise_set_form_class = WorkloadForm
    weightlifting_template = "weight-lifting.html"
    endurance_template = "endurance.html"
    running_template = "running.html"
    EXERCISE_TYPE_WEIGHTLIFTING = 0
    EXERCISE_TYPE_RUNNING = 1
    EXERCISE_TYPE_ENDURANCE = 2

    def get(self, request, *args, **kwargs):
        # If the user is not logged in, then redirect them to the login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect("accounts/login/")

        workout_exercise_id = kwargs["workout_exercise_id"]

        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        workout_exercise_form = self.workout_exercise_form_class(user_id=request.user.id,
                                                                 instance=workout_exercise, prefix="workout_exercise")

        # Empty form for adding a new set
        exercise_set_form = self.exercise_set_form_class(prefix="exercise_set")

        # Retrieve list of exercise_sets for the template
        exercise_set_list = Workload.objects.filter(
            workout_exercise_id=workout_exercise_id).order_by("id")

        # Retrieve exercise for the template
        exercise = Exercise.objects.get(
            id=workout_exercise.exercise_id)

        return self.__render(request, exercise, workout_exercise_form, exercise_set_form, exercise_set_list)

    def post(self, request, workout_exercise_id, *args, **kwargs):
        # Retrieve workout_exercise using the workout_exercise_id
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)

        # Retrieve the workout_exercise_form from the request object
        workout_exercise_form = self.workout_exercise_form_class(
            request.POST, user_id=request.user.id, instance=workout_exercise, prefix="workout_exercise")
        # Retrieve the execise_set_form from the request oobject
        exercise_set_form = self.exercise_set_form_class(
            request.POST, prefix="exercise_set")
        # Retrieve list of exercise_sets for the template
        exercise_set_list = Workload.objects.filter(
            workout_exercise_id=workout_exercise_id).order_by("id")
        # Retrieve an exercise object for the template
        exercise = Exercise.objects.get(id=workout_exercise.exercise_id)

        # If forms are valid
        if workout_exercise_form.is_valid() and exercise_set_form.is_valid():
            # Save the forms
            return self.__save_forms(request, workout_exercise_form,
                                     exercise_set_form)

        return self.__render(request, exercise, workout_exercise_form,\
            exercise_set_form, exercise_set_list)

    def __save_forms(self, request, workout_exercise_form, exercise_set_form):
        # Save forms
        workout_exercise_form.instance.user = request.user
        workout_exercise_form.save()

        # Create a new object of type ExerciseSet
        exercise_set = Workload.objects.create(owner=request.user,
            workout_exercise_id=workout_exercise_form.instance.id)
        # Copy fields from the form to the created object
        exercise_set.reps = exercise_set_form.instance.reps
        exercise_set.weight = exercise_set_form.instance.weight
        exercise_set.time = exercise_set_form.instance.time
        exercise_set.distance = exercise_set_form.instance.distance
        # Save the object
        exercise_set.save()

        return HttpResponseRedirect(reverse("workload_list", kwargs={"workout_exercise_id": workout_exercise_form.instance.id}))

    def __render(self, request, exercise, workout_exercise_form, exercise_set_form, exercise_set_list):
        # Render a template according to the type and goal of the exercise
        if exercise.exercise_type == self.EXERCISE_TYPE_WEIGHTLIFTING:
            return render(request, self.weightlifting_template, {"exercise": exercise, "workout_exercise_form": workout_exercise_form, "exercise_set_form": exercise_set_form, "exercise_set_list": exercise_set_list})
        elif exercise.exercise_type == self.EXERCISE_TYPE_RUNNING:
            return render(request, self.running_template, {"exercise": exercise, "workout_exercise_form": workout_exercise_form, "exercise_set_form": exercise_set_form, "exercise_set_list": exercise_set_list})
        else:
            return render(request, self.endurance_template, {"exercise": exercise, "workout_exercise_form": workout_exercise_form, "exercise_set_form": exercise_set_form, "exercise_set_list": exercise_set_list})


class DeleteWorkload(View):
    def get(self, request, workout_exercise_id, exercise_set_id, *args, **kwargs):
        exercise_set = Workload.objects.get(id=exercise_set_id, owner=request.user)
        exercise_set.delete()
        return HttpResponseRedirect(reverse('workload_list', kwargs={"workout_exercise_id": workout_exercise_id}))