""" Views for Exercise """
#pylint: disable=no-name-in-module
from django.views import View, generic
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .forms import ExerciseForm
from .models import Exercise

# Create your views here.
class HomePage(View):
    """View for the home page"""
    # View for the home page
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        """ get the template for homepage """
        # Check if the user belongs in a group and redirect them if they do
        # if request.user.groups.exists():
        #     return redirect_user_to_goup(request=request)

        return render(request, self.template_name)

class ExerciseList(generic.ListView):
    """ List of exercises that belong to the user"""
    model = Exercise    
    template_name = "exercise_list.html"
    paginate_by = 5

    def get_queryset(self):
        # Only retrieve datasets related to the user
        return self.model.objects.filter(user_id=self.request.user.id)


class EditExercise(View):
    """ View for editting an exercise """
    # Reference to the form
    exercise_form_class = ExerciseForm
    # Reference to the template
    template_name = "edit_exercise.html"

    def get(self, request, *args, **kwargs):
        """ Process a GET-Request"""        
        exercise_id = kwargs["exercise_id"]
        # Retrieve dataset
        exercise = Exercise.objects.get(id=exercise_id)        
        # Store the id of the last object in the session
        request.session["edit_exercise_id"] = exercise_id
        # Instanciate the form
        exercise_form = self.exercise_form_class(instance=exercise)
        # Render the specified template
        return render(request, self.template_name, {"exercise_form": exercise_form})

    def post(self, request,  *args, **kwargs):
        """Process a POST-Request"""
        # Retrieve the object using the id stored in session
        edit_exercise = Exercise.objects.get(
            id=request.session["edit_exercise_id"])
        # Instanciate the form
        exercise_form = self.exercise_form_class(
            request.POST, instance=edit_exercise)
        # If the form is valid
        if exercise_form.is_valid():
            # Assign the form to the current user.
            # The instance property of the forms is a reference to the model class
            # that is being used and allows us to access its properties and methods
            exercise_form.instance.user = request.user
            # Commit the model object to the database
            exercise_form.save()

            return HttpResponseRedirect(reverse("edit_exercise_list"))
        # If the form was not valid, render the template. The workout_from will contain the validation
        # messages for the user, which had been generated upon calling the is_valid() method
        return render(request, self.template_name, {"exercise_form": exercise_form})