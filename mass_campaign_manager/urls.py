from django.contrib import admin
from django.urls import path
from campaigns import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Contact Lists
    path('lists/', views.contact_lists, name='contact_lists'),
    path('lists/<int:pk>/', views.contact_list_detail, name='contact_list_detail'),
    path('lists/<int:pk>/delete/', views.contact_list_delete, name='contact_list_delete'),

    # Subscribers
    path('lists/<int:list_id>/subscribers/add/', views.subscriber_create, name='subscriber_create'),
    path('subscribers/<int:pk>/update/', views.subscriber_update, name='subscriber_update'),
    path('subscribers/<int:pk>/delete/', views.subscriber_delete, name='subscriber_delete'),

    # Email Templates (V2)
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/update/', views.template_update, name='template_update'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),

    # Campaigns (V2)
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path('campaigns/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:pk>/update/', views.campaign_update, name='campaign_update'),
    path('campaigns/<int:pk>/delete/', views.campaign_delete, name='campaign_delete'),
    path('campaigns/<int:pk>/toggle-status/', views.campaign_toggle_status, name='campaign_toggle_status'),
]

