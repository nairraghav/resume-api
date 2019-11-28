from src.models import experience


def test_create_experience():
    new_experience = experience.Experience(company_name="Company", start_date="01-01-2019", end_date="01-02-2019", description="This was my job")
    assert new_experience.company_name == "Company"
    assert new_experience.start_date == "01-01-2019"
    assert new_experience.end_date == "01-02-2019"
    assert new_experience.description == "This was my job"
