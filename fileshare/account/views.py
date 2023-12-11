from .models import User
from django.shortcuts import HttpResponse,HttpResponseRedirect

import hashlib
import jwt
from cryptography.hazmat.primitives import serialization
from urllib.parse import parse_qs

def toHash(data):
    sha256_hash = hashlib.sha256(data.encode())
    hash_hex = sha256_hash.hexdigest()
    return hash_hex

def turnToJWT(payload):
    private_key = open('rsa/id_rsa','r').read()
    key = serialization.load_ssh_private_key(private_key.encode(),password=b'')
    return jwt.encode(payload=payload, key=key, algorithm='RS256')

def jwtDecoder(token):
    public_key = open('rsa/id_rsa.pub','r').read()
    new_key = serialization.load_ssh_public_key(public_key.encode())
    decoded = jwt.decode(jwt=token, key=new_key, algorithms=['RS256', ])
    return decoded

def wsgiRequestToDict(the_request):
    data = parse_qs(the_request.body.decode('utf-8'))
    data_dict = {key: value[0] for key, value in data.items()}
    return data_dict

def login(request):
    if request.method == "POST":
        data = wsgiRequestToDict(request)
        # print(data)
        if (User.objects.filter(email=data["email"]).exists()):
            if toHash(data['password'])==User.objects.get(email=data['email']).password:                
                user = User.objects.get(email=data["email"])
                payload={
                    "id":str(user.id),
                    "name":user.user_name,
                    "email":user.email,
                    "phone":user.phone
                }
                token = turnToJWT(payload)
                response =  HttpResponseRedirect("/")
                response.set_cookie('token',token, httponly=True)
                return response
                
            else:
                return HttpResponse("Auth Failure!")
        else:
            return HttpResponse("User not exists!")


    pass

def signup(request):
    if request.method=="POST":
        data = wsgiRequestToDict(request)
        # print(data)
        try:
            if len(User.objects.filter(email=data["email"])) != 0:
                return HttpResponse("User already exists!")
            else:
                create_user = User(
                user_name = data['name'],
                email = data['email'],
                phone = data['phone'],
                password = toHash(data['password'])
                )
                
                user_id = create_user.save()
                print(user_id)
                payload = {
                    "id":user_id,
                    "name":data['name'],
                    "email":data['email'],
                    "phone":data['phone']
                }
                token = turnToJWT(payload)
                response = HttpResponseRedirect("/")
                response.set_cookie('token',token,httponly=True)
                return response
        except Exception as e:
            print(e)
            return HttpResponseRedirect("/auth/")
    

    pass

def logout(request):
    if request.method=="POST":
        response = HttpResponseRedirect("/")
        response.delete_cookie('token')
        return response
        
    