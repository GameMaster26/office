# Standard Library Imports
from django.utils import timezone
from datetime import datetime, timedelta
import io
from io import BytesIO

# Django Imports
from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin, GroupAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.contrib.gis import admin as gis_admin
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.admin import GISModelAdmin
from django.db import router, transaction
from django.db.models import Max, Q, OuterRef, Subquery
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape, format_html, mark_safe
from django.utils.translation import gettext_lazy as _,gettext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

# Third-party Library Imports
from leaflet.admin import LeafletGeoAdmin
from leaflet.forms.widgets import LeafletWidget
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer 
from reportlab.platypus import HRFlowable
from reportlab.lib.enums import TA_CENTER
from import_export import resources

# Local App Imports
from .models import Patient, History, Treatment, Municipality, Barangay, Doctor, User
from .forms import PatientAdminForm, HistoryForm, HistoryInlineForm, CustomMapWidget,DoctorForm

# Django Custom Imports
from django.contrib.contenttypes.admin import GenericTabularInline, GenericInlineModelAdmin
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import PermissionDenied

# CSRF and Sensitive Post Parameters Decorators
csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters)


class AgeFilter(SimpleListFilter):
    title = 'Age of Patient' 
    parameter_name = 'age' 

    def lookups(self, request, model_admin):
        
        return (
            ('below_15', 'Below or Equal 15'),
            ('above_16', 'Above 15'),
        )
    
    def queryset(self, request, queryset):
        
        today = datetime.today()
        if self.value() == 'below_15':
            return queryset.filter(birthday__gt=today - timedelta(days=365*15))
        elif self.value() == 'above_16':
            return queryset.filter(birthday__lt=today - timedelta(days=365*16))

class BarangayFilter(SimpleListFilter):
    title = 'Barangay'
    parameter_name = 'brgy_id'
    
    def lookups(self, request, model_admin):
        return Patient.objects.values_list('brgy_id__brgy_name', 'brgy_id__brgy_name').distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brgy_id__brgy_name=self.value())

class CodeFilter(admin.SimpleListFilter):
    title = _('Animal Bite Center Code')
    parameter_name = 'user__code'

    def lookups(self, request, model_admin):
        """Retrieve and display all distinct user codes, even if no patient exists yet."""
        # Query distinct codes from the User model
        codes = User.objects.values_list('code', flat=True).distinct()
        return [(code, code) for code in codes if code]

    def queryset(self, request, queryset):
        """Filter queryset based on selected code."""
        if self.value():
            return queryset.filter(user__code=self.value())
        return queryset

class CodeForeign(admin.SimpleListFilter):
    title = _('Animal Bite Center Code')
    parameter_name = 'patient_id__user__code'

    def lookups(self, request, model_admin):
        # Get distinct codes associated with users who have patients
        codes = User.objects.values_list('code', flat=True).distinct()
        return [(code, code) for code in codes if code]  # filter out any null or empty values

    def queryset(self, request, queryset):
        # Filter the queryset based on the selected code value
        if self.value():
            return queryset.filter(patient_id__user__code=self.value())
        return queryset

class MunicipalityFilter(SimpleListFilter):
    title = 'Municipality of Patient'
    parameter_name = 'muni_id'

    def lookups(self, request, model_admin):
        return Patient.objects.values_list('muni_id__muni_name', 'muni_id__muni_name').distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(muni_id__muni_name=self.value())
        
class BarangayFilter(SimpleListFilter):
    title = 'Barangay of Patient'
    parameter_name = 'brgy_id'

    def lookups(self, request, model_admin):
        # Return unique Barangay names for filtering
        return Patient.objects.values_list('brgy_id__brgy_name', 'brgy_id__brgy_name').distinct()

    def queryset(self, request, queryset):
        if self.value():
            # Filter the queryset by the selected Barangay
            return queryset.filter(brgy_id__brgy_name=self.value())
        return queryset


