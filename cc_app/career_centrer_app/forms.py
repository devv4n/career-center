from django import forms
from .models import StudentForm, Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'employer',
            'title',
            'responsibilities',
            'requirements',
            'conditions',
            'location',
            'contact_person',
            'contact_phone',
            'contact_email',
            'additional_contacts',
            'job_type',
        ]
        widgets = {
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'conditions': forms.Textarea(attrs={'rows': 4}),
            'additional_contacts': forms.Textarea(attrs={'rows': 3}),
        }


class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentForm
        fields = ['first_name', 'last_name', 'email', 'phone', 'faculty', 'vacancy', 'skills', 'work_experience', 'education_level', 'other_education', 'note', 'resume']
        widgets = {
            'vacancy': forms.Select(),
            'resume': forms.ClearableFileInput(attrs={'accept': '.pdf, .docx'}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'note': forms.Textarea(attrs={'rows': 3}),
            'faculty': forms.Select(),
        }

    vacancy = forms.ModelChoiceField(queryset=Vacancy.objects.filter(is_active=True), required=False, label="В какой вакансии заинтересованы?")
    work_experience = forms.BooleanField(required=False, label="Имеете ли Вы опыт работы в данной сфере?")
    education_level = forms.ChoiceField(choices=StudentForm.EDUCATION_LEVEL_CHOICES, required=True, label="Уровень образования")
    other_education = forms.CharField(required=False, label="Другой уровень")
