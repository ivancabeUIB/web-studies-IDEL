from django import forms

class ChatbotForm(forms.Form):
    message = forms.CharField(
        label="Dime lo que quieras saber sobre la web",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Escribe tu mensaje aquí..."})
    )
