from django.shortcuts import render, redirect

from diabetes.forms import VitalsForm, PredictionForm

from diabetes.lr_offline import save_record, to_csv, logistic_regression, predict, stat_plots

# Create your views here.
def welcome_action(request):
    return render(request, 'diabetes/welcome.html', {})

def about_action(request):
    return render(request, 'diabetes/about.html', {})

def new_record_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = VitalsForm()
        context['message'] = ''
        return render(request, 'diabetes/newrecord.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = VitalsForm(request.POST)
    context['form'] = form

    

    if form.is_valid():
        patient_info = {}

        patient_info['patient_id'] = int(request.POST.get('patient_id'))
        patient_info['patient_name'] = request.POST.get('patient_name')
        patient_info['age'] = int(request.POST.get('age'))
        patient_info['gender'] = 1 if request.POST.get('gender') == 'True' else 0
        patient_info['polyuria'] = 1 if 'polyuria' in request.POST else 0
        patient_info['polydipsia'] = 1 if 'polydipsia' in request.POST else 0
        patient_info['sudden_weight_loss'] = 1 if 'sudden_weight_loss' in request.POST else 0
        patient_info['weakness'] = 1 if 'weakness' in request.POST else 0
        patient_info['polyphagia'] = 1 if 'polyphagia' in request.POST else 0
        patient_info['genital_thrush'] = 1 if 'genital_thrush' in request.POST else 0
        patient_info['visual_blurring'] = 1 if 'visual_blurring' in request.POST else 0
        patient_info['itching'] = 1 if 'itching' in request.POST else 0
        patient_info['irritability'] = 1 if 'irritability' in request.POST else 0
        patient_info['delayed_healing'] = 1 if 'delayed_healing' in request.POST else 0
        patient_info['partial_paresis'] = 1 if 'polpartial_paresisydipsia' in request.POST else 0
        patient_info['muscle_stiffness'] = 1 if 'muscle_stiffness' in request.POST else 0
        patient_info['alopecia'] = 1 if 'alopecia' in request.POST else 0
        patient_info['obesity'] = 1 if 'obesity' in request.POST else 0
        patient_info['diabetes'] = 1 if request.POST.get('diabetes') == 'True' else 0
        
        save_record(patient_info)
        
        # Create new instance of the form to clear it
        form = VitalsForm()
        context['form'] = form
        context['message'] = "Record saved successfully!"

        # read the database and create a CSV file for model fitting process
        to_csv()

        #model training
        logistic_regression()

    return render(request, 'diabetes/newrecord.html', context)

def predict_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = PredictionForm()
        context['message'] = ''
        return render(request, 'diabetes/predict.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = PredictionForm(request.POST)
    context['form'] = form

    
    if form.is_valid():
        patient_info = {}

        patient_info['age'] = int(request.POST.get('age'))
        patient_info['gender'] = 1 if request.POST.get('gender') == 'True' else 0
        patient_info['polyuria'] = 1 if 'polyuria' in request.POST else 0
        patient_info['polydipsia'] = 1 if 'polydipsia' in request.POST else 0
        patient_info['sudden_weight_loss'] = 1 if 'sudden_weight_loss' in request.POST else 0
        patient_info['weakness'] = 1 if 'weakness' in request.POST else 0
        patient_info['polyphagia'] = 1 if 'polyphagia' in request.POST else 0
        patient_info['genital_thrush'] = 1 if 'genital_thrush' in request.POST else 0
        patient_info['visual_blurring'] = 1 if 'visual_blurring' in request.POST else 0
        patient_info['itching'] = 1 if 'itching' in request.POST else 0
        patient_info['irritability'] = 1 if 'irritability' in request.POST else 0
        patient_info['delayed_healing'] = 1 if 'delayed_healing' in request.POST else 0
        patient_info['partial_paresis'] = 1 if 'polpartial_paresisydipsia' in request.POST else 0
        patient_info['muscle_stiffness'] = 1 if 'muscle_stiffness' in request.POST else 0
        patient_info['alopecia'] = 1 if 'alopecia' in request.POST else 0
        patient_info['obesity'] = 1 if 'obesity' in request.POST else 0

        y_predict = predict(patient_info)[0]

        context['form'] = form
        context['message'] = "no potential diabetes" if y_predict == 0 else "potential diabetes"

    return render(request, 'diabetes/predict.html', context)

def statistics_action(request):
    stat_plots()
    return render(request, 'diabetes/statistics.html', {})