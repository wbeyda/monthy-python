from django.conf.urls import patterns, include, url
from django.contrib import admin
from zipcode import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^home$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^', include('zipcode.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
