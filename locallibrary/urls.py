
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # django authentication system login logout and registere
    path('accounts/', include('django.contrib.auth.urls')),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/', permanent=True)),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
