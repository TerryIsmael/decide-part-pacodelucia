from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, RegisterView, getTokens, deleteToken, addToken, adminLogin, isAdmin, UserView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('get-auth/', getTokens),
    path('del-auth/<int:userId>', deleteToken),
    path('add-auth/<int:userId>', addToken),
    path('login-auth/', adminLogin),
    path('admin-auth/', isAdmin),
    path('user/', UserView.as_view()),
]
