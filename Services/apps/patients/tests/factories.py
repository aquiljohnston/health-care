import factory


class PatientProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.PatientProfile`
    """

    class Meta:
        model = 'patients.PatientProfile'
        django_get_or_create = ('user', )


class ProblemAreaFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.ProblemArea`
    """

    class Meta:
        model = 'patients.ProblemArea'


class PatientMedicationFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.PatientMedication`
    """

    class Meta:
        model = 'patients.PatientMedication'


class PotentialPatientFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.PotentialPatient`
    """

    class Meta:
        model = 'patients.PotentialPatient'


class EmergencyContactFactory(factory.django.DjangoModelFactory):
    """
    Factory for :model:`patients.EmergencyContact`
    """

    class Meta:
        model = 'patients.EmergencyContact'
