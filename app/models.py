import datetime
import random
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from django.utils import timezone




class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        extra_fields.setdefault('first_name', 'admin')
        extra_fields.setdefault('last_name', 'admin')
        extra_fields.setdefault('id_number', '1')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    # phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    # is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    first_name   = models.CharField(max_length=30, verbose_name='Nombre')
    last_name    = models.CharField(max_length=30, verbose_name='Apellido')
    # address      = models.CharField(blank=True, max_length=64, verbose_name='address')
    # mobile_phone = models.CharField(validators=[phone_regex], blank=True, max_length=16, verbose_name='mobile phone')
    id_number    = models.IntegerField(verbose_name='ID number', default=0)
    role_choice  = [ ('Cliente', 'Cliente') ]
    role         = models.CharField(choices=role_choice, max_length=9, blank=True)
    company      = models.ForeignKey('Company', related_name="employees", null=True) 

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def canVerify(self):
        return not (self.verified or self.id_front or self.selfie_image)

    @property
    def owners(self):
      return [self]
    

class Company(models.Model):
  name = models.CharField(max_length=30, verbose_name='Nombre de la compañia')
  rif  = models.CharField(primary_key= True, max_length=30, verbose_name='RIF')

  def __str__(self):
    return self.name

  @property
  def owners(self):
    return self.employees.all()

class Terrain(models.Model):
  city        = models.CharField(max_length=30, verbose_name='Ciudad')
  country     = models.CharField(max_length=30, verbose_name='País')
  coordinates = models.CharField(max_length=30, verbose_name='Coordenadas')
  name        = models.CharField(max_length=30, verbose_name='Nombre')
  is_active   = models.CharField(max_length=30, verbose_name='Activo')
  owned_by    = models.ForeignKey(Company, related_name="terrains")

  def __str__(self):
    return self.name

  @property
  def owners(self):
    return self.owned_by.employees.all()

class Crop(models.Model):
  tipo          = models.CharField(max_length=30, verbose_name='Tipo')
  variety       = models.CharField(max_length=30, verbose_name='Variedad')
  name          = models.CharField(max_length=30, verbose_name='Nombre')
  density       = models.FloatField(verbose_name='Densidad', default=1) 
  distance      = models.FloatField(verbose_name='Distancia entre plantas', default=0)  
  coordinates   = models.CharField(max_length=30, verbose_name='Coordenadas')
  number_plants = models.IntegerField(verbose_name='Número de plantas', default=0)
  sown_area     = models.FloatField(verbose_name='Area Sembrada', default=0)
  inside_of     = models.ForeignKey(Terrain, related_name="crops")

  def __str__(self):
    return self.name

  @property
  def owners(self):
    return self.inside_of.owned_by.employees.all()

class Weather(models.Model):
  eto             = models.FloatField(verbose_name='Evapotranspiración', default=0)
  co2             = models.FloatField(verbose_name='Dióxido de carbono', default=0)
  date            = models.DateField(default=datetime.date.today, verbose_name='Fecha')
  station         = models.CharField(max_length=30, verbose_name='Estación meteorológica')
  precipitation   = models.FloatField(verbose_name='Precipitación', default=0)
  min_temperature = models.FloatField(verbose_name='Temperatura mínima', default=0)
  max_temperature = models.FloatField(verbose_name='Temperatura máxima', default=0)
  radiation       = models.FloatField(verbose_name='Radiación', default=0)
  min_humidity    = models.FloatField(verbose_name='Humedad mínima', default=0)
  max_humidity    = models.FloatField(verbose_name='Humedad máxima', default=0)
  wind_speed      = models.FloatField(verbose_name='Velocidad del viento', default=0)
  terrain         = models.ForeignKey(Terrain, related_name="weather_reports")

  def __str__(self):
    return "Reporte Clima %s, %s" %(self.id, self.terrain)

  @property
  def owners(self):
    return self.terrain.owned_by.employees.all()

class Production(models.Model):
  code        = models.CharField(primary_key=True, max_length=30)
  date        = models.DateField(default=datetime.date.today, verbose_name="Fecha inicial")
  tah         = models.FloatField(verbose_name="Tonelada de azucar por hectarea")
  tch         = models.FloatField(verbose_name="Tonelada de caña por hectarea")
  pfh         = models.FloatField(verbose_name="Porcetanje de Fibra por hectarea")
  rend_ha     = models.FloatField(verbose_name="Rendimiento por Hectarea")
  brix        = models.FloatField(verbose_name="Grados Brix")
  pol         = models.FloatField(verbose_name='Porcentaje de sacarosa', default=0)
  pressing    = models.FloatField(verbose_name="Molienda en toneladas")
  purity      = models.FloatField(verbose_name="Porcetanje de pureza")
  days_zafra  = models.IntegerField(verbose_name="Duración de la zafra")
  ground_cane = models.FloatField(verbose_name="Toneladas de caña molida")
  rend_cane   = models.FloatField(verbose_name="Rendimiento de la caña")
  crop        = models.ForeignKey(Crop, verbose_name="Proviene de", related_name="productions")



  def __str__(self):
    return "Producción %s, %s" %(self.id, self.crop)

  @property
  def owners(self):
    return self.crop.inside_of.owned_by.employees.all()