class DoctorFilter(SimpleListFilter):
    title = 'Doctors'  # The title shown in the admin panel
    parameter_name = 'doctor'  # The parameter used in the query string

    def lookups(self, request, model_admin):
        # Generate unique doctor full names for filtering
        doctors = Doctor.objects.all()
        return [
            (doctor.id, f"{doctor.first_name} {doctor.middle_name or ''} {doctor.last_name}".strip())
            for doctor in doctors
        ]

    def queryset(self, request, queryset):
        if self.value():
            # Filter the queryset by the selected doctor ID
            return queryset.filter(doctor_id=self.value())
        return queryset



class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient
        fields = ('first_name','middle_name', 'last_name', 'muni_id','brgy_id', 'age', 'sex','contactNumber','doctor')
        export_order = ('doctor','first_name','middle_name', 'last_name', 'muni_id','brgy_id', 'age', 'sex','contactNumber')

class CustomGeoAdmin(LeafletGeoAdmin):
    
    class Media:
        css = {
            'all': ('assets/css/muni.css',),  
        }
        js = ('assets/js/reset_view.js',
            'assets/js/municipality_center.js',
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'assets/js/mapHistory.js',   
        )

@admin.register(Doctor) 
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email','licensed',  'specialization','muni_id', 'brgy_id')
    list_filter = ('gender', 'muni_id', 'brgy_id')
    search_fields = ('first_name', 'middle_name', 'last_name', 'email', 'contact_number')
    ordering = ('last_name', 'first_name')
    list_per_page = 5
    ordering = ('first_name',) 

    # Group fields logically in the form view
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name','licensed', 'specialization', 'gender','is_superdoctor')
        }),
        ('Contact Information', {
            'fields': ('muni_id', 'brgy_id', 'email','contact_number' )
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.middle_name or ''} {obj.last_name}".strip()
    full_name.short_description = "Full Name"

    readonly_fields = ('full_name',)

    """ # Override to restrict permissions for non-superusers
    def has_change_permission(self, request, obj=None):
        # Allow change permission only for superusers
        if not request.user.is_superuser:
            return False  # Non-superusers cannot change
        return super().has_change_permission(request, obj) """

    def has_delete_permission(self, request, obj=None):
        # Allow delete permission only for superusers
        if not request.user.is_superuser:
            return False  # Non-superusers cannot delete
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        # Allow add permission for all users (superusers and non-superusers)
        return super().has_add_permission(request)
    
    # Optionally restrict the 'is_superdoctor' field visibility to superusers only
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'is_superdoctor' and not request.user.is_superuser:
            kwargs['disabled'] = True  # Disable field for non-superusers
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.is_superdoctor = False  # Prevent non-superusers from changing this field
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/theadColor.css','admin/css/checkbox.css',) 
        }


class PatientInline(admin.StackedInline):
    model = Patient
    extra = 0
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'patient_id']
            return readonly_fields
        return self.readonly_fields

class HistoryInline(admin.StackedInline):
    model = History
    form = HistoryInlineForm
    extra = 0

    def get_fields(self, request, obj=None):
        fields = ['date_registered', 'date_of_exposure', 'muni_id', 'brgy_id','source_of_exposure','category_of_exposure', 
                    'exposure_type','bite_site', 'provoked_status', 'immunization_status',
                    'status_of_animal', 'confinement_status',  'washing_hands', 'human_rabies',]#'geom'
        if obj:
            fields.insert(0, 'registration_no')
        return fields

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        if obj:
            if request.user.is_superuser and 'registration_no' in formset.form.base_fields:
                
                formset.form.base_fields['registration_no'].widget.attrs['readonly'] = True
                formset.form.base_fields['registration_no'].required = False
        else:
            
            formset.form.base_fields.pop('registration_no', None)
        return formset

    """ def has_change_permission(self, request, obj=None):
        if obj:
            return False  
        return True   """
    # Prevent editing of History inline records
    """ def has_change_permission(self, request, obj=None):
        return False """

    # Override the has_delete_permission method to disable delete option
    def has_delete_permission(self, request, obj=None):
        return False  # Prevents deletion of Treatment inline records

class TreatmentInline(admin.StackedInline):
    model = Treatment
    extra = 0

    """ def has_change_permission(self, request, obj=None):
        if obj:
            
            return False  
        return True   """

    # Override the has_delete_permission method to disable delete option
    def has_delete_permission(self, request, obj=None):
        return False  # Prevents deletion of Treatment inline records

