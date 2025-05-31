from django import forms
from .models import Applicant, Application
from .models import EducationProgram

class EducationProgramForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        help_text="Опишите программу подробно, включая основные дисциплины и перспективы"
    )
    
    class Meta:
        model = EducationProgram
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        budget_places = cleaned_data.get('budget_places')
        paid_places = cleaned_data.get('paid_places')
        
        if budget_places == 0 and paid_places == 0:
            raise forms.ValidationError(
                "Программа должна иметь либо бюджетные, либо платные места"
            )
        return cleaned_data

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant', 'program', 'status', 'exam_results']
        widgets = {
            'exam_results': forms.Textarea(attrs={'rows': 3}),
        }