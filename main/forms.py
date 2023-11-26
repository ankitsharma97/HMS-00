from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    profile_picture = forms.ImageField(required=False)
    username = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    address_line1 = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)

    user_type = forms.ChoiceField(
        choices=[
            ('patient', 'Patient'),
            ('doctor', 'Doctor'),
        ],
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'username', 'password1', 'password2', 'address_line1', 'city', 'state', 'pincode', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        if self.cleaned_data['user_type'] == 'patient':
            # Create a patient profile
            from .models import Patient
            patient = Patient.objects.create(user=user, address_line1=self.cleaned_data['address_line1'], city=self.cleaned_data['city'], state=self.cleaned_data['state'], pincode=self.cleaned_data['pincode'])
        elif self.cleaned_data['user_type'] == 'doctor':
            # Create a doctor profile
            from .models import Doctor
            doctor = Doctor.objects.create(user=user, address_line1=self.cleaned_data['address_line1'], city=self.cleaned_data['city'], state=self.cleaned_data['state'], pincode=self.cleaned_data['pincode'])

        return user
