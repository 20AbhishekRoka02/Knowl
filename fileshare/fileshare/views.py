from django.shortcuts import render, HttpResponseRedirect
from account.views import jwtDecoder
from files.models import File
def convert_bytes(num):
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0

def dashboard(request):
    # return HttpResponse("This is dashboard.")
    if request.COOKIES.get('token'):
        data = jwtDecoder(request.COOKIES.get('token'))
        uploaded_user_files = File.objects.filter(user_id=data['id'])
        files_data = []
        for file in uploaded_user_files:
            file_data=dict()
            file_data['name']=file.file_name
            file_data['size']=convert_bytes(file.size)
            file_data['upload_date']=file.upload_date
            files_data.append(file_data)
        # data['files'] = files_data
            

        # print(data)
        return render(request,"new_dashboard.html",{'name':jwtDecoder(request.COOKIES.get('token'))['name'],'files':files_data})
    else:
        return HttpResponseRedirect("/auth")


def auth(request):
    if request.COOKIES.get('token'):
        return HttpResponseRedirect("/")
    else:
        return render(request, "auth.html")
    
# def searchPeer(request):
#     return render(request, "searchpeer.html")