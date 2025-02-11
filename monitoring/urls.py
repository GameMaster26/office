from django.urls import path,include
from django.conf import settings
from . import views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.conf.urls.static import static
from .views import download_excel,export_excel,exp_excel,download_report_excel,download_report_pdf,download_masterlist_excel,download_masterlist_pdf,pdf_report_create,pdf_masterlist_create,excel_masterlist_create,logout,PatientListView,pdf_report_create2,pdf_report_create3,pdf_report_create4,pdf_report_create_annual,pdf_cohort_create1,pdf_cohort_create2,pdf_cohort_create3,pdf_cohort_create4,pdf_cohort_create_annual


app_name = 'monitoring'

urlpatterns = [

    #path('locked/', locked_view, name='locked'),
    #path('confirmation/', views.confirm_device, name='confirmation'),
    #path('lock_account/', views.lock_account, name='lock_account'),

    path('patientlistview/',PatientListView.as_view(),name='patientlist'),
    path('',views.index,name='index'),
    path('choropleth_map/',views.choropleth_map,name='choropleth_map'),
    path('admin/', views.admin_redirect, name='admin_redirect'),
    path('admin/logout/', views.logout, name='logout'),
    #path('admin/downloads/', views.table, name='table'),
    path('overview/', views.overview, name='overview'),
    path('overview/choropleth_map/', views.choro, name='choro'),
    path('overview/reports/', views.reports, name='reports'),
    path('overview/tables/', views.tables, name='tables'),
    #path('overview/download/', views.download, name='download'),
    path('overview/download_excel/', download_excel, name='download_excel'),
    path('overview/export_excel/', export_excel, name='export_excel'),
    path('overview/exp_excel/', exp_excel, name='exp_excel'),
    path('download_report_excel/', excel_masterlist_create, name='excel_masterlist_create'),

    #For Report URL
    path('download_report_pdf/', pdf_report_create, name='download_report_pdf'),
    path('download_report_pdf2/', pdf_report_create2, name='download_report_pdf2'),
    path('download_report_pdf3/', pdf_report_create3, name='download_report_pdf3'),
    path('download_report_pdf4/', pdf_report_create4, name='download_report_pdf4'),
    path('download_report_pdf_annual/', pdf_report_create_annual, name='download_report_pdf_annual'),


    #For Cohort URL
    path('download_cohort_pdf1/', pdf_cohort_create1, name='pdf_cohort_create1'),
    path('download_cohort_pdf2/', pdf_cohort_create2, name='pdf_cohort_create2'),
    path('download_cohort_pdf3/', pdf_cohort_create3, name='pdf_cohort_create3'),
    path('download_cohort_pdf4/', pdf_cohort_create4, name='pdf_cohort_create4'),
    path('download_cohort_pdf_annual/', pdf_cohort_create_annual, name='pdf_cohort_create_annual'),



    path('download_masterlist_excel/', download_masterlist_excel, name='download_masterlist_excel'),
    path('download_masterlist_pdf/', pdf_masterlist_create, name='download_masterlist_pdf'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

