from django.urls import path
from . import views

app_name = 'applicants'

urlpatterns = [
    path('', views.ApplicantListView.as_view(), name='applicant_list'),
    path('<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant_detail'),
    path('<int:pk>/update/', views.ApplicantUpdateView.as_view(), name='applicant_update'),
    path('new/', views.ApplicantCreateView.as_view(), name='applicant_create'),
    
    

    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='application_update'),
    path('applications/new/', views.ApplicationCreateView.as_view(), name='application_create'),
    
    path('applicant/<int:applicant_id>/application/<int:application_id>/pdf/',
         views.generate_pdf_document, name='generate_pdf_document'),
]