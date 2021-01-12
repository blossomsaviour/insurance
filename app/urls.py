from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views as core_views
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    path('user-order/', views.UserOrder, name='user-order'),

    url(r'^insurance/entry/$', core_views.AddInsuranceForm, name='add-insurance'),
    path('insruance/<int:pk>/delete/', views.InsuranceDelete.as_view(), name='delete-insurance'),
    url(r'^insurance_profile/$', views.InsuranceListView.as_view(), name='insurance_profile'),
    path('select_insurer/<int:pk>/', views.SelectedInsurance.as_view(), name='selected_insurer'),
    path('buy-insurance/', views.UserInsuranceView, name='buy-insurance'),
    url(r'^order/$',views.OrdersListView.as_view(),name='orders'),

    path('payment_status/', views.payment_status, name='payment_status'),
    path('payment/', views.payment, name='payment'),
    path('payment_confirmation/', views.payment_confirmation.as_view(), name='payment_confirmation'),

]
