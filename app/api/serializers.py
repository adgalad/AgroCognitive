from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _


import app.models as models

class User(serializers.ModelSerializer): # forms.ModelForm

    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'id_number', 'role', 'company']
        read_only_fields = ['pk']

    # converts to JSON
    # validations for data passed

    # def get_url(self, obj):
    #     # request
    #     request = self.context.get("request")
    #     return obj.get_api_url(request=request)

class Payment(serializers.ModelSerializer): # forms.ModelForm
    class Meta:
        model = models.Payment
        fields = ['code', 'user', 'crop', 'date', 'amount', 'service',]
        read_only_fields = ['pk', 'user']

class Crop(serializers.ModelSerializer): # forms.ModelForm
    class Meta:
        model = models.Crop
        fields = ['id', 'tipo', 'variety', 'name', 'density', 'distance', 
                  'coordinates', 'number_plants', 'sown_area', 'inside_of']
        read_only_fields = ['pk']

class Terrain(serializers.ModelSerializer): # forms.ModelForm
    class Meta:
        model = models.Terrain
        fields = ['id', 'city','country','coordinates','name','is_active','owned_by',]
        read_only_fields = ['pk']

class Company(serializers.ModelSerializer): # forms.ModelForm
    class Meta:
        model = models.Company
        fields = ['name', 'rif']
        read_only_fields = []

class Affection(serializers.ModelSerializer):
    class Meta:
        model = models.Affection
        fields = ['code', 'description', 'type']
        read_only_fields = []

class LocatedIn(serializers.ModelSerializer):
    class Meta:
        model = models.LocatedIn
        fields =  ["affection","coordinates"]
        read_only_fields = ['diagnostic']

class Diagnostic(serializers.ModelSerializer):
    affections = LocatedIn(source='locatedIn', read_only=False, many=True)

    def create(self, validated_data):
        affections = validated_data.pop('affections')
        diagnostic =  super(Diagnostic, self).create(validated_data)
        for affection in affections:
            LocatedIn.objects.create(affection=affection['affection'],
                                     diagnostic=diagnostic,
                                     coordinates=affection['coordinates'])
        return diagnostic
    class Meta:
        model = models.Diagnostic
        fields = ['code', 'date', 'crop', 'affections']
        read_only_fields = []


class FumigationType(serializers.ModelSerializer):
    class Meta:
        model = models.FumigationType
        fields = "__all__"
class NutritionType(serializers.ModelSerializer):
    class Meta:
        model = models.NutritionType
        fields = "__all__"
class PrunMethod(serializers.ModelSerializer):
    class Meta:
        model = models.PrunMethod
        fields = "__all__"
class IrrigationMethod(serializers.ModelSerializer):
    class Meta:
        model = models.IrrigationMethod
        fields = "__all__"

class Fumigation(serializers.ModelSerializer):
    class Meta:
        model = models.Fumigation
        exclude = ["activity"]
        read_only_fields = []

class Nutrition(serializers.ModelSerializer):
    class Meta:
        model = models.Nutrition
        exclude = ["activity"]
        read_only_fields = []

class Prun(serializers.ModelSerializer):
    class Meta:
        model = models.Prun
        exclude = ["activity"]
        read_only_fields = []

class Irrigation(serializers.ModelSerializer):
    class Meta:
        model = models.Irrigation
        exclude = ["activity"]
        read_only_fields = []

class Activity(serializers.ModelSerializer):
    fumigation = Fumigation(required=False)
    nutrition = Nutrition(required=False)
    prun = Prun(required=False)
    irrigation = Irrigation(required=False)

    def create(self, validated_data):
        fumigation = validated_data.pop("fumigation") if 'fumigation' in validated_data else None
        nutrition = validated_data.pop("nutrition") if 'nutrition' in validated_data else None
        prun = validated_data.pop("prun") if 'prun' in validated_data else None
        irrigation = validated_data.pop("irrigation") if 'irrigation' in validated_data else None
        activity = models.Activity(**validated_data)
        
        if activity.type == "Fumigation":
            if not fumigation or not fumigation['type']:
                raise serializers.ValidationError(_("Missing fumigation activity."))
            fumigation['activity'] = activity
            models.Fumigation.objects.create(**fumigation)
        elif activity.type == "Nutrition":
            if not nutrition or not nutrition['type']:
                raise serializers.ValidationError(_("Missing nutrition activity."))
            nutrition['activity'] = activity
            models.Nutrition.objects.create(**nutrition)
        elif activity.type == "Prun":
            if not prun or not prun['method']:
                raise serializers.ValidationError(_("Missing prun activity."))
            prun['activity'] = activity
            models.Prun.objects.create(**prun)
        elif activity.type == "Irrigation":
            if not irrigation or not irrigation['method']:
                raise serializers.ValidationError(_("Missing irrigation activity."))
            irrigation['activity'] = activity
            models.Irrigation.objects.create(**irrigation)
        activity.save()
        return activity
        
    class Meta:
        model = models.Activity
        fields = "__all__"
        read_only_fields = []




class Ground(serializers.ModelSerializer):
    class Meta:
        model = models.Ground
        exclude = ["measure"]
        read_only_fields = []

class Nutritional(serializers.ModelSerializer):
    class Meta:
        model = models.Nutritional
        exclude = ["measure"]
        read_only_fields = []

class Biological(serializers.ModelSerializer):
    class Meta:
        model = models.Biological
        exclude = ["measure"]
        read_only_fields = []

class Measure(serializers.ModelSerializer):
    ground = Ground(required=False)
    nutritional = Nutritional(required=False)
    biological = Biological(required=False)

    def create(self, validated_data):
        ground = validated_data.pop("ground") if 'ground' in validated_data else None
        nutritional = validated_data.pop("nutritional") if 'nutritional' in validated_data else None
        biological = validated_data.pop("biological") if 'biological' in validated_data else None
        measure = models.Measure(**validated_data)
        
        if measure.type == "Ground":
            if not ground:
                raise serializers.ValidationError(_("Missing ground measures."))
            ground['measure'] = measure
            models.Ground.objects.create(**ground)
        elif measure.type == "Nutritional":
            if not nutritional:
                raise serializers.ValidationError(_("Missing nutritional measures."))
            nutritional['measure'] = measure
            models.Nutritional.objects.create(**nutritional)
        elif measure.type == "Biological":
            if not biological:
                raise serializers.ValidationError(_("Missing biological measures."))
            biological['measure'] = measure
            models.Biological.objects.create(**biological)
        measure.save()
        return measure


    class Meta:
        model = models.Measure
        fields = "__all__"
        read_only_fields = []





