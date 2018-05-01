from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^registration$', views.registration),
  url(r'^login$', views.login),
  url(r'^create$', views.create),
  url(r'^index$', views.index),
  url(r'^logout$', views.logout),
  url(r'^new$', views.new),
  url(r'^make_product$',views.make_product),
  url(r'^add_to_wishlist$',views.add_to_wishlist),
  url(r'^show/<int:product_id>$', views.show),
  url(r'^remove_from_wishlist$', views.remove_from_wishlist),
  url(r'^delete_product$', views.delete_product)
]
