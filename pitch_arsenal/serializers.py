from rest_framework import serializers
from .models import Pitch, PitchAttribute, PitchAttributeChoice

class PitchAttributeChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchAttributeChoice
        fields = ('score', 'description')


class PitchAttributeSerializer(serializers.ModelSerializer):
    choices = PitchAttributeChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = PitchAttribute
        fields = ('attribute', 'choices')


class PitchSerializer(serializers.ModelSerializer):
    attributes = PitchAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Pitch
        fields = ('name', 'attributes')


class ChoiceFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchAttributeChoice
        fields = ("id", "score")


class AttributeFormSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    class Meta:
        model = PitchAttribute
        fields = ("id", "attribute", "choices")
    
    def get_choices(self, obj):
        choices = PitchAttributeChoice.objects.filter(attribute=obj)
        return ChoiceFormSerializer(choices, many=True).data


class PitchFormSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Pitch
        fields = ("id", "name", "attributes")
    
    def get_attributes(self, obj):
        attributes = PitchAttribute.objects.filter(pitch=obj)
        return AttributeFormSerializer(attributes, many=True).data