class Payment(models.Model):
  code    = models.CharField(primary_key=True, max_length=30)
  amount  = models.FloatField(verbose_name='Monto', default=0)
  date    = models.DateField(auto_now_add=True, verbose_name='Fecha')
  service = models.CharField(max_length=30, verbose_name='Servicio')
  user    = models.ForeignKey(User, verbose_name="Usuario", related_name="payments")
  crop    = models.ForeignKey(Crop, verbose_name="Cultivo")

  def __str__(self):
    return str(self.code)
  @property
  def owners(self):
    return [self.user].all()

class Affection(models.Model):
  code        = models.CharField(primary_key=True, max_length=30)
  description = models.CharField(max_length=128)
  type_choice = ( ('Rolla', 'Rolla'), ('Candelilla', 'Candelilla'), ('Estrés hídrico', 'Estrés hídrico') )
  type        = models.CharField(choices=type_choice, max_length=9, blank=True)

  def __str__(self):
    return self.code

  @property
  def owners(self):
    return self.diagnostic.crop.inside_of.owned_by.employees.all()

class LocatedIn(models.Model):
  affection = models.ForeignKey(Affection, verbose_name="Affección")
  diagnostic = models.ForeignKey("Diagnostic", verbose_name="Diagnóstico", related_name="locatedIn")
  coordinates = models.CharField(max_length=30, verbose_name='Coordenadas')

  class Meta():
        auto_created=True

class Diagnostic(models.Model):
  code       = models.CharField(primary_key=True, max_length=30)
  date       = models.DateField(default=datetime.date.today, verbose_name='Fecha')
  crop       = models.ForeignKey(Crop, related_name="diagnostics")
  affections = models.ManyToManyField(Affection, related_name="diagnostics", through=LocatedIn)

  @property
  def owners(self):
    return self.crop.inside_of.owned_by.employees.all()

#<------------ Activity ----------------------------------------

class Activity(models.Model):
  date        = models.DateField(default=datetime.date.today, verbose_name='Fecha')
  coordinates = models.CharField(primary_key=True, max_length=30, verbose_name='Coordenadas')
  started_at  = models.TimeField(verbose_name="Comienzo")
  endeded_at  = models.TimeField(verbose_name="Final")
  type_choice = ( ('Fumigation', 'Fumigation'), ('Nutrition', 'Nutrition'), ('Prun', 'Prun'), ('Irrigation', 'Irrigation') )
  type        = models.CharField(choices=type_choice, max_length=9, blank=True, verbose_name="Tipo")
  crop        = models.ForeignKey(Crop, related_name="activities")
  
  def __str__(self):
    return "Actividad %s, %s" %(self.id, self.crop)

  def clean(self):
    # En caso de que exista un registro de un tipo incorrecto de medida, lo eliminamos
    if self.type == "Fumigation":
      if self.nutrition: self.nutrition.delete()
      if self.prun: self.prun.delete()
      if self.irrigation: self.irrigation.delete()

    elif self.type == "Nutrition":
      if self.fumigation: self.fumigation.delete()
      if self.prun: self.prun.delete()
      if self.irrigation: self.irrigation.delete()
    
    elif self.type == "Prun":
      if self.nutrition: self.nutrition.delete()
      if self.fumigation: self.fumigation.delete()
      if self.irrigation: self.irrigation.delete()
    
    elif self.type == "Irrigation":
      if self.nutrition: self.nutrition.delete()
      if self.prun: self.prun.delete()
      if self.fumigation: self.fumigation.delete()

  @property
  def owners(self):
    return self.crop.inside_of.owned_by.employees.all()

  class Meta:
    unique_together = ('date', 'coordinates', 'crop', 'type')

class FumigationType(models.Model):
  name = models.CharField(max_length=32, verbose_name="Tipo")

  def __str__(self):
    return self.name

class Fumigation(models.Model):
  amount   = models.FloatField(verbose_name='Cantidad', default=0) 
  type     = models.ForeignKey(FumigationType, null=True, related_name="applied_in")
  activity = models.OneToOneField(Activity, verbose_name="Actividad", related_name="fumigation")

class NutritionType(models.Model):
  name = models.CharField(max_length=32, verbose_name="Tipo")

  def __str__(self):
    return self.name

class Nutrition(models.Model):
  amount   = models.FloatField(verbose_name='Cantidad', default=0) 
  type     = models.ForeignKey(NutritionType, null=True, related_name="applied_in")
  activity = models.OneToOneField(Activity, verbose_name="Actividad", related_name="nutrition")

class PrunMethod(models.Model):
  name = models.CharField(max_length=32, verbose_name="Método")

  def __str__(self):
    return self.name

