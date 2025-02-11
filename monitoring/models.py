from django import forms
from django.db import models
from datetime import datetime,date,timedelta
import os, random
from django.utils.html import mark_safe
from django.utils import timezone
from django.contrib import admin
from django.db.models import Q  
from functools import reduce  
import operator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from django.contrib.gis.db import models
from django.contrib.gis.db import models as geomodels
from django.db.models.signals import post_save
from django.db.models import OuterRef, Subquery
from django.utils.safestring import mark_safe as safe_mark
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.contrib.auth.models import Permission,PermissionsMixin

def validate_contact_number(value):
    if not value.startswith('09') or len(value) != 11:
        raise ValidationError(
            _('Invalid contact number: %(value)s. It should start with "09" and be 11 digits long.'),
            params={'value': value},
            
        )



class Municipality(models.Model):
    muni_id = models.AutoField(primary_key=True)
    muni_name = models.CharField(max_length=100,blank=False, verbose_name="Municipality Name")
    geom = geomodels.MultiPolygonField(verbose_name="Geom", null=True, blank=True)
    #logo = models.ImageField(upload_to='municipality_logo', null=True, blank=True, verbose_name="Municipality Logo")

    def muni_logo(self):
        """Display the logo thumbnail in Django admin."""
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" width="50" />')
        return "No Logo"
    muni_logo.short_description = "Municipality Logo"

    def save(self, *args, **kwargs):
        self.muni_name = self.muni_name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.muni_name}"
    class Meta:
        verbose_name_plural = "Municipalities"

class Barangay(models.Model):
    brgy_id = models.AutoField(primary_key=True)
    brgy_name = models.CharField(max_length=100,blank=False, verbose_name="Barangay Name")
    muni_id = models.ForeignKey(Municipality,blank=False, on_delete=models.CASCADE, verbose_name="Municipality Name",related_name='barangays',db_column='muni_id')
    boundary = geomodels.MultiPolygonField(verbose_name="Boundary",blank=True, srid=4326,null=True)  # SRID 4326 is the standard for WGS 84, used by GPS

    def save(self, *args, **kwargs):
        exceptions = ['lo-ok',]  # Add other barangays that need specific casing
        if self.brgy_name.lower() in exceptions:
            self.brgy_name = self.brgy_name.lower()  # retain original casing
        else:
            # Capitalize only the first letter of the entire barangay name
            self.brgy_name = ' '.join([word.capitalize() if '-' not in word else word for word in self.brgy_name.split()])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brgy_name}, {self.muni_id.muni_name}"

    class Meta:
        verbose_name_plural = "Barangays"
        # Enforce uniqueness for the combination of brgy_name and muni_id
        unique_together = ['brgy_name', 'muni_id']  

