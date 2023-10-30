from django.urls import path

from . import views

urlpatterns = [
    path('process-list', views.process_list, name='process-list'),
    path('process-create', views.process_create, name='process-create'),
    path('process-update/<str:process_id>', views.process_update, name='process-update'),
    path('process-delete/<str:process_id>', views.process_delete, name='process-delete'),

    path('process-view/<str:process_id>', views.process_view, name='process-view'),
    path('risk-create/<str:process_id>', views.risk_create, name='risk-create'),
    path('risk-upload/<str:process_id>', views.risk_upload, name='risk-upload'),
    path('risk-update/<str:risk_id>', views.risk_update, name='risk-update'),
    path('risk-delete/<str:risk_id>', views.risk_delete, name='risk-delete')
]
