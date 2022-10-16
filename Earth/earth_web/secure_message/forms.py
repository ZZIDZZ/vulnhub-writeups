import re

from ipaddress import ip_address
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import EncryptedMessage

class MessageForm(ModelForm):
    message_key = forms.CharField(max_length=50)
    class Meta:
        model = EncryptedMessage
        fields = ['message']

class CLICommandField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        for potential_ip in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', value):
            try:
                ip_address(potential_ip)
            except:
                pass
            else:
                raise ValidationError('Remote connections are forbidden.')

class CLIForm(forms.Form):
    cli_command = CLICommandField(label='CLI command', max_length=100)
