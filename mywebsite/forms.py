from django import forms
from django.forms import Textarea
from .models import myweb
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class Webform(forms.ModelForm):
    class Meta:
        model = myweb
        fields = ['image', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                # Ang Image ay nasa kaliwa (4 units)
                Column('image', css_class='form-group col-md-4 mb-0'),
                
                # Ang Description ay nasa kanan (8 units)
                # Dito rin natin i-set yung laki ng rows
                Column('description', css_class='form-group col-md-8 mb-0'),
            ),
        )
        
        # Ito ang diskarte para palitan ang rows ng textarea sa Crispy
        self.fields['description'].widget.attrs.update({'rows': '10', 'cols': '90'})