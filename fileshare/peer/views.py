from django.shortcuts import render
from django.http import HttpResponse
from account.models import User
from files.models import File
from account.views import wsgiRequestToDict, jwtDecoder
from peer.models import Share
# from fileshare.views import sharing
# Create your views here.
def search_peer(request):
    if request.method=="POST":
        request_data = wsgiRequestToDict(request)
        print(request_data)
        try:
            users = User.objects.filter(user_name=request_data['username'])
            
            users_data = []
            for user in users:
                user_data = dict()
                user_data['id'] = user.id
                user_data['name']=user.user_name
                uploaded = File.objects.filter(user_id=user.id)
                user_data['uploaded']= str(len(uploaded))
                users_data.append(user_data)
            context = {"name":jwtDecoder(request.COOKIES.get('token'))['name'],"result":True, "usersdata":users_data}
            return render(request,"searchpeer.html",context)

                
                
        except Exception as e:
            print(e)
            return HttpResponse("Some error occured.")

        pass
    return render(request,"searchpeer.html",{"name":jwtDecoder(request.COOKIES.get('token'))['name']})
    pass

def share(request):
    if request.method=="POST":
        request_data = wsgiRequestToDict(request)
        decoded = jwtDecoder(request.COOKIES.get('token'))
        
        files_to_share = request.POST.get('checked_names').split(",")
        # print(files_to_share)
        userid = decoded['id']
        peerid = request_data['peerID']
        # print(userid, peerid)
        try:
            if User.objects.filter(id=peerid).exists():
                # notexistsfile = []
                # sucessfullyshared=[]
                for file in files_to_share:
                    # print(file, type(file))
                    if not File.objects.filter(file_name=file).exists():
                        continue
                        # notexistsfile.append(file)
                    else:
                        fileid = File.objects.filter(file_name=file)
                        if Share.objects.filter(file_id=fileid[0].file_id).exists():
                            continue
                        else:
                            fileid = str(fileid[0].file_id)

                            file_shared = Share(sender_id=userid, recipient_id=peerid,file_id=fileid)
                            file_shared.save()
                            print(fileid)
                        # sucessfullyshared.append(file)
                # message = ""
                # if len(notexistsfile)<1:
                #     notexistsfile_message = ",".join(notexistsfile) + " not exists!"
                #     message+=notexistsfile_message+"\n"
                # if len(sucessfullyshared)>0:
                #     sucessfullyshared_message = ",".join(sucessfullyshared) + " shared successfully!"
                #     message+=sucessfullyshared_message
                # return HttpResponse(message)
                return HttpResponse("Performed sharing operation!")
            else:
                return HttpResponse(f"Given Peer ID doesn't exists. Peer ID: {peerid}")
        except Exception as e:
            print(e)
            return HttpResponse("An error occurred.")
        
    if request.method=="GET":
        try:
            user_cred= jwtDecoder(request.COOKIES.get('token'))
            user_files_instances = File.objects.filter(user_id=user_cred['id'])
            user_files = []
            if len(user_files_instances)>0:
                for file_instance in user_files_instances:
                    user_file = dict()
                    # user_file['fileid'] = file_instance.file_id
                    # user_file['userid'] = file_instance.user_id
                    # user_file['size'] = file_instance.size
                    user_file['filename'] = file_instance.file_name
                    # user_file['uploaddate'] = file_instance.upload_date
                    user_files.append(user_file)
                return render(request, "sharewithpeers.html",{"name":user_cred['name'], "availablefiles": user_files})
            else:
                return render(request, "sharewithpeers.html",{"name":user_cred['name']})

        except Exception as e:
            print(e)
        return HttpResponse("Sharing page.")

def uploadfiles(requests):
    decoded = jwtDecoder(requests.COOKIES.get('token'))
    context = dict()
    context['name']= decoded['name']
    if Share.objects.filter(recipient_id=decoded['id']).exists():
        transaction_instances = []
        transactions = Share.objects.filter(recipient_id=decoded['id'])
        for instance in transactions:
            instance_history = dict()
            instance_history['shareid'] = instance.share_id

            sender = User.objects.filter(id=instance.sender_id)
            instance_history['sender'] = sender[0].user_name

            file = File.objects.filter(file_id=instance.file_id)
            instance_history['file'] = file[0].file_name

            instance_history['timestamp'] = instance.share_timestamp
            transaction_instances.append(instance_history)
        context['received'] = transaction_instances

            
    return render(requests,"uploadedfiles.html", context)