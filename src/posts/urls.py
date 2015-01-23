from django.conf import settings

from django.conf.urls import patterns, url
from . import views



urlpatterns = patterns('posts.views',
    # Examples:
    url(r'^tags/(?P<tag>\S+)/$', views.TagDetail.as_view(), name='tag_detail'),
    url(r'^(?P<slug>[\w-]+)/$', views.single_post, name='single_post'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category_single, name='category'),



)


