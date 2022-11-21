from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import default_storage
import requests
import hashlib

def dashboard(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            token = form.cleaned_data['token']
            uploaded_file = request.FILES['file']
            uploaded_file_size = 'size of file uploaded(bytes): ' + str(uploaded_file.size)
            content_type = 'content type of file: ' + str(uploaded_file.content_type)
            uploaded_filename = 'file name: ' + str(uploaded_file.name)
            messages.success(request, 'Access bearer token is ' + str(token))
            messages.success(request,uploaded_file_size)
            messages.success(request,content_type)
            messages.success(request,uploaded_filename)

            #STEP 1
            try:
                headers =  {"Authorization": f"Bearer {token}"}
                response = requests.post('http://integrations.bynder.com/upload/prepare', headers=headers)
                json_response = response.json()
                success_message = 'File ID is ' + str(json_response['file_id'])
                file_id = json_response['file_id']
                messages.success(request, success_message)
            except:
                test_success_message = 'File ID is 1 for testing purposes'
                file_id = 1
                messages.success(request, test_success_message)

            CHUNK_SIZE = 1048576
            cfilectr = 0
            file_saved = default_storage.save(uploaded_file.name, uploaded_file)
            total_hex = ""
            with default_storage.open(file_saved, 'rb') as readbinfile:
                while True:
                    chunk = readbinfile.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    cfilectr += 1
                    chunk_digest = hashlib.sha256(chunk).hexdigest()
                    total_hex += str(chunk_digest)
                    #STEP 2
                    try:
                        headers =  {"Authorization": f"Bearer {token}", "content-sha256": chunk_digest}
                        response = requests.post('http://integrations.bynder.com/' + str(file_id) + '/chunk/' + str(cfilectr), headers=headers, data=chunk)
                    except:
                        chunk_number = 'Chunk number is ' + str(cfilectr)
                        hexdigest_status = 'Hex digest is ' + str(chunk_digest) + ' for testing purposes'
                        messages.success(request, chunk_number)
                        messages.success(request, hexdigest_status)

            #STEP 3
            try:
                headers =  {"Authorization": f"Bearer {token}", "content-sha256": total_hex, "Content-Type": "application/x-www-form-urlencoded"}
                data = {"filename": uploaded_file.name, "filesize": uploaded_file.size, "chunks": cfilectr}
                response = requests.post('http://integrations.bynder.com/upload/' + str(file_id) + '/finalise', headers=headers, data=data)
            except:
                messages.success(request, 'Total chunks are: ' + str(cfilectr))
    else:
        form = UploadFileForm()
    return render(request, 'cwrapper/dashboard.html', {"form": form})
