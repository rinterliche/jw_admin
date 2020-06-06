"""jwadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from outerpages.views import (
     service_week_screen_view,
     list_service_occurrences_view,
     new_service_occurrence_view,
     edit_service_occurrence_view,
     show_service_occurrence_view,
     list_territories_view,
     new_territory_view,
     edit_territory_view,
     show_territory_view,
)
from account.views import (
     registration_view,
     logout_view,
     login_view,
)


handler404 = 'outerpages.views.page_not_found_view'

urlpatterns = [
    path('', login_view, name="home"),

    path('service_week/', service_week_screen_view, name="service_week"),

    path('territory/list', list_territories_view, name="list_territories"),
    path('territory/new', new_territory_view, name="new_territory"),
    path('territory/<int:id>/edit', edit_territory_view, name="edit_territory"),
    path('territory/<int:id>/show', show_territory_view, name="show_territory"),

    path('service_occurrence/list', list_service_occurrences_view, name="list_service_occurrences"),
    path('service_occurrence/new', new_service_occurrence_view, name="new_service_occurrence"),
    path('service_occurrence/<int:id>/edit', edit_service_occurrence_view, name="edit_service_occurrence"),
    path('service_occurrence/<int:id>/show', show_service_occurrence_view, name="show_service_occurrence"),


    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('admin/', admin.site.urls),

    # API URLS
    path('api/', include("api.urls")),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