class Prun(models.Model):
  method   = models.ForeignKey(PrunMethod, null=True, related_name="applied_in")
  activity = models.OneToOneField(Activity, verbose_name="Actividad", related_name="prun")

class IrrigationMethod(models.Model):
  name = models.CharField(max_length=32, verbose_name="Método")

  def __str__(self):
    return self.name

class Irrigation(models.Model):
  method   = models.ForeignKey(IrrigationMethod, null=True, related_name="applied_in")
  activity = models.OneToOneField(Activity, verbose_name="Actividad", related_name="irrigation")


#--------------------------------------------------------------

#<------------ Measure ----------------------------------------

class Measure(models.Model):
  ''' Esta tabla almacena las medidas asociada a cada cultivo. 
      Pueden ser medidas del suelo, nutricionales o biologicas
  '''
  date        = models.DateField(default=datetime.date.today, verbose_name="Fecha")
  type_choice = ( ('Ground', 'Ground'), ('Nutritional', 'Nutritional'), ('Biological', 'Biological') )
  type        = models.CharField(choices=type_choice, max_length=9, blank=True, verbose_name="Tipo")
  crop        = models.ForeignKey(Crop, related_name="measures", verbose_name="Cultivo")

  def __str__(self):
    return "Medición %s, %s" %(self.id, self.crop)

  def clean(self):
    # En caso de que exista un registro de un tipo incorrecto de medida, lo eliminamos
    if self.type == "Ground":
      if self.nutritional: self.nutritional.delete()
      if self.biological: self.biological.delete()
    
    elif self.type == "Nutritional":
      if self.ground: self.ground.delete()
      if self.biological: self.biological.delete()
    
    elif self.type == "Biological":
      if self.nutritional: self.nutritional.delete()
      if self.ground: self.ground.delete()

  @property
  def owners(self):
    return self.crop.inside_of.owned_by.employees.all()

class Ground(models.Model):
  ''' Medidas del suelo del cultivo '''
  carbon    = models.FloatField(verbose_name='Carbón', default=0) 
  nitrogen  = models.FloatField(verbose_name='Nitrógeno', default=0)  
  iron      = models.FloatField(verbose_name='Hierro', default=0) 
  zinc      = models.FloatField(verbose_name='Zinc', default=0) 
  calcium   = models.FloatField(verbose_name='Calcio', default=0) 
  chlorine  = models.FloatField(verbose_name='Cloro', default=0)  
  magnesium = models.FloatField(verbose_name='Magnesio', default=0) 
  ph        = models.FloatField(verbose_name='pH', default=7)
  measure   = models.OneToOneField(Measure, verbose_name="Medicion", related_name="ground")
  

class Nutritional(models.Model):
  ''' Medida de los nutrietes del cultivo '''
  sulfur     = models.FloatField(verbose_name='Azufre', default=0)
  magnesium  = models.FloatField(verbose_name='Magnesio', default=0)
  cooper     = models.FloatField(verbose_name='Cobre', default=0)
  potasium   = models.FloatField(verbose_name='Potasio', default=0)
  maturation = models.FloatField(verbose_name='Maduración', default=0)
  brix       = models.FloatField(verbose_name='Porcentaje de jugo', default=0)
  pol        = models.FloatField(verbose_name='Porcentaje de sacarosa', default=0)
  measure    = models.OneToOneField(Measure, verbose_name="Medición", related_name="nutritional")
  

class Biological(models.Model):
  ''' Medidas biológicas del cultivo '''
  biomass = models.FloatField(verbose_name='Porcentaje de sacarosa', default=0) 
  vegetal_coverage = models.FloatField(verbose_name='Cubierta vegetal', default=0)
  wave_length = models.FloatField(verbose_name='Lengitud de onda', default=0)
  chlorophyll_a = models.FloatField(verbose_name='Clorofila a', default=0)
  chlorophyll_b = models.FloatField(verbose_name='Clorofila b', default=0)
  beta_carotene = models.FloatField(verbose_name='beta-Caroteno', default=0)
  alpha_carotene = models.FloatField(verbose_name='alpha-Caroteno', default=0)
  xanthophyll = models.FloatField(verbose_name='Xantofila', default=0)
  RVI = models.FloatField(verbose_name='Ratio Vegetation Index (RVI)', default=0)
  NDVI = models.FloatField(verbose_name='Normalized Difference Vegetation Index (NDVI)', default=0)
  PVI = models.FloatField(verbose_name='Perpendicular Vegetation Index (PVI)', default=0)
  TVI = models.FloatField(verbose_name='Transformed Vegetation Index (TVI)', default=0)
  TCAVI = models.FloatField(verbose_name='Transformed Soil Adjested Vegetation Index (TCAVI)', default=0)
  measure   = models.OneToOneField(Measure, verbose_name="Medición", related_name="biological")

#--------------------------------------------------------------->















