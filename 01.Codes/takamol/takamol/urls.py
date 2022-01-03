from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
urlpatterns = [
    
    path('admin/', admin.site.urls),
    re_path(r'^$', include('articles.urls'), name="home"),
    re_path(r'^articles/', include('articles.urls')), # To manage articles urls
    re_path(r'^users/', include('users.urls')), # To manage login, logout, and signup urls
]

urlpatterns += staticfiles_urlpatterns()