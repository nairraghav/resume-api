from src.models import experience, user


def test_create_user():
    new_experience = experience.Experience(
        company_name="Company",
        start_date="01-01-2019",
        end_date="01-02-2019",
        description="This was my job",
    )
    new_user = user.User(
        password="password",
        test_pass="password",
        email_address="ron@ron.com",
        phone_number="123456789",
        city_state="Seattle, WA",
        last_name="Ronaldo",
        first_name="Ron",
        experiences=[new_experience],
    )
    assert new_user.password == "password" == new_user.test_pass
    assert new_user.email_address == "ron@ron.com"
    assert new_user.phone_number == "123456789"
    assert new_user.city_state == "Seattle, WA"
    assert new_user.last_name == "Ronaldo"
    assert new_user.first_name == "Ron"
