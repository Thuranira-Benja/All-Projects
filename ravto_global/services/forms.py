from django import forms

class ServiceRequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    service_type = forms.ChoiceField(choices=[
        ('electrical', 'Electrical & Electronics'),
        ('plumbing', 'Plumbing'),
        ('civil', 'Civil Engineering'),
        ('ict', 'ICT Services'),
        ('mechanical', 'Mechanical'),
        ('automotive', 'Automotive Repair'),
    ])
    location = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
