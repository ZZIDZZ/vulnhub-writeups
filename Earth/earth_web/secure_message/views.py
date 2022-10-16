from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import EncryptedMessage
from .forms import MessageForm, CLIForm
import subprocess

def index(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            encrypted_text = xor_cipher_hex(request.POST['message'], request.POST['message_key'])
            EncryptedMessage.objects.create(message=encrypted_text)
    else:
        form = MessageForm()

    return render(request, 'secure_message/index.html', {'form': form, 'previous_messages': EncryptedMessage.objects.order_by('-id')})

def admin(request):
    cmd_output = ''
    if request.method == 'POST':
        form = CLIForm(request.POST)
        if form.is_valid():
            cmd_output = subprocess.run(request.POST['cli_command'], capture_output=True, text=True, shell=True).stdout
    else:
        form = CLIForm()
    return render(request, 'secure_message/admin.html', {'form': form, 'cmd_output': cmd_output})

def xor_cipher_hex(text, key):
    result = ''
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result.encode('utf-8').hex()
