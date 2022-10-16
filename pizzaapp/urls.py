from django.contrib import admin
from django.urls import path
from .views import acceptorder, adminorders, authenticateuser, customerwelcomeview, declineorder, logoutuser, placeorder, signupuser, homepageview, deletepizza, addpizza, adminhomepageview, adminloginview, authenticateadmin, logoutadmin, userloginview, userorders

urlpatterns = [
    path('admin/', adminloginview, name="adminloginpage"),
    path('adminauthenticate/', authenticateadmin),
    path('admin/homepage', adminhomepageview, name= "adminhomepage"),
    path("adminlogout/", logoutadmin),
    path("addpizza/", addpizza),
    path("deletepizza/<int:pizzapk>/", deletepizza),
    path("", homepageview, name = "homepage"),
    path("signupuser/", signupuser),
    path("loginuser/", userloginview, name= "userlogin"),
    path('userlogout/', logoutuser),
    path("authenticateuser/", authenticateuser),
    path('customer/', customerwelcomeview, name="customerpage"),
    path("placeorder/", placeorder),
    path("userorders/", userorders),
    path("adminorders/", adminorders),
    path("acceptorder/<int:orderpk>/", acceptorder),
    path("declineorder/<int:orderpk>/", declineorder),
]
