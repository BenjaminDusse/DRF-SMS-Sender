from django.urls import path
from congrats.views import UsersListView, BirthdayUsers, CongrateUsers

urlpatterns = [
    path("birthday-users/", BirthdayUsers.as_view(), name="birthday_users"),
    path("users/", UsersListView.as_view(), name="user_list"),
    path("congrate-users/", CongrateUsers.as_view(), name="congrate_users"),]

