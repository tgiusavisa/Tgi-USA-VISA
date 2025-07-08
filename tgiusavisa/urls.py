from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('superadmin-dashboard/', admin.site.urls),
    path('chat-api/', views.chat_api, name='chat_api'),
    path('', views.home, name='index'),
    path('', include('account.urls')),
    path('', include('websitedashboard.urls')),
    path('', include('Clients.urls')),
    path('visitor-count/', views.visitor_count, name='visitor_count'),
    path('blog/', include('blogs.urls')),
]