class User(AbstractUser):
    # Add the custom field 'code' here
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    number = models.CharField(max_length=12,blank=False, verbose_name="Contact Number", validators=[validate_contact_number],)
    email = models.EmailField(_("email address"), blank=False)
    code_choices = (
        ('ALM','ALM'),
        ('BIL','BIL'),
        ('CABUC','CABUC'),
        ('CAIB','CAIB'),
        ('CUL','CUL'),
        ('KAW','KAW'),
        ('MAR','MAR'),
        ('NAV','NAV'),
    )
    code = models.CharField(verbose_name="code",choices=code_choices, max_length=20, blank=True)
    logo_image = models.ImageField(upload_to='municipality_logo', null=True, blank=True, verbose_name="Municipality Logo")

    groups = models.ManyToManyField(
        Group,  # Reference CustomGroup here
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="customuser_set",  # Set a unique related name
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="customuser_set_permissions",  # Unique related name for permissions
        related_query_name="customuser_permission",
    )

    def save(self,*args,**kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super().save(*args,**kwargs)


    def image_logo(self):
        """Display the logo thumbnail in Django admin."""
        if self.logo_image:
            return mark_safe(f'<img src="{self.logo_image.url}" width="50" />')
        return "No Logo"
    image_logo.short_description = "Municipality Logo"

    def __str__(self):
        return self.username 

  
    
class Doctor(models.Model):

    SPECIALIZATION_CHOICES = (
        ('gp', 'General Practitioner'),
        ('pediatrician', 'Pediatrician'),
        ('dermatologist', 'Dermatologist'),
        ('cardiologist', 'Cardiologist'),
        ('orthopedic', 'Orthopedic Surgeon'),
        ('obgyn', 'Obstetrician/Gynecologist'),
        ('endocrinologist', 'Endocrinologist'),
        ('neurologist', 'Neurologist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('psychiatrist', 'Psychiatrist'),
    )
    #user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User",default=1, related_name='doctors')
    first_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="First Name")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Middle Name")
    last_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Last Name")
    specialization = models.CharField(blank=True,choices=SPECIALIZATION_CHOICES, null=True, verbose_name="Specialization")
    sex_choice =(
        ('male','Male'),
        ('female','Female'),
    )
    gender = models.CharField(choices=sex_choice, max_length=20,null=True, verbose_name="Sex")
    
    contact_number = models.CharField(max_length=12, validators=[validate_contact_number], blank=True, verbose_name="Contact Number")
    email = models.EmailField( blank=False, null=False, verbose_name="Email")
    licensed = models.CharField(unique=True,blank=False,null=False, verbose_name="Licensed Number")
    muni_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name="Municipality", related_name='doctors_muni')#7 cabucgayan,6 culaba, 5 almeria, 8 kaw
    brgy_id = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True,verbose_name="Barangay",related_name='doctors_brgy')
    is_superdoctor = models.BooleanField(default=False, verbose_name="Lead  Doctor")  # New attribute


    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()  # Capitalize first letter
        self.middle_name = self.middle_name.title()
        self.last_name = self.last_name.title()  
        super().save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()
    full_name.short_description = "Full Name"

    def __str__(self):
        return f"Dr. {self.full_name()}"

    class Meta:
        verbose_name_plural = "Doctors"

