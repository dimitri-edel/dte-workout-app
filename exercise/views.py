""" Views for Exercise """
# pylint: disable=E1101
# pylint: disable=unused-argument
from django.views import View, generic
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .forms import ExerciseForm
from .models import Exercise


class ExerciseList(generic.ListView):
    """List of exercises that belong to the user"""

    model = Exercise
    template_name = "exercise_list.html"
    paginate_by = 5

    def get_queryset(self):
        # Only retrieve datasets related to the user
        return self.model.objects.filter(owner=self.request.user.id)


class CreateExercise(View):
    """View for creating an exercise"""

    # Reference to the form
    exercise_form_class = ExerciseForm
    # Reference to the template
    template_name = "create_exercise.html"

    def get(self, request, *args, **kwargs):
        """Process a GET-Request and return a rendered template"""
        # Check if the user is authenticated, if not redirect them to home page
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        # Instantiate the form
        exercise_form = self.exercise_form_class()
        # Render the specified template
        return render(request, self.template_name, {"exercise_form": exercise_form})

    def post(self, request, *args, **kwargs):
        """Process a POST-Request" for creating an exercise"""
        # Retrieve form from REQUEST
        exercise_form = self.exercise_form_class(request.POST)
        # If the form is valid
        if exercise_form.is_valid():
            # Assign the form to the current user.
            # The instance property of the forms is a reference to
            #  the model class
            # that is being used and allows us to access its properties
            # and methods
            exercise_form.instance.owner = request.user
            # Commit the model object to the database
            exercise_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"A new exercise: '{exercise_form.instance.name}'\
                 has been created   !",
            )
            return HttpResponseRedirect(reverse("exercise_list"))
        # If the form was not valid, render the template.
        # The workout_from will contain the
        # validation messages for the user, which had been generated upon
        # calling the is_valid() method
        return render(request, self.template_name, {"exercise_form": exercise_form})


class EditExercise(View):
    """View for editing an exercise"""

    # Reference to the form
    exercise_form_class = ExerciseForm
    # Reference to the template
    template_name = "edit_exercise.html"

    def get(self, request, *args, **kwargs):
        """Process a GET-Request"""
        exercise_id = kwargs["exercise_id"]
        # Retrieve dataset
        exercise = Exercise.objects.get(id=exercise_id)
        # Store the id of the last object in the session
        request.session["edit_exercise_id"] = exercise_id
        # Instantiate the form
        exercise_form = self.exercise_form_class(instance=exercise)
        # Render the specified template
        return render(request, self.template_name, {"exercise_form": exercise_form})

    def post(self, request, *args, **kwargs):
        """Process a POST-Request"""
        # Retrieve the object using the id stored in session
        edit_exercise = Exercise.objects.get(id=request.session["edit_exercise_id"])
        # Instantiate the form
        exercise_form = self.exercise_form_class(request.POST, instance=edit_exercise)
        # If the form is valid
        if exercise_form.is_valid():
            # Assign the form to the current user.
            # The instance property of the forms is a reference
            # to the model class
            # that is being used and allows us to access its properties
            # and methods
            exercise_form.instance.user = request.user
            # Commit the model object to the database
            exercise_form.save()
            # Let the user know about the successful update
            messages.add_message(
                request,
                messages.SUCCESS,
                f"{exercise_form.instance.name} has been updated!",
            )
            return HttpResponseRedirect(reverse("exercise_list"))
        # If the form was not valid, render the template.
        # The workout_from will contain the validation messages
        # for the user, which had been generated upon calling
        # the is_valid() method
        return render(request, self.template_name, {"exercise_form": exercise_form})


class DeleteExercise(View):
    """Delete an exercise from the list of available exercises"""

    def get(self, request, exercise_id):
        """Process the GET-request for delete"""
        exercise = Exercise.objects.get(id=exercise_id)
        if exercise.owner != request.user:
            # Relay the error message to the user
            messages.add_message(
                request,
                messages.ERROR,
                "This exercise cannot be deleted because \
                you are not the owner!",
            )
            return HttpResponseRedirect(reverse("exercise_list"))

        try:
            exercise.delete()
            messages.add_message(
                request, messages.SUCCESS, f"{exercise.name} has been deleted!"
            )
        except ProtectedError:
            # ProtectedError is raised because if the exercise is used
            # in a workout
            # In the model WorkoutExercise the foreign key to the
            # exercise states on_delete=models.PROTECT
            messages.add_message(
                request,
                messages.ERROR,
                "This exercise cannot be deleted because \
                it is being used in a workout!",
            )

        return HttpResponseRedirect(reverse("exercise_list"))
