from django.urls import path
from Products import views as Products_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Products_views.index.as_view(), name='home'),
    path('api/Products/', Products_views.Products_list),
    path('api/Products/<int:pk>/', Products_views.Products_detail),
    path('api/Products/published/', Products_views.Products_list_published)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)