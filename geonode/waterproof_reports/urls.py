
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.views.generic import TemplateView

# Loading plotly Dash apps script
import dash_app_code

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.reportMenu, name='reports'),
    path('data', views.pivot_data, name='pivot_data'),
    url('^dash_plot$', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
    url('^django_plotly_dash/', include('django_plotly_dash.urls')),
]