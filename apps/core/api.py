from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, permissions, mixins

from care_adopt_backend import utils
from apps.accounts.models import EmailUser
from apps.accounts.serializers import SettingsUserForSerializers
from apps.core.models import (
    Organization, Facility, ProviderProfile, ProviderTitle, ProviderRole,
    ProviderSpecialty, Diagnosis, Medication, Procedure, )
from apps.patients.models import PatientProfile


class OrganizationSerializer(serializers.ModelSerializer):
    is_manager = serializers.SerializerMethodField()

    def get_is_manager(self, obj):
        request = self.context['request']
        if not request.user.provider_profile:
            return False
        return obj.id in request.user.provider_profile.organizations_managed.all()

    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = Organization.objects.all()
        provider_profile = utils.provider_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        # If user is a provider, get all organizations that they belong to
        if provider_profile is not None:
            qs = qs.filter(
                Q(id__in=provider_profile.organizations.all()) |
                Q(id__in=provider_profile.organizations_managed.all()),
            )
            return qs.all()
        # If user is a patient, only return the organization their facility belongs to
        if patient_profile is not None:
            qs = qs.filter(
                id=patient_profile.facility.organization.id)
            return qs.all()
        return qs.none()


# TODO: DELETE on a facility should mark it inactive rather than removing it
# from the database.
class FacilitySerializer(serializers.ModelSerializer):
    is_manager = serializers.SerializerMethodField()

    def get_is_manager(self, obj):
        request = self.context['request']
        provider_profile = utils.provider_profile_or_none(request.user)
        if not provider_profile:
            return False
        return obj in request.user.provider_profile.facilities_managed.all()

    class Meta:
        model = Facility
        fields = '__all__'


class FacilityViewSet(viewsets.ModelViewSet):
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = Facility.objects.all()
        provider_profile = utils.provider_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        # If user is a provider, filter out facilities they do not belong to
        if provider_profile is not None:
            qs = qs.filter(
                Q(id__in=provider_profile.facilities.all()) |
                Q(id__in=provider_profile.facilities_managed.all())
            )
            # Filter for getting only facilities within a specific organization
            organization = self.request.query_params.get('organization_id')
            if organization:
                qs = qs.filter(organization__id=organization)
            return qs.all()
        # If user is a patient, only return their facility
        if patient_profile is not None:
            qs = qs.filter(id=patient_profile.facility.id)
            return qs.all()


class ProviderUserInfo(SettingsUserForSerializers, serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('email', 'date_joined', 'last_login', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key', 'is_developer', )


class ProviderProfileSerializer(serializers.ModelSerializer):
    user = ProviderUserInfo()

    class Meta:
        model = ProviderProfile
        fields = '__all__'


class ProviderProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = ProviderProfile.objects.all()
        provider_profile = utils.provider_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if provider_profile is not None:
            # TODO: For providers, only return providers in the same facilities/organizations
            return qs.all()
        if patient_profile is not None:
            # TODO: For patients, only return providers that are providers for the patient
            return qs.all()


class ProviderTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderTitle
        fields = '__all__'


class ProviderTitleViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderTitleSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProviderTitle.objects.all()


class ProviderRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRole
        fields = '__all__'


class ProviderRoleViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderRoleSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProviderRole.objects.all()


class ProviderSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderSpecialty
        fields = '__all__'


class ProviderSpecialtyViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSpecialtySerializer
    permission_classes = (permissions.AllowAny, )
    queryset = ProviderSpecialty.objects.all()


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class DiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Diagnosis.objects.all()


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'


class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Medication.objects.all()


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'


class ProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = ProcedureSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Procedure.objects.all()
