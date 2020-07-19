from django.forms import ModelForm, CheckboxSelectMultiple, Form, CharField, PasswordInput
from .models import Teacher

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'room_number', 'profile_picture']

