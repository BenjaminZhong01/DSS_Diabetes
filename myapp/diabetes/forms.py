from django import forms

class VitalsForm(forms.Form):
    patient_id = forms.IntegerField(label='Patient ID')
    patient_name = forms.CharField(max_length = 20, label='Patient Name')
    age = forms.IntegerField(label='Age')
    gender = forms.BooleanField(label='Gender', required=False, widget=forms.Select(choices=[(True, 'Male'), (False, 'Female')]))
    polyuria = forms.BooleanField(label='Polyuria', required=False)
    polydipsia = forms.BooleanField(label='Polydipsia', required=False)
    sudden_weight_loss = forms.BooleanField(label='Sudden weight loss', required=False)
    weakness = forms.BooleanField(label='Weakness', required=False)
    polyphagia = forms.BooleanField(label='Polyphagia', required=False)
    genital_thrush = forms.BooleanField(label='Genital thrush', required=False)
    visual_blurring = forms.BooleanField(label='Visual blurring', required=False)
    itching = forms.BooleanField(label='Itching', required=False)
    irritability = forms.BooleanField(label='Irritability', required=False)
    delayed_healing = forms.BooleanField(label='Delayed healing', required=False)
    partial_paresis = forms.BooleanField(label='Partial paresis', required=False)
    muscle_stiffness = forms.BooleanField(label='Muscle stiffness', required=False)
    alopecia = forms.BooleanField(label='Alopecia', required=False)
    obesity = forms.BooleanField(label='Obesity', required=False)
    diabetes = forms.BooleanField(label='Diabetes', required=False, widget=forms.Select(choices=[(True, 'Positive'), (False, 'Negative')]))

    # # Customizes form validation for properties that apply to more
    # # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class PredictionForm(forms.Form):
    age = forms.IntegerField(label='Age')
    gender = forms.BooleanField(label='Gender', required=False, widget=forms.Select(choices=[(True, 'Male'), (False, 'Female')]))
    polyuria = forms.BooleanField(label='Polyuria', required=False)
    polydipsia = forms.BooleanField(label='Polydipsia', required=False)
    sudden_weight_loss = forms.BooleanField(label='Sudden weight loss', required=False)
    weakness = forms.BooleanField(label='Weakness', required=False)
    polyphagia = forms.BooleanField(label='Polyphagia', required=False)
    genital_thrush = forms.BooleanField(label='Genital thrush', required=False)
    visual_blurring = forms.BooleanField(label='Visual blurring', required=False)
    itching = forms.BooleanField(label='Itching', required=False)
    irritability = forms.BooleanField(label='Irritability', required=False)
    delayed_healing = forms.BooleanField(label='Delayed healing', required=False)
    partial_paresis = forms.BooleanField(label='Partial paresis', required=False)
    muscle_stiffness = forms.BooleanField(label='Muscle stiffness', required=False)
    alopecia = forms.BooleanField(label='Alopecia', required=False)
    obesity = forms.BooleanField(label='Obesity', required=False)

    # # Customizes form validation for properties that apply to more
    # # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data