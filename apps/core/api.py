from django.db.models import Q
from rest_framework import serializers, viewsets, permissions, mixins
from apps.accounts.serializers import UserSerializer
from apps.core.models import (
    Organization, Facility, ProviderProfile, ProviderTitle, ProviderRole,
    ProviderSpecialty, Diagnosis, Medication, Procedure, )
from apps.patients.models import PatientProfile


class OrganizationSerializer(serializers.ModelSerializer):
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
        # if self.request.user.is_superuser:
        #     return qs.all()
        try:
            provider_profile = self.request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            provider_profile = None
        if provider_profile is not None:
            qs = qs.filter(
                Q(id__in=provider_profile.organizations.all()) |
                Q(id__in=provider_profile.organizations_managed.all())
            )
            return qs.all()
        try:
            patient_profile = self.request.user.patient_profile
        except PatientProfile.DoesNotExist:
            patient_profile = None
        if patient_profile is not None:
            qs = qs.filter(
                id=patient_profile.facility.organization.id)
            return qs.all()
        return qs.none()


# TODO: DELETE on a facility should mark it inactive rather than removing it
# from the database.
class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class FacilityViewSet(viewsets.ModelViewSet):
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        # QUESTION: should providers only have relations to facilities,
        # and not organizations?
        qs = Facility.objects.all()
        # if self.request.user.is_superuser:
        #     return qs.all()
        try:
            provider_profile = self.request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            provider_profile = None
        try:
            patient_profile = self.request.user.patient_profile
        except PatientProfile.DoesNotExist:
            patient_profile = None
        if provider_profile is not None:
            qs = qs.filter(
                Q(id__in=provider_profile.facilities.all()) |
                Q(id__in=provider_profile.facilities_managed.all())
            )
        elif patient_profile is not None:
            qs = qs.filter(id=patient_profile.facility.id)
        organization = self.request.query_params.get('organization_id')
        if organization:
            qs = qs.filter(organization__id=organization)
        return qs.all()


class ProviderProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = ProviderProfile
        fields = '__all__'


class ProviderProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProviderProfile.objects.all()
    # TODO: For providers, only return providers in the same facilities/organizations
    # TODO: For patients, only return providers that are providers for the patient


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