class Patient(models.Model):
    #app_label = 'monitoring'
    STREET_CHOICES = [
        ("Abad Street", "Abad Street"),
        ("Adobo Compound Road", "Adobo Compound Road"),
        ("Ballesteros Street", "Ballesteros Street"),
        ("Biliran Circumferential Road", "Biliran Circumferential Road"),
        ("Biliran Rotunda", "Biliran Rotunda"),
        ("Bonifacio Street", "Bonifacio Street"),
        ("Burgos Street", "Burgos Street"),
        ("Cabadiangan Road", "Cabadiangan Road"),
        ("Calambis Bridge", "Calambis Bridge"),
        ("Caneja Street", "Caneja Street"),
        ("Castin Street", "Castin Street"),
        ("Corvera Street", "Corvera Street"),
        ("Garrido", "Garrido"),
        ("Gomez", "Gomez"),
        ("Imelda Road", "Imelda Road"),
        ("Jaguros Street", "Jaguros Street"),
        ("Leyte-Biliran Road", "Leyte-Biliran Road"),
        ("Lico Road", "Lico Road"),
        ("Limpiado", "Limpiado"),
        ("Lomboy Road", "Lomboy Road"),
        ("Looc Diversion Road", "Looc Diversion Road"),
        ("Mabini Pier", "Mabini Pier"),
        ("Mabini Street", "Mabini Street"),
        ("Magallanes Street", "Magallanes Street"),
        ("Mapuyo Loop", "Mapuyo Loop"),
        ("Maripipi Circumferential Road", "Maripipi Circumferential Road"),
        ("Mission", "Mission"),
        ("Naval-Caibiran Cross Country Road", "Naval-Caibiran Cross Country Road"),
        ("Padre Garcia Street", "Padre Garcia Street"),
        ("Padre Innocentes Street", "Padre Innocentes Street"),
        ("Real Street", "Real Street"),
        ("Redaza Street", "Redaza Street"),
        ("Rizal Street", "Rizal Street"),
        ("Rojas Street", "Rojas Street"),
        ("Sabenorio Street", "Sabenorio Street"),
        ("Salazar", "Salazar"),
        ("Salut", "Salut"),
        ("San Isidro Street", "San Isidro Street"),
        ("San Juan Street", "San Juan Street"),
        ("San Roque Street", "San Roque Street"),
        ("Santa Cruz Street", "Santa Cruz Street"),
        ("Santissimo Rosario", "Santissimo Rosario"),
        ("Santo Niño Road", "Santo Niño Road"),
        ("Sitio Hayahay Road", "Sitio Hayahay Road"),
        ("Sitio Lupa Road", "Sitio Lupa Road"),
        ("Vicentillo Extension", "Vicentillo Extension"),
        ("Vicentillo Street", "Vicentillo Street"),
        ("Zamora", "Zamora"),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="User", related_name='patients')
    
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200, verbose_name="First Name", blank=False,)
    middle_name = models.CharField(max_length=200, verbose_name="Middle Name",blank=False,)
    last_name = models.CharField(max_length=200, verbose_name="Last Name", blank=False)
    muni_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, blank=False,verbose_name="Municipality", related_name='patients_muni')#7 cabucgayan,6 culaba, 5 almeria, 8 kaw
    brgy_id = models.ForeignKey(Barangay, on_delete=models.CASCADE, blank=False,null=True, verbose_name="Barangay",related_name='patients_brgy')#88 Caib, 50 cabuc, 47 kaw, 67 cula
    street = models.CharField(
        max_length=100,
        choices=STREET_CHOICES,
        blank=True,
        null=True,
    )
    birthday = models.DateField(verbose_name="Birthday", )#default=date(2001, 12, 2)
    sex_choice =(
        ('male','Male'),
        ('female','Female'),
    )
    sex = models.CharField(choices=sex_choice, max_length=20,blank=False, verbose_name="Sex")#default='male',
    contactNumber = models.CharField(max_length=12, blank=False, verbose_name="Contact Number",validators=[validate_contact_number],)#default= '09582488441',

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()  # Capitalize first letter
        self.middle_name = self.middle_name.title()
        self.last_name = self.last_name.title()  
        super().save(*args, **kwargs)
    
    def code(self):
        return self.user.code
    code.short_description = 'Code'

    """ def registration_no(self):
        history = History.objects.filter(patient_id=self.patient_id).first()
        return history.registration_no if history else 'N/A' """

    def get_age(self):
        """Calculate age based on birthday."""
        today = date.today()
        age = today.year - self.birthday.year
        if today.month < self.birthday.month or (today.month == self.birthday.month and today.day < self.birthday.day):
            age -= 1
        return age
    
    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    class Meta:
        #ordering = ['-patient_id__registration_no']
        verbose_name_plural = "Patient Records"
        app_label = 'monitoring'