@admin.register(Patient)
class PatientAdmin(LeafletGeoAdmin):
    list_display = ('code', 'first_name','middle_name', 'last_name', 'muni_id','brgy_id','street', 'age', 'sex','contactNumber')
    list_per_page = 5
    search_fields = ['first_name','middle_name','last_name','muni_id__muni_name','brgy_id__brgy_name','sex__iexact']
    list_filter = (CodeFilter, MunicipalityFilter,BarangayFilter,AgeFilter, 'sex')
    inlines = [HistoryInline, TreatmentInline] 
    exclude = ('user',) 
    ordering = ('-patient_id',)

    actions = ['export_patient_data']

    def export_patient_data(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one patient to export data.", level='error')
            return

        patient = queryset.first()

        # Create HTTP response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{patient.first_name} {patient.last_name} Rabies Exposure Registry.pdf"'
 
        # Initialize buffer for PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        elements = []

        # Title of the document
        elements.append(Paragraph(
            "National Rabies Prevention and Control Program",
            ParagraphStyle(name="Title", fontSize=13, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=10)
        ))

        elements.append(Paragraph(
            "Rabies Exposure Registry",
            ParagraphStyle(name="Title", fontSize=13, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=20)
        ))

        # Gather data for the table
        histories = History.objects.filter(patient_id=patient)
        treatments = Treatment.objects.filter(patient_id=patient)

        # Define the table header with line breaks using \n for multi-line text
        data = [
            [
                Paragraph("Registration\nNo", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Registration\nDate", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Name\nof\nPatient", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Address\nof\nPatient", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Age", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Sex", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Date\nof\nExposure", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Place\nof\nExposure", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Type\nof\nAnimal", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Type", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Category", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Day\n0", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Day\n3", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Day\n7", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
                Paragraph("Brand\nName", style=ParagraphStyle(name="Header", fontSize=8, alignment=1, textColor=colors.black)),
            ]
        ]

        # Add rows for each history and treatment
        for history in histories:
            treatment = treatments.filter(patient_id=patient).first()

            # Break the patient's name into words using space as delimiter
            name_words = f"{patient.first_name} {patient.middle_name} {patient.last_name}".split()
            name = "<br/>".join(name_words)

            # Wrap the patient address in Paragraphs to allow text wrapping
            patient_address = f"{patient.muni_id}, {patient.brgy_id}"

            # Break Place of Exposure as well
            place_of_exposure = f"{history.muni_id}, {history.brgy_id}"

            # Format the date in the desired format (e.g., "November 11, 2024")
            formatted_date = history.date_of_exposure.strftime("%B %d, %Y")  # Converts to 'Month Day, Year'

            # Add data to the table row
            data.append([
                history.registration_no,
                Paragraph(formatted_date, style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)),
                Paragraph(name, style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)),
                Paragraph(patient_address, style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)),
                patient.get_age(),
                patient.sex.capitalize(),
                Paragraph(formatted_date, style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)),
                Paragraph(place_of_exposure, style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)),
                history.source_of_exposure,
                history.exposure_type,
                history.category_of_exposure,
                Paragraph(
                    treatment.day0.strftime("%B %d, %Y") if treatment and treatment.day0 else "N/A",
                    style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)
                ),
                Paragraph(
                    treatment.day3.strftime("%B %d, %Y") if treatment and treatment.day3 else "N/A",
                    style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)
                ),
                Paragraph(
                    treatment.day7.strftime("%B %d, %Y") if treatment and treatment.day7 else "N/A",
                    style=ParagraphStyle(name="Data", fontSize=8, alignment=1, textColor=colors.black, wordWrap=True)
                ),
                treatment.vaccine_brand_name if treatment else "N/A"
            ])

        # Create the table with column widths adjusted for compactness
        table = Table(data, repeatRows=1, hAlign="CENTER", colWidths=[60, 60, 60, 60, 30, 30, 60, 60, 40, 40, 40, 50, 50, 50, 50])  
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  
            ('WORDSPACE', (0, 0), (-1, -1), 0.2),  
        ]))

        # Append the table to elements
        elements.append(table)

        # Add the "Noted By" section
        elements.append(Spacer(1, 20))  # Space before "Noted By"
        elements.append(Paragraph("Noted By:", style=ParagraphStyle(name="NotedBy", fontSize=10, alignment=1)))
        elements.append(Spacer(1, 15))  # Slightly more space between "Noted By" and the name
        elements.append(Paragraph(
            f"{request.user.first_name} {request.user.last_name}",
            style=ParagraphStyle(name="NotedByName", fontSize=10, fontName="Helvetica-Bold", alignment=1, spaceAfter=5)
        ))

        # Add the horizontal line directly beneath the name (no extra space)
        elements.append(HRFlowable(width="20%", thickness=0.5, color=colors.black, spaceBefore=0, spaceAfter=0))



        # Add footer (Treatment Center)
        municipality_name = {
            'ALM': 'Almeria', 'BIL': 'Biliran', 'CABUC': 'Cabucgayan', 'CAIB': 'Caibiran',
            'CUL': 'Culaba', 'KAW': 'Kawayan', 'MAR': 'Maripipi', 'NAV': 'Naval'
        }
        treatment_center = municipality_name.get(request.user.code, "Biliran Province Hospital")

        # Add some space before the footer, pushing it down to the bottom of the page
        elements.append(Spacer(1, 200))  # Adjust spacer to place it at the bottom

        # Create the footer text with bold only for the treatment_center
        footer_text = f"Name of Animal Bite Treatment Center: <b>{treatment_center} Animal Bite Center</b>"

        # Set footer style with left alignment
        footer_style = ParagraphStyle(
            name="Footer", 
            fontSize=8, 
            fontName="Helvetica", 
            alignment=0,  # Left alignment
            spaceBefore=10
        )

        # Add footer
        elements.append(Paragraph(
            footer_text,
            style=footer_style
        ))

        # Adjusting the layout to mov

        # Build the PDF
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    export_patient_data.short_description = "Export patient data"


    def get_search_results(self, request, queryset, search_term):
        # Allow search across all patients for all users, also show user code during search
        if search_term:
            queryset = Patient.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(middle_name__icontains=search_term) |
                Q(last_name__icontains=search_term)
            ).select_related('user')  
        return queryset, False  

    def get_list_display(self, request):
        # If not searching or for regular users, remove 'code' from the list view
        if not request.GET.get('q'):  # When no search query
            if request.user.is_superuser:
                return ('code', 'first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id','street', 'age', 'sex', 'contactNumber')
            else:
                return ('first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id','street', 'age', 'sex', 'contactNumber')
        else:  # When search query is present
            return ('code', 'first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id','street', 'age', 'sex', 'contactNumber')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            queryset = qs.annotate(
                latest_registration_no=Max('histories__registration_no')
            ).order_by('-latest_registration_no')
        else:
            queryset = qs.filter(user=request.user).annotate(
                latest_registration_no=Max('histories__registration_no')
            ).order_by('-latest_registration_no')
        return queryset

    # Allow editing patients by ensuring the correct patient object is retrieved
    def get_object(self, request, object_id, from_field=None):
        try:
            # Get the patient by its ID, bypassing user-based filtering for editing
            return Patient.objects.get(pk=object_id)
        except Patient.DoesNotExist:
            return None  # Return None if the patient doesn't exist

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'patient_id']
            return readonly_fields
        return self.readonly_fields
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request,obj)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def each_context(self, request):
        context = super().each_context(request)
        context['search_name'] = '<script src="/static/placeholder/search_name.js"></script>'
        return context

    def brgy_name(self, obj):
        return obj.brgy_id.brgy_name
    brgy_name.short_description = 'Barangay'

    def muni_name(self, obj):
        return obj.muni_id.muni_name
    muni_name.short_description = 'Municipality'
    
    def age(self, obj):
        # Calculate age based on the birth date
        today = datetime.today()
        age = today.year - obj.birthday.year - ((today.month, today.day) < (obj.birthday.month, obj.birthday.day))
        return age
    age.short_description = 'Age'  # Display as 'Age' in the admin interface

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return (MunicipalityFilter,BarangayFilter,AgeFilter, 'sex')

    class Media:
        js = ('assets/js/admin.js',)
        css = {
            'all': ('assets/css/admin.css','admin/css/theadColor.css','admin/css/checkbox.css',),
        }


