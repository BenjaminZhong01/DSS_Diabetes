from django.shortcuts import render, redirect

from diabetes.forms import VitalsForm

# Create your views here.
def home_action(request):
    return render(request, 'diabetes/base.html', {})

def about_action(request):
    return render(request, 'diabetes/about.html', {})

def new_record_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = VitalsForm()
        return render(request, 'diabetes/newrecord.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = VitalsForm(request.POST)
    context['form'] = form

    

    if form.is_valid():
        # TODO: Save form data to database
        # form.save()
        
        # Create new instance of the form to clear it
        form = VitalsForm()
        context['form'] = form
        context['message'] = "Record saved successfully!"


    return render(request, 'diabetes/newrecord.html', context)