class History(models.Model):

    history_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Patient", related_name='histories',db_column='patient_id')
    registration_no = models.CharField(max_length=200,verbose_name='Registration Number', blank=True, null=True,)#unique=True, 
    #treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE, verbose_name="Treatment",default=1,  related_name='history_treatment', db_column='treatment_id')
    date_registered = models.DateField(verbose_name="Date Registered",blank=False,)#default=date(2024,9,1),
    date_of_exposure = models.DateField(blank=False, null=True, verbose_name="Date of Exposure")#default=date(2024, 8, 16),
    muni_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, blank=False,verbose_name="Municipality of Exposure", related_name='history_muni',db_column='muni_id')#default=1,
    brgy_id = models.ForeignKey(Barangay, on_delete=models.CASCADE, blank=False, null=True,verbose_name="Barangay Exposure", related_name='history_brgy',db_column='brgy_id')#default=1,
    
    category = (
        ('I','I'),
        ('II',"II"),
        ('III','III'),
    )
    category_of_exposure = models.CharField(max_length=10,blank=False, choices=category,verbose_name="Exposure Category" )#default="II",

    source_of_exposure_choices = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Bat', 'Bat'),
        ('Monkey', 'Monkey'),
        ('Human', 'Human'),
        ('Horse', 'Horse'),
        ('Cow', 'Cow'),
        ('Goat', 'Goat'),
        ('Pig', 'Pig'),
        ('Rabbit', 'Rabbit'),
        ('Guinea Pig', 'Guinea Pig'),
    )

    exposure_type_choices = (
        ('Bite', 'Bite'),
        ('Non-Bite', 'Non-Bite'),
    )

    bite_site_choices = (
        # Head and Face
        ('Front of Head', 'Front of Head'),
        ('Back of Head', 'Back of Head'),
        ('Face', 'Face'),
        ('Jaw', 'Jaw'),
        ('Mouth', 'Mouth'),
        ('Eye', 'Eye'),
        ('Cheek', 'Cheek'),
        ('Forehead', 'Forehead'),
        ('Temple', 'Temple'),
        ('Behind Ear', 'Behind Ear'),

        # Neck and Shoulders
        ('Front of Neck', 'Front of Neck'),
        ('Back of Neck', 'Back of Neck'),
        ('Shoulder (Left)', 'Shoulder (Left)'),
        ('Shoulder (Right)', 'Shoulder (Right)'),

        # Arms and Hands
        ('Upper Arm (Left)', 'Upper Arm (Left)'),
        ('Upper Arm (Right)', 'Upper Arm (Right)'),
        ('Elbow (Left)', 'Elbow (Left)'),
        ('Elbow (Right)', 'Elbow (Right)'),
        ('Forearm (Left)', 'Forearm (Left)'),
        ('Forearm (Right)', 'Forearm (Right)'),
        ('Wrist (Left)', 'Wrist (Left)'),
        ('Wrist (Right)', 'Wrist (Right)'),
        ('Palm (Left)', 'Palm (Left)'),
        ('Palm (Right)', 'Palm (Right)'),
        ('Back of Hand (Left)', 'Back of Hand (Left)'),
        ('Back of Hand (Right)', 'Back of Hand (Right)'),
        ('Thumb (Left)', 'Thumb (Left)'),
        ('Thumb (Right)', 'Thumb (Right)'),
        ('Index Finger (Left)', 'Index Finger (Left)'),
        ('Index Finger (Right)', 'Index Finger (Right)'),
        ('Middle Finger (Left)', 'Middle Finger (Left)'),
        ('Middle Finger (Right)', 'Middle Finger (Right)'),
        ('Ring Finger (Left)', 'Ring Finger (Left)'),
        ('Ring Finger (Right)', 'Ring Finger (Right)'),
        ('Little Finger (Left)', 'Little Finger (Left)'),
        ('Little Finger (Right)', 'Little Finger (Right)'),

        # Chest and Abdomen
        ('Chest (Front)', 'Chest (Front)'),
        ('Chest (Side)', 'Chest (Side)'),
        ('Abdomen (Front)', 'Abdomen (Front)'),
        ('Lower Back', 'Lower Back'),

        # Hips and Legs
        ('Hip (Left)', 'Hip (Left)'),
        ('Hip (Right)', 'Hip (Right)'),
        ('Thigh (Left, Front)', 'Thigh (Left, Front)'),
        ('Thigh (Left, Back)', 'Thigh (Left, Back)'),
        ('Thigh (Right, Front)', 'Thigh (Right, Front)'),
        ('Thigh (Right, Back)', 'Thigh (Right, Back)'),
        ('Knee (Left, Front)', 'Knee (Left, Front)'),
        ('Knee (Left, Back)', 'Knee (Left, Back)'),
        ('Knee (Right, Front)', 'Knee (Right, Front)'),
        ('Knee (Right, Back)', 'Knee (Right, Back)'),
        ('Calf (Left)', 'Calf (Left)'),
        ('Calf (Right)', 'Calf (Right)'),
        ('Leg (Left)', 'Leg (Left)'),
        ('Leg (Right)', 'Leg (Right)'),
        ('Leg Lower(Left)', 'Leg Lower(Left)'),
        ('Leg Lower(Right)', 'Leg Lower(Right)'),
        ('Leg Upper(Left)', 'Leg Upper(Left)'),
        ('Leg Upper(Right)', 'Leg Upper(Right)'),
        ('Leg Anterior(Left)', 'Leg Anterior(Left)'),
        ('Leg Anterior(Right)', 'Leg Anterior(Right)'),
        ('Leg Posterior(Left)', 'Leg Posterior(Left)'),
        ('Leg Posterior(Right)', 'Leg Posterior(Right)'),
        # Ankles and Feet
        ('Ankle (Left)', 'Ankle (Left)'),
        ('Ankle (Right)', 'Ankle (Right)'),
        ('Foot (Left)', 'Foot (Left)'),
        ('Foot (Right)', 'Foot (Right)'),
        ('Toes (Left)', 'Toes (Left)'),
        ('Toes (Right)', 'Toes (Right)'),
        ('Ball of Foot (Left)', 'Ball of Foot (Left)'),
        ('Ball of Foot (Right)', 'Ball of Foot (Right)'),
        ('Heel (Left)', 'Heel (Left)'),
        ('Heel (Right)', 'Heel (Right)'),
    )

    provoked_choices = (
        ('Provoked', 'Provoked'),
        ('Unprovoked', 'Unprovoked'),
    )
    
    immunization_choices = (
        ('Immunized', 'Immunized'),
        ('Unimmunized', 'Unimmunized'),
    )
    
    status_of_animal_choices = (
        ('Alive','Alive'),
        ('Dead','Dead'),
        ('Killed','Killed'),
        ('Lost','Lost'),
    )
    
    animal_status = (
        ('Stray','Stray'),
        ('Leashed/Caged','Leashed/Caged'),
    )
    
    washing = (
        ('Yes','Yes'),
        ('No','No'),
    )
    source_of_exposure = models.CharField(max_length=10 ,choices=source_of_exposure_choices,  blank=False, verbose_name="Animal")#default='Cat',
    exposure_type = models.CharField(max_length=10, choices=exposure_type_choices,  blank=False, verbose_name="Type of Exposure")#default='Bite',
    bite_site = models.CharField(max_length=50, choices=bite_site_choices, blank=False,null=False, verbose_name="Bite Site")
    provoked_status = models.CharField(max_length=20, choices=provoked_choices,blank=False,verbose_name="Provocation Status")#default='Unprovoked' ,
    immunization_status = models.CharField(max_length=20, choices=immunization_choices,blank=False, verbose_name="Animal Vaccination")#default='Unimmunized',
    status_of_animal = models.CharField(max_length=20,choices=status_of_animal_choices,blank=False, verbose_name="Animal Status")#default='Lost',
    confinement_status = models.CharField(max_length=20,choices=animal_status,blank=False, verbose_name="Confinement Status")#default='Stray',
    washing_hands = models.CharField(max_length=10,choices=washing,blank=False,verbose_name="Washing Wound")#default='Yes' ,
    human_rabies = models.BooleanField(default=False,verbose_name="Human Rabies")
    latitude = models.FloatField(verbose_name="Latitude", blank=True, null=False, default=0.0)
    longitude = models.FloatField(verbose_name="Longitude", blank=True, null=False, default=0.0)
    geom= geomodels.PointField(verbose_name="Geometry",  null=True, blank=False)



    def save(self, *args, **kwargs):
        if self.geom:
            # Automatically set latitude and longitude from geom if geom is set
            self.latitude = self.geom.y
            self.longitude = self.geom.x
        else:
            # Ensure latitude and longitude are set
            if self.latitude is None or self.longitude is None:
                raise ValueError("Both latitude and longitude must be set if geom is not provided.")
        
        if not self.registration_no:
            self.registration_no = self.generate_registration_no()
        self.registration_no = self.registration_no.upper()  # Convert to uppercase
        self.bite_site = self.bite_site.title()  # Capitalize first letter

        super().save(*args, **kwargs)

    def generate_registration_no(self):
        current_year = date.today().year
        user_id = self.patient_id.user.id
    
        # Filter histories for the current year and user, and get the last registration number
        last_history = History.objects.filter(
            patient_id__user__id=user_id,
            registration_no__startswith=f'{current_year}-'
        ).order_by('registration_no').last()

        if last_history:
            last_reg_no = last_history.registration_no
            last_reg_num = int(last_reg_no.split('-')[-1])
            new_reg_num = last_reg_num + 1
        else:
            new_reg_num = 1

        new_registration_no = f'{current_year}-{new_reg_num:05d}'
        return new_registration_no

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Specify the fields you want to search for names
            search_fields = ['patient_id__first_name', 'patient_id__last_name']
            
            # Split the search term into individual characters
            terms = search_term.strip().split()
            for term in terms:
                or_queries = [Q(**{f'{field}__icontains': term}) for field in search_fields]
                queryset = queryset.filter(reduce(operator.or_, or_queries))

        return queryset, use_distinct
    
    def code(self):
        return self.patient_id.user.code
    code.short_description = 'Code'

    def __str__(self):
        return '{} - Registered on {} - Source: {}'.format(
            self.patient_id,
            self.date_registered,
            self.source_of_exposure
            )
    
    class Meta:
        verbose_name_plural = "Patient's History"
        ordering = ['-registration_no']
        unique_together = ('registration_no', 'patient_id')  # Ensure registration_no is unique per patient

