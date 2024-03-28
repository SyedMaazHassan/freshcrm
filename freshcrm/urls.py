from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from core.views import index,about
from userprofile.views import signup,login,LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("", index, name='index'),
    path("dashboard/",include('dashboard.urls')),
    path("dashboard/leads/",include('lead.urls')),
    path("dashboard/scraper/",include('webscrape.urls')),
    path("about/", about, name='about'),
    path("signup/", signup, name='signup'),
    path("login/", auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path("logout/",LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
