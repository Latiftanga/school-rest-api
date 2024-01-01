from faker import Faker
from faker.providers import DynamicProvider


gender_provider = DynamicProvider(
    provider_name="gender",
    elements=['M', 'F'],
)


staff_category_provider = DynamicProvider(
    provider_name="staff_category",
    elements=['Teaching', 'Non Teaching'],
)


region_provider = DynamicProvider(
    provider_name="region",
    elements=[
        'Upper West', 'Upper East', 'North East',
        'Northern', 'Savanna', 'Bono East', 'Ahafo',
        'Western', 'Western North', 'Greater Accra',
        'Central', 'Volta', 'Oti'
    ],
)

rank_provider = DynamicProvider(
    provider_name="rank",
    elements=[
        'Superintendent II', 'Superintendent I',
        'Snr. Superintendent II', 'Snr. Superintendent I',
        'Principal Superintendent', 'Assistant Director II',
        'Assistant Director I', 'Deputy Director',
        'Director II', 'Director I',
    ],
)
qualification_provider = DynamicProvider(
    provider_name="qualification",
    elements=[
        'Diploma', 'Degree', 'Post Graduate',
        'PhD'
    ],
)

qualification_category_provider = DynamicProvider(
    provider_name="qualification_category",
    elements=['Professional', 'Academic'],
)


institution_provider = DynamicProvider(
    provider_name="institution",
    elements=[
        'UEW', 'UG', 'University of Cape Coast',
        'UDS', 'UBIDS', 'KNUST', 'UHASs'
    ],
)

fake = Faker()

fake.add_provider(rank_provider)
fake.add_provider(gender_provider)
fake.add_provider(region_provider)
fake.add_provider(staff_category_provider)
fake.add_provider(qualification_category_provider)
fake.add_provider(institution_provider)
fake.add_provider(qualification_provider)


def get_school_default_values():
    """Return some random values for the school object"""
    return {
        'name': fake.name(),
        'subdomain': fake.first_name(),
        'address': fake.address(),
        'city': fake.city(),
        'region': fake.state(),
        'phone': fake.phone_number(),
        'email': fake.email()
    }


def get_staff_detail_default_values():
    """Return some random values for staff object"""
    return {
        'category': fake.staff_category(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'other_names': fake.first_name(),
        'gender': fake.gender(),
        'date_of_birth': fake.date(),
        'place_of_birth': fake.city(),
        'home_town': fake.city(),
        'home_region': fake.region(),
        'home_district': fake.city(),
        'nationality': fake.country(),
        'phone': fake.phone_number(),
        'residential_address': fake.address(),
        'permanent_address': fake.address()
    }


def get_promotion_default_values():
    """Return random values for promotion"""
    return {
        'rank': fake.rank(),
        'notional_date': fake.date(),
        'substantive_date': fake.date()
    }


def get_qualification_default_values():
    """Return random values for promotion"""
    return {
        'category': fake.qualification_category(),
        'title': fake.qualification(),
        'date_obtain': fake.date(),
        'institution': fake.institution()
    }
