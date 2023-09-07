""" Views for Workload. Displaying, adding and deleting sets of an exercise in a workout session"""
# pylint: disable=no-name-in-module
# pylint: disable=no-member
#pylint: disable=unused-argument
from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect
from exercise.models import Exercise
from workout.models import WorkoutExercise
from workout.forms import WorkoutExerciseForm
from .models import WeightLifting
from .forms import WeightLiftingForm


class WeightLiftingList(View):
    """List weight-lifting sets in an exercise. Add sets to an workout session"""
    workout_exercise_form_class = WorkoutExerciseForm
    weight_lifting_form_class = WeightLiftingForm
    weightlifting_template = "weight-lifting-list.html"

    def get(self, request, *args, **kwargs):
        """Process GET-Request. Retrieve the requested data and pass it to the template"""
        print("weight lifting in progress!!!!!!!!!!!")
        # If the user is not logged in, then redirect them to the login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect("accounts/login/")

        workout_exercise_id = kwargs["workout_exercise_id"]

        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        workout_exercise_form = self.workout_exercise_form_class(user_id=request.user.id,
                                                                 instance=workout_exercise, prefix="workout_exercise")

        # Empty form for adding a new set
        weight_lifting_form = self.weight_lifting_form_class(prefix="exercise_set")

        # Retrieve list of exercise_sets for the template
        exercise_set_list = WeightLifting.objects.filter(
            workout_exercise_id=workout_exercise_id).order_by("id")

        # Retrieve exercise for the template
        exercise = Exercise.objects.get(
            id=workout_exercise.exercise_id)

        return render(request, self.weightlifting_template,\
            {"exercise": exercise, "workout_exercise_form": workout_exercise_form,\
                "weight_lifting_form": weight_lifting_form, "exercise_set_list": exercise_set_list})

    def post(self, request, workout_exercise_id, *args, **kwargs):
        """Process the POST-Request. Validate the posted data and commit to database"""
        # Retrieve workout_exercise using the workout_exercise_id
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)

        # Retrieve the workout_exercise_form from the request object
        workout_exercise_form = self.workout_exercise_form_class(
            request.POST, user_id=request.user.id, instance=workout_exercise, prefix="workout_exercise")
        # Retrieve the execise_set_form from the request oobject
        weight_lifting_form = self.weight_lifting_form_class(
            request.POST, prefix="exercise_set")
        # Retrieve list of exercise_sets for the template
        exercise_set_list = WeightLifting.objects.filter(
            workout_exercise_id=workout_exercise_id).order_by("id")
        # Retrieve an exercise object for the template
        exercise = Exercise.objects.get(id=workout_exercise.exercise_id)

        # If forms are valid
        if workout_exercise_form.is_valid() and weight_lifting_form.is_valid():
            # Save the forms
            return self.__save_forms(request, workout_exercise_form,
                                     weight_lifting_form)

        return render(request, self.weightlifting_template,\
            {"exercise": exercise, "workout_exercise_form": workout_exercise_form,\
                "weight_lifting_form": weight_lifting_form, "exercise_set_list": exercise_set_list})

    def __save_forms(self, request, workout_exercise_form, weight_lifting_form):
        # Save forms
        workout_exercise_form.instance.user = request.user
        workout_exercise_form.save()

        # Create a new object of type ExerciseSet
        weight_lifting_set = WeightLifting.objects.create(owner=request.user,
            workout_exercise_id=workout_exercise_form.instance.id)
        # Copy fields from the form to the created object
        weight_lifting_set.reps = weight_lifting_form.instance.reps
        weight_lifting_set.weight = weight_lifting_form.instance.weight
        # Save the object
        weight_lifting_set.save()

        return HttpResponseRedirect(reverse("weight_lifting_list",\
             kwargs={"workout_exercise_id": workout_exercise_form.instance.id}))


class DeleteWeightLifting(View):
    """Delete an set of weight-lifting"""
    def get(self, request, workout_exercise_id, exercise_set_id, *args, **kwargs):
        """Process the GET-Request and delete the requested dataset"""
        exercise_set = WeightLifting.objects.get(id=exercise_set_id, owner=request.user)
        exercise_set.delete()
        return HttpResponseRedirect(reverse('weight_lifting_list',\
            kwargs={"workout_exercise_id": workout_exercise_id}))