@admin.register(History)
class HistoryAdmin(CustomGeoAdmin):
    
    #form = HistoryForm    
    list_display = ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 'source_of_exposure')
    #list_display_links = ['code',]
    search_fields = [
        'registration_no', 'patient_id__first_name','patient_id__last_name','date_registered', 'date_of_exposure',
        'muni_id__muni_name','brgy_id__brgy_name','category_of_exposure','source_of_exposure','exposure_type',
        'bite_site','provoked_status','immunization_status__iexact','status_of_animal','confinement_status',
    ]
    # Define the field order in the form
    fields = (
        'patient_id', 'registration_no', 'date_registered', 'date_of_exposure', 'muni_id', 'brgy_id',
        'category_of_exposure', 'source_of_exposure', 'exposure_type', 'bite_site', 'provoked_status',
        'immunization_status', 'status_of_animal', 'confinement_status','washing_hands', 'human_rabies', 'latitude', 'longitude', 'geom'
    )#, 'latitude', 'longitude', 'geom'
    list_filter = (CodeForeign,'muni_id', 'brgy_id','category_of_exposure',)
    list_per_page = 5
    ordering = ('-patient_id',)

    #inlines = [HistoryInline, TreatmentInline]
    
    def get_latitude(self, obj):
        return obj.latitude
    get_latitude.short_description = 'Latitude'

    def get_longitude(self, obj):
        return obj.longitude
    get_longitude.short_description = 'Longitude'

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            queryset = queryset.filter(
                Q(patient_id__first_name__icontains=search_term) |
                Q(patient_id__middle_name__icontains=search_term) |
                Q(patient_id__last_name__icontains=search_term)
            ).select_related('patient_id') 
        return queryset, False  

    def get_list_display(self, request):
        if not request.GET.get('q'):  # When no search query
            if request.user.is_superuser:
                return ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 'source_of_exposure')
            else:
                return ('registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 'source_of_exposure')
        else:  # When search query is present
            return ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 'source_of_exposure')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is superuser, show all records
        if request.user.is_superuser:
            return qs     
        # If not searching, filter by the current user (for regular users)
        if not request.GET.get('q'):  # No search query
            return qs.filter(patient_id__user=request.user)       
        # Otherwise, show all records even if the user is not the owner (search case)
        return qs
    
    # Allow editing patients by ensuring the correct patient object is retrieved
    def get_object(self, request, object_id, from_field=None):
        try:
            # Get the patient by its ID, bypassing user-based filtering for editing
            return History.objects.get(pk=object_id)
        except History.DoesNotExist:
            return None  # Return None if the patient doesn't exist

    def get_search_results(self, request, queryset, search_term):
        # Allow search across all patients for all users, also show user code during search
        if search_term:
            queryset = queryset.filter(
                Q(patient_id__first_name__icontains=search_term) |
                Q(patient_id__middle_name__icontains=search_term) |
                Q(patient_id__last_name__icontains=search_term)
            ).select_related('patient_id')  # Pre-fetch user data, including the user code
        return queryset, False  # Return the modified queryset

    def get_fields(self, request, obj=None):
        fields = [
            'patient_id', 'registration_no', 'date_registered', 'date_of_exposure', 
            'muni_id', 'brgy_id', 'category_of_exposure', 'source_of_exposure', 
            'exposure_type', 'bite_site', 'provoked_status', 'immunization_status', 
            'status_of_animal', 'confinement_status', 'washing_hands', 
            'human_rabies', 'latitude', 'longitude', 'geom'
        ]
        if request.user.is_superuser:
            fields.remove('latitude')  # Remove `latitude` for superadmins
            fields.remove('longitude')  # Remove `longitude` for superadmins
            fields.remove('geom')  # Remove `geom` for superadmins
        return fields
 
    def patient_name(self, obj):
        return  f"{obj.patient_id.first_name} {obj.patient_id.last_name}"
    patient_name.short_description = 'Patient Name'

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return ('muni_id', 'brgy_id','category_of_exposure',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields]  # All fields read-only
            readonly_fields.remove('latitude')  # Remove `latitude` from readonly
            readonly_fields.remove('longitude')  # Remove `longitude` from readonly
            readonly_fields.remove('geom')  # `geom` will not be shown
            return readonly_fields
        return []# Regular users can edit all fields

    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return
        if not obj.pk:
            obj.patient_id.user = request.user
        super().save_model(request, obj, form, change)
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'patient_id':
            if not request.user.is_superuser:
                kwargs['queryset'] = Patient.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ['']

    class Media:
        css = {
            'all': ('admin/css/theadColor.css','admin/css/checkbox.css',) 
        }


