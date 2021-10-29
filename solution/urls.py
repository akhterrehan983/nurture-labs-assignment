"""rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from solution import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('user/register',views.userRegistration),
    path('user/login',views.userLogin),
    path('user/<int:id>/advisor',views.getAdvisor),
    path('user/<int:userId>/advisor/<int:advisorId>',views.bookAdvisor),
    path('user/<int:userId>/advisor/booking',views.getBookedCalls),

    #the given endpoint http://127.0.0.1:8000/admin/advisor throws error
    # Raised by:	django.contrib.admin.sites.catch_all_view
    #so given endpoint is replaced with http://127.0.0.1:8000/adminn/advisor
    path('adminn/advisor',views.addAdvisor),
    
    

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)