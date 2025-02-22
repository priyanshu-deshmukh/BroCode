from django.urls import path
from . import views

app_name = "llm"

urlpatterns = [
    path("home/", views.llm_home, name="llm_home"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("search/", views.search, name="search"),
    path("reputation/", views.reputation, name="reputation"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.profile, name="profile"),
]