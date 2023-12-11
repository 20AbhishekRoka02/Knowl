from django.shortcuts import render, HttpResponse
from account.views import wsgiRequestToDict, jwtDecoder
from .models import File
# Create your views here.
def upload(request):
    if request.method=="POST" and request.FILES['files']:
        files = request.FILES.getlist('files')
        tokendata = jwtDecoder(request.COOKIES.get("token"))
        already = " already exists!"
        try:        
            for file in files:
                if File.objects.filter(user_id=tokendata['id']).exists() and File.objects.filter(file_name=file.name).exists():
                    already = " " + file.name + already
                else:
                    File.objects.create(user_id=tokendata['id'],size=file.size,file_name=file.name,upload_file=file)
        except Exception as e:
            print(e)
            return HttpResponse("Some error occured!")
            
        return HttpResponse(f"Files are successfully uploaded!")