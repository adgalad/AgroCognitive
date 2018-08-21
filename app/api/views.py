# generic

from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import *
from app.ibm_cloud import COSZipUploadHandler
from app.forms import cargarImagenesVueloForm
from .permissions import IsOwnerOrReadOnly, IsOwner
import app.api.serializers as serializers
import app.api.responses as responses


class UserAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.User
  # queryset                = User.objects.all()

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return User.objects.none()
    if self.request.user.is_superuser:
      return User.objects.all()
    else:
      return User.objects.filter(pk=self.request.user.id)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class UserRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.User
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return User.objects.none()
    if self.request.user.is_superuser:
      return User.objects.all()
    else:
      return User.objects.filter(pk=self.request.user.id)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

  # def get_object(self):
  #     pk = self.kwargs.get("pk")
  #     return User.objects.get(pk=pk)




''' Payment API '''
class PaymentAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Payment
  #queryset                = Payment.objects.all()

  def get_queryset(self):
    return Payment.objects.all()

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class PaymentRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Payment
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return Payment.objects.none()
    if self.request.user.is_superuser:
      return Payment.objects.all()
    else:
      return Payment.objects.filter(user=self.request.user)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}



''' Crop API '''
class CropAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Crop
  #queryset                = Crop.objects.all()

  def get_queryset(self):
    return Crop.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class CropRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Crop
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if True or self.request.user.is_superuser:
      return Crop.objects.all()
    else:
      return Crop.objects.filter(inside_of__owned_by__employees__pk=self.request.user.id)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}


''' Terrain API '''
class TerrainAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Terrain
  #queryset                = Terrain.objects.all()

  def get_queryset(self):
    return Terrain.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class TerrainRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Terrain
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return Terrain.objects.none()
    if self.request.user.is_superuser:
      return Terrain.objects.all()
    else:
      return Terrain.objects.filter(user=self.request.user)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

''' Company API '''
class CompanyAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Company
  #queryset                = Company.objects.all()

  def get_queryset(self):
    return Company.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class CompanyRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Company
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return Company.objects.none()
    if self.request.user.is_superuser:
      return Company.objects.all()
    else:
      return Company.objects.filter(employees__pk=self.request.user.id)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

''' Diagnostic API '''
class DiagnosticAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Diagnostic

  def get_queryset(self):
    return Diagnostic.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class DiagnosticRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Diagnostic
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return Diagnostic.objects.none()
    if self.request.user.is_superuser:
      return Diagnostic.objects.all()
    else:
      return Diagnostic.objects.filter(crop__inside_of__owned_by__employees__pk=self.request.user.id)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}


''' Diagnostic API '''
class AffectionAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Affection

  def get_queryset(self):
    return Affection.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class AffectionRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Affection
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return Affection.objects.none()
    else:
      return Affection.objects.all()
      
  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}


''' FumigationType API '''
class FumigationTypeAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.FumigationType

  def get_queryset(self):
    return FumigationType.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class FumigationTypeRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk'
  serializer_class        = serializers.FumigationType
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return FumigationType.objects.none()
    if self.request.user.is_superuser:
      return FumigationType.objects.all()

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}


''' NutritionType API '''
class NutritionTypeAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.NutritionType

  def get_queryset(self):
    return NutritionType.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class NutritionTypeRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk'
  serializer_class        = serializers.NutritionType
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return NutritionType.objects.none()
    if self.request.user.is_superuser:
      return NutritionType.objects.all()

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}


''' PrunMethod API '''
class PrunMethodAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.PrunMethod

  def get_queryset(self):
    return PrunMethod.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class PrunMethodRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk'
  serializer_class        = serializers.PrunMethod
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return PrunMethod.objects.none()
    if self.request.user.is_superuser:
      return PrunMethod.objects.all()

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}


''' IrrigationMethod API '''
class IrrigationMethodAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field     = 'pk'
  serializer_class = serializers.IrrigationMethod

  def get_queryset(self):
    return IrrigationMethod.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class IrrigationMethodRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field       = 'pk'
  serializer_class   = serializers.IrrigationMethod
  permission_classes = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return IrrigationMethod.objects.none()
    if self.request.user.is_superuser:
      return IrrigationMethod.objects.all()

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}





''' Activity API '''
class ActivityAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Activity

  def get_queryset(self):
    return Activity.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class ActivityRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Activity
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return Activity.objects.none()
    if self.request.user.is_superuser:
      return Activity.objects.all()
    else:
      return Activity.objects.filter(crop__inside_of__owned_by__employees__pk=self.request.user.id)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}


''' Measure API '''
class MeasureAPI(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Measure

  def get_queryset(self):
    return Measure.objects.all()

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}

class MeasureRud(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
  lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
  serializer_class        = serializers.Measure
  permission_classes      = [IsOwnerOrReadOnly]

  def get_queryset(self):
    if not self.request.user.is_authenticated():
      return Measure.objects.none()
    if self.request.user.is_superuser:
      return Measure.objects.all()
    else:
      return Measure.objects.filter(crop__inside_of__owned_by__employees__pk=self.request.user.id)

  def get_serializer_context(self, *args, **kwargs):
    return {"request": self.request}




class uploadImages(APIView):

  def post(self, request, *args, **kwargs):
    handler = COSZipUploadHandler(request=request)
    request.upload_handlers = [handler]
    form = cargarImagenesVueloForm(request.POST, request.FILES)

    if not handler.file_name:
      return responses.ImagesUpload.error("No se encontró ningun archivo.")
    elif handler.error:
      return responses.ImagesUpload.error(handler.error)
    else:
      return responses.ImagesUpload.success()
    

  
