from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail

from .serializers import (
    UserLoginSerializer ,
    UserLogoutSerializer , 
    UserRegisterSerializer , 
    UserRegisterVerifySerializer,
    UserRegisterCompleteSerializer
)
from .models import User , OTP
import random


class UserLoginAPIView(TokenObtainPairView):

    """
        لاگین کردن کاربر \n
        کاربر ایمیل و رمز عبور خود را باید ارسال کند و یک جفت توکن اکسس و رفرش دریافت کند
        توکنی که باید برای هر کاربر در نظر گرفت اکسس است
    """

    serializer_class = UserLoginSerializer


class UserLogoutAPIView(APIView):

    """
        لاگ اوت کردن کاربر \n
        رفرش توکن کاربر را دریافت میکند و منقضی میشود \n
        فرانت هم باید اکسس توکن را حذف کند
    """

    serializer_class = UserLogoutSerializer

    def post(self,request):
        srz_data = self.serializer_class(data = request.data)
        if srz_data.is_valid():
            refresh = srz_data.validated_data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message":"Refresh Token Deleted"},status=status.HTTP_205_RESET_CONTENT)
        return Response({"message":"Error Logout"},status=status.HTTP_400_BAD_REQUEST)
    

class UserRegisterAPIView(APIView):

    """
        رجیستر کردن کاربر (مرحله اول) \n
        ایمیل کاربر را گرفته و در سشن ذخیره میکند و یک کد چهار رقمی به ایمیل ارسال میکند
    """

    serializer_class = UserRegisterSerializer

    def post(self , request):
        srz_data = self.serializer_class(data = request.data)

        if srz_data.is_valid():
            vd = srz_data.validated_data
            create_code = random.randint(1000,9999)

            otp = OTP.objects.create(email = vd["email"] , code = create_code)
            request.session["user_email"] = vd["email"]

            mesg = f"Code Verify {otp.code}"
            send_mail("Yadegar",mesg,"testpass935@gmail.com" , [vd["email"]] , fail_silently=False)
            return Response(data=srz_data.data , status=status.HTTP_201_CREATED)
        return Response(srz_data.errors)
    

class UserRegisterVerifyAPIView(APIView):

    """
        رجیستر کردن کاربر (مرحله دوم) \n
        کد ارسال شده به ایمیل را دریافت میکند
    """

    serializer_class = UserRegisterVerifySerializer

    def post(self , request):
        srz_data = self.serializer_class(data = request.data)
        email = request.session.get("user_email")
        print("=========EMAIL========",email)
        otp = OTP.objects.get(email = email)

        if srz_data.is_valid():
            if otp.code == srz_data.validated_data["code"]:
                otp.delete()
                return Response({"message":"کد تایید شد . به مرحله آخر ریدایرکت شود"} , status=status.HTTP_302_FOUND)
            else:
                return Response({"message":"کد اشتباه است"} , status=status.HTTP_400_BAD_REQUEST)
        return Response(srz_data.errors)
    

class UserRegisterCompleteAPIView(APIView):

    """
        رجیستر کردن کاربر (مرحله سوم) \n
        نام کاربری و رمزعبور را از کاربر دریافت میکند وحساب ساخته میشود. \n
        کاربر لاگین میشود و یک جفت توکن رفرش و اکسس برمیگرداند
    """

    serializer_class = UserRegisterCompleteSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        email = request.session.get("user_email") 

        if srz_data.is_valid():
            vd = srz_data.validated_data
            user = User.objects.create(
                email=email,
                username=vd["username"],
                password=vd["password"]
            )
            
            token = RefreshToken.for_user(user)
            return Response({"message": "کاربر رجیستر و لاگین شد", "access": str(token.access_token),"refresh": str(token)}, status=status.HTTP_201_CREATED)
        
        return Response(srz_data.errors)
