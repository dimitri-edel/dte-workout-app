""" Home page view """
from django.views import View
from django.shortcuts import render

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