from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('', views.events_list),
    path('events', views.events_list, name='events'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_event/', views.add_event, name='add_event'),
    path('event/<int:event_id>', views.event_page, name='event'),
    path('update_event/<int:event_id>', views.update_event, name='update_event'),
    path('add_event_image/<int:event_id>', views.add_event_image, name='add_event_image'),
    path('remove_event_image/<int:event_image_id>', views.remove_event_image, name='remove_event_image'),



]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