class Treatment(models.Model):
    
    treatment_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Doctor",blank=False,null=True, related_name='doctors_patient')
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE,blank=False, verbose_name="Patient", related_name='treatments_patient', db_column='patient_id')
    #history_id = models.ForeignKey(History, on_delete=models.CASCADE,s verbose_name="History", related_name='treatment_history', db_column='history_id')
    
    GENERIC_NAME = (
        ('PCECCV', 'PCECCV'),
        ('PVRV', 'PVRV'),
    )
    BRAND_NAME = (
        ('Verorab', 'Verorab'),
        ('Speeda', 'Speeda'),
        ('Vaxirab', 'Vaxirab'),
        ('Abhayrab', 'Abhayrab'),
    )
    route = (
        ('intramuscular', 'Intramuscular'),
        ('intradermal', 'Intradermal')
    )
    outcome_choices = (
        # Animal-related remarks
        ('Completed', 'Completed'),
        ('Incomplete', 'Incomplete'),
        ('Died', 'Died'),
        ('None', 'None'),
    )
    
    vaccine_generic_name = models.CharField(max_length=10,blank=False, choices=GENERIC_NAME,  verbose_name='Vaccine Generic Name')  # PCECCV or PVRV
    vaccine_brand_name = models.CharField(max_length=10,blank=False, choices=BRAND_NAME, verbose_name='Vaccine Brand Name')  # Verorab, Speeda, etc.
    vaccine_route = models.CharField(max_length=50,blank=False, choices=route, verbose_name='Vaccine Route')  # Route of administration

    tcv_given = models.DateField(blank=True, null=True, verbose_name="TCV")

    day0 = models.DateField( blank=True, null=True, verbose_name="Day 0(First Dose)")#default=date(2024,4,3),
    day0_arrived = models.BooleanField(default=False, verbose_name="") 

    day3 = models.DateField( blank=True, null=True, verbose_name="Day 3(Second Dose)")#default=date(2024,4,6),
    day3_arrived = models.BooleanField(default=False, verbose_name="")

    day7 = models.DateField(blank=True, null=True, verbose_name="Day 7(Third Dose)")#default=day7_str, default=date(2024,4,10), 
    day7_arrived = models.BooleanField(default=False, verbose_name="")

    day14 = models.DateField(blank=True, null=True, verbose_name="Day 14")
    
    day28 = models.DateField(blank=True, null=True, verbose_name="Day 28")
    
    #day28_arrived = models.BooleanField(default=False, verbose_name="")

    booster1 = models.DateField(blank=True,null=True, verbose_name="Booster1")
    booster2 = models.DateField(blank=True,null=True, verbose_name="Booster2")

    
    hrig_given = models.DateField(blank=True, null=True, verbose_name="HRIG")
    rig_given = models.DateField(blank=True, null=True, verbose_name="ERIG")

    animal_alive = models.BooleanField(blank=False, null=True, verbose_name='Animal alive')#default=True,
    remarks = models.CharField(max_length=100,blank=True,null=True,choices=outcome_choices,verbose_name="Remarks")


    def code(self):
        return self.patient_id.user.code
    code.short_description = 'Code'
    
    

    def get_category_of_exposure(self):
        history = History.objects.filter(patient_id=self.patient_id).first()
        return history.category_of_exposure if history else 'N/A'
    
    def registration_no(self):
        history = History.objects.filter(patient_id=self.patient_id).first()
        return history.registration_no if history else 'N/A'
    registration_no.short_description = "Registration Number"

    class Meta:
        ordering = ['-patient_id']
        verbose_name_plural = "Patient's Treatment"

    def __str__(self):
        return f"Treatment for {self.patient_id.first_name} {self.patient_id.last_name} on his/her {self.day0}"
