from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.generic.base import View
from django.db.models import Q
from .models import User, Note
import face_recognition
import base64
import cv2
import numpy as np
from datetime import datetime


# Create your views here.
class RegisterView(View):
    def post(self, request):
        # print(request)
        picture = request.POST.get("picture", '')
        # print(picture)
        # register_form = RegisterForm(request.POST)
        # if register_form.is_valid():
        username = request.POST.get("username", "")
        if User.objects.filter(username=username):
            print('注册不成功')
            return JsonResponse({"status": 0})
        else:
            password = request.POST.get("password", "")
            user = User()
            # 图片存入np数组, 用于face_recognition的识别
            # imgdata = base64.b64decode(picture)  # b64解码
            # imgdata = np.fromstring(imgdata, np.uint8)  # 转化成np数组
            # imgdata = cv2.imdecode(imgdata, cv2.COLOR_BGR2RGB)   # 函数从指定的内存缓存中读取数据，并把数据转换(解码)成图像格式;主要用于从网络传输数据中恢复出图像。
            user.image = picture
            user.username = username
            # user.is_active =
            user.password = make_password(password)
            user.save()
            print('注册成功')
            return JsonResponse({"status": 1})
        # else:
        #     return JsonResponse({"status": 2})

            # 返回的状态 0 为用户已存在 1注册成功 2 为form验证失败


class HeadLoginView(View):
    def post(self, request):
        # login_form = LoginForm(request.POST)
        #
        # if login_form.is_valid():
        username = request.POST.get("username", '')
        picture = request.POST.get("picture", '')
        print(username)
        # 设置session
        # request.apllacation["username"] = username

        passimg = User.objects.get(username=username).image  # 获取注册时的图片数据
        print(passimg)
        if passimg == False:
            return JsonResponse({'status': 0})
        # print(passimg)
        # 新的图片数据进行转码
        picture = base64.b64decode(picture)
        picture = np.fromstring(picture, np.uint8)
        picture = cv2.imdecode(picture, cv2.COLOR_BGR2RGB)

        # 旧的图片数据进行转码
        passimg = base64.b64decode(passimg)
        passimg = np.fromstring(passimg, np.uint8)
        passimg = cv2.imdecode(passimg, cv2.COLOR_BGR2RGB)
        # 再利用face_recognition进行人脸识别
        my_face_encoding = face_recognition.face_encodings(passimg)[0]
        unknown_face_encoding = face_recognition.face_encodings(picture)[0]
        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
        if results[0] == True:
            print("It's a picture of me!")
            return JsonResponse({'status': 1})
        else:
            print("It's not a picture of me!")
            return JsonResponse({'status': 0})

        # else:
        #     return JsonResponse({"status": 2})

        # 返回的状态 0 为未注册, 1 成功, 2为form验证失败


class PassWordLoginView(View):

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 利用密码登录
        user = authenticate(username=username, password=password)

        if user is not None:
            # login
            # 设置session
            print('登录成功')
            return JsonResponse({"status": 1})
        else:
            print('登录失败')
            return JsonResponse({"status": 0})


class PostNote(View):

    def post(self, request):
        content = request.POST.get('content', '')
        print('content', content)
        username = request.POST.get('username', '')
        print("username", username)
        # print(request.session['username'])
        user = User.objects.get(username=username)
        note = Note.objects.create(content=content, user=user)
        note.save()
        return JsonResponse({'status': 1})


class GetNote(View):

    def post(self, request):
        username = request.POST.get("username", '')
        user = User.objects.get(username=username)
        note = Note.objects.filter(user=user).order_by('-time')
        list2 = []
        for i in note:
            list2.append(i.content)
        print(list2)
        return JsonResponse({"results": list2})


class SearchNote(View):

    def post(self, request):
        word = request.POST.get("word", '')
        username = request.POST.get("username", '')
        user = User.objects.get(username=username)
        resluts = Note.objects.filter(Q(user_id__exact=user) and Q(content__icontains=word))
        list = []
        for reslut in resluts:
            list.append(reslut.content)

        return JsonResponse({"results": list})


class ModifyNote(View):

    def post(self, request):
        username = request.POST.get('username', '')
        no = request.POST.get('no', '')
        content = request.POST.get('content', '')
        no = int(no)+1
        user = User.objects.get(username=username)
        Note.objects.filter(user_id=user.id, id=no).update(content=content, time=datetime.now())
        # note.save()
        return JsonResponse({'status': 1})


class DeleteNote(View):

    def post(self, request):
        username = request.POST.get('username', '')
        no = request.POST.get('no', '')
        no = int(no) +1
        user = User.objects.get(username=username)
        note = Note.objects.filter(user_id=user.id).order_by('-time')
        print(no)
        j = 0
        for i in note:
            j += 1
            if j == no:
                Note.objects.get(id=i.id).delete()

        return JsonResponse({'status': 1})