@admin.register(Treatment)    
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'get_day0','day0_arrived_status', 'get_day3','day3_arrived_status', 'get_day7','day7_arrived_status',
                    'day28','tcv_given', 'rig_given','remarks')
                
    search_fields = ['patient_id__first_name','patient_id__last_name','vaccine_route__iexact','vaccine_generic_name']
    list_per_page = 5
    list_filter = [CodeForeign,DoctorFilter, 'patient_id__histories__category_of_exposure', 'vaccine_brand_name','vaccine_generic_name']

    # Exclude the 'day0_arrived' field from the form
    exclude = ('day0_arrived', 'day3_arrived', 'day7_arrived','day28_arrived',)
    ordering = ('-patient_id',)

    def day0_arrived_status(self, obj):
        return format_html('<b style="color: green;">✓</b>' if obj.day0_arrived else '<b style="color: red;">X</b>')
    day0_arrived_status.short_description = format_html("")

    def day3_arrived_status(self, obj):
        return format_html('<b style="color: green;">✓</b>' if obj.day3_arrived else '<b style="color: red;">X</b>')
    day3_arrived_status.short_description = format_html("")

    def day7_arrived_status(self, obj):
        return format_html('<b style="color: green;">✓</b>' if obj.day7_arrived else '<b style="color: red;">X</b>')
    day7_arrived_status.short_description = format_html("")


    # Custom methods to display Day 0, Day 3, Day 7 without extra labels in list display
    def get_day0(self, obj):
        return obj.day0
    get_day0.short_description = format_html(_("(Day0)<br>1st Dose"))

    def get_day3(self, obj):
        return obj.day3
    get_day3.short_description = format_html(_("(Day3)<br>2nd Dose"))

    def get_day7(self, obj):
        return obj.day7
    get_day7.short_description =format_html(_("(Day7)<br>3rd Dose"))

    # Customizing the form labels for add/edit views
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        
        if db_field.name == "day0":
            field.label = _("Day 0 (First Dose)")
        elif db_field.name == "day3":
            field.label = _("Day 3 (Second Dose)")
        elif db_field.name == "day7":
            field.label = _("Day 7 (Third Dose)")
        
        return field

    def get_search_results(self, request, queryset, search_term):
        # Allow search across all patients for all users, also show user code during search
        if search_term:
            queryset = queryset.filter(
                Q(patient_id__first_name__icontains=search_term) |
                Q(patient_id__middle_name__icontains=search_term) |
                Q(patient_id__last_name__icontains=search_term)
            ).select_related('patient_id')  # Pre-fetch user data, including the user code
        return queryset, False  # Return the modified queryset

    def get_list_display(self, request):
        
        # If not searching or for regular users, remove 'code' from the list view
        if not request.GET.get('q'):  # When no search query
            if request.user.is_superuser:
                return ('code', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'get_day0','day0_arrived_status', 'get_day3','day3_arrived_status', 'get_day7','day7_arrived_status',
                    'day28','tcv_given', 'rig_given','remarks')
            else:
                return ('patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'get_day0','day0_arrived_status', 'get_day3','day3_arrived_status', 'get_day7','day7_arrived_status',
                    'day28','tcv_given', 'rig_given','remarks')
        return ('code', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'get_day0','day0_arrived_status', 'get_day3','day3_arrived_status', 'get_day7','day7_arrived_status',
                    'day28','tcv_given', 'rig_given','remarks')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # If user is a superuser, show all records
        if request.user.is_superuser:
            return qs  
        
        # If there is a search query, do not filter by user ownership
        if request.GET.get('q'):
            return qs  # Allows search to show all results without filtering by user ownership
        
        # Filter by the current user if no search query is provided (regular access)
        return qs.filter(patient_id__user=request.user)

    # Allow editing patients by ensuring the correct patient object is retrieved
    def get_object(self, request, object_id, from_field=None):
        try:
            # Get the patient by its ID, bypassing user-based filtering for editing
            return Treatment.objects.get(pk=object_id)
        except Treatment.DoesNotExist:
            return None  # Return None if the patient doesn't exist


    def patient_name(self, obj):
        return  f"{obj.patient_id.first_name} {obj.patient_id.last_name}"
    patient_name.short_description = 'Patient Name'

    def get_search_fields(self, request):
        return ['patient_id__first_name', 'patient_id__last_name']

    def category_of_exposure(self, obj):
        return obj.get_category_of_exposure()
    category_of_exposure.short_description = 'Exposure Category'
    
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return  
        if not obj.pk:
            obj.patient_id.user = request.user
        super().save_model(request, obj, form, change)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return ('patient_id__histories__category_of_exposure', 'vaccine_brand_name','vaccine_generic_name')
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'treatment_id']
            return readonly_fields
        return self.readonly_fields
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):
        # Superusers always have permission
        if request.user.is_superuser:
            return False
        elif request.user.is_staff:
            return True

        # If there is a search query, allow change permission without checking ownership
        if request.GET.get('q'):
            return True
        
        # Otherwise, restrict to objects owned by the user
        return obj is not None and obj.patient_id.user == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """
       
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            return {}  
        return actions

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'patient_id':
            if not request.user.is_superuser:
                kwargs['queryset'] = Patient.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)\
    
    def mark_day0(self, request, queryset):
        for treatment in queryset:
            treatment.day0_arrived = not treatment.day0_arrived
            treatment.day0 = datetime.today()
            treatment.save()
    mark_day0.short_description = "Day0(First Dose)"

    def mark_day3(self, request, queryset):
        for treatment in queryset:
            treatment.day3_arrived = not treatment.day3_arrived
            treatment.day3 =datetime.today()
            treatment.save()
    mark_day3.short_description = "Day3(Second Dose)"

    def mark_day7(self, request, queryset):
        for treatment in queryset:
            treatment.day7_arrived = not treatment.day7_arrived
            treatment.day7 = datetime.today()
            treatment.save()
    mark_day7.short_description = "Day7(Third Dose)"

    def mark_day28(self, request, queryset):
        for treatment in queryset:
            treatment.day28_arrived = not treatment.day28_arrived
            treatment.save()
    mark_day28.short_description = "Day 28"

    def mark_as_animal(self,request,queryset):
        for treatment in queryset:
            treatment.animal_alive = not treatment.animal_alive
            treatment.save()
    mark_as_animal.short_description = "Animal is Dead"

    actions = ['mark_day0','mark_day3','mark_day7','mark_day28', 'mark_as_animal',]

    class Media:
        css = {
            'all': ('admin/css/theadColor.css','admin/css/checkbox.css',) 
        }

@admin.register(Barangay)
class BarangayAdmin(CustomGeoAdmin):
    list_display = ('muni_id','brgy_name',)#'tmp_muni'
    list_filter = ['muni_id','brgy_name',]
    #search_fields = ['brgy_name','muni_id']
    ordering = ('muni_id__muni_name','brgy_name') 
    list_per_page = 10
    exclude = ('boundary',)
    
    def muni_name(self, obj):
        return  f"{obj.muni_id.muni_name}"
    muni_name.short_description = 'Municipality Name'

    def get_search_fields(self, request):
        return ['muni_id__muni_name','brgy_name']

    """ def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False """
    """ return super().has_change_permission(request, obj) """

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """
    
    class Media:
        js = ('assets/js/admin.js',)
        css = {
            'all': ('assets/css/admin.css','admin/css/theadColor.css','admin/css/checkbox.css',) 
            
        }
        
        
