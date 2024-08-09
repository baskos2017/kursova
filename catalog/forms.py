from django import forms
from .models import Comment, Order

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['city', 'last_name', 'first_name', 'phone', 'additional_info']
        widgets = {
            'city': forms.TextInput(attrs={'placeholder': 'Населений пункт', 'id': 'id_city'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Прізвище', 'id': 'id_last_name'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ім\'я', 'id': 'id_first_name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'id': 'id_phone'}),
            'additional_info': forms.Textarea(attrs={'placeholder': 'Додаткова інформація', 'id': 'id_additional_info'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['city'].label = "Населений пункт"
        self.fields['last_name'].label = "Прізвище"
        self.fields['first_name'].label = "Ім'я"
        self.fields['phone'].label = "Телефон"
        self.fields['additional_info'].label = "Додаткова інформація"