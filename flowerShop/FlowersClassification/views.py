from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage


from .image import predict_one_image, process_image

from django.contrib.auth.decorators import login_required

# def index(request):
#      flows = Categories.objects.all()
#      return render(request, 'index.html',{'flows':flows})




def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        context['filename'] = name
        pred, probability, text = process_image(name)

        context['probability'] = probability
        context['text'] = text
    return render(request, 'upload.html', context)