@admin.register(Municipality)
class MunicipalityAdmin(CustomGeoAdmin):
    list_display = ('muni_name',)#'muni_logo'
    fields = ('muni_name',)#'logo'
    ordering = ('muni_name',)
    exclude = ('geom',)

    """ def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False """
    """ return super().has_change_permission(request, obj) """

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """

    class Media:
        css = {
            'all': ('admin/css/theadColor.css','admin/css/checkbox.css',) 
        }

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_flag','object_repr', 'content_type','action_time', )
    fields = ('user', 'action_flag','object_repr', 'content_type','action_time',)
    list_filter = ('user__code', 'action_flag')
    search_fields = ('object_repr', 'change_message','user','action_flag')
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'treatment_id']
            return readonly_fields
        return self.readonly_fields
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    """ def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj) """
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)
    
    class Media:
        css = {
            'all': ('admin/css/theadColor.css','admin/css/checkbox.css',) 
        }

admin.site.register(LogEntry, LogEntryAdmin)

# Override UserAdmin
@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password",'logo_image','code')}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email","number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username",  "password1", "password2","code"),#"usable_password",
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "first_name", "last_name", "email", "code", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email", "code")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    # Method to display logo image thumbnail
    def image_logo_display(self, obj):
        if obj.logo_image:
            return mark_safe(f'<img src="{obj.logo_image.url}" width="50" height="50" />')
        return "No Logo"
    image_logo_display.short_description = "Municipality Logo"
    
    # Override to prevent non-superusers from accessing "Change" pages
    def has_change_permission(self, request, obj=None):
        """
        Only superusers can access the 'Change' functionality.
        """
        if request.user.is_superuser:
            return True
        return False
    
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets  # When adding a user
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)  # Show all fields for superadmin
        return (
            ("General", {"fields": ("username", "code","logo_image")}),
            ("Personal info", {"fields": ("first_name", "last_name", "email","number")}),
        )
    
    def get_readonly_fields(self, request, obj=None):
        """
        Restrict editing of certain fields for non-superusers.
        """
        if request.user.is_superuser:
            return ()  # Superuser has no readonly fields
        # For non-superusers, restrict editing of specific fields
        return ("username", "first_name", "last_name", "email","code","number","logo_image")

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ("is_staff", "is_superuser", "groups")
        else:
            return ("is_staff", "is_superuser")
        
    # Restrict 'Add' button to superusers only
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    # Restrict 'Delete' button to superusers only
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter out session and contenttypes permissions
        if 'user_permissions' in form.base_fields:
            content_type_ids = ContentType.objects.filter(
                model__in=['session', 'contenttype']
            ).values_list('id', flat=True)

            form.base_fields['user_permissions'].queryset = Permission.objects.exclude(content_type_id__in=content_type_ids)
        return form

    class Media:
        css = {
            'all': ('admin/css/theadColor.css','admin/css/checkbox.css',) 
        }

class CustomGroupAdmin(GroupAdmin):
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions",)
    
    # To optimize the permissions form field, similar to what you did in the original GroupAdmin
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "permissions":
            qs = kwargs.get("queryset", db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs["queryset"] = qs.select_related("content_type")
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter out session and contenttypes permissions
        if 'permissions' in form.base_fields:
            content_type_ids = ContentType.objects.filter(
                model__in=['session', 'contenttype']
            ).values_list('id', flat=True)

            form.base_fields['permissions'].queryset = Permission.objects.exclude(content_type_id__in=content_type_ids)
        return form

    class Media:
        css = {
            'all': ('admin/css/theadColor.css','admin/css/checkbox.css',) 
        }

if admin.site.is_registered(DefaultUserAdmin):
    admin.site.unregister(get_user_model())

if admin.site.is_registered(Group):
    admin.site.unregister(Group)
# Register CustomGroup model with CustomGroupAdmin
admin.site.register(Group, CustomGroupAdmin)
