from django.urls import path
from account.views import(
    RegisterView,LoginView,ChangePasswordView,GetUser,ChangeUserDetail,DeleteUser,AccountAPIView,
    
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"), 
    path('changepassword/', ChangePasswordView.as_view(), name="change_password"),
    path('getuser/<pk>',GetUser.as_view()),  
    path('changeuserdetail/<pk>',ChangeUserDetail.as_view()),
    path('deleteuser/<pk>',DeleteUser.as_view()),    
    path('dynamicfilter/', AccountAPIView.as_view())

]

