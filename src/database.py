from src.config import db
from src.models.user import User
from src.models.experience import Experience
from faker import Faker
from random import randint
from bcrypt import hashpw, gensalt

fake = Faker()


def init_db():
    db.create_all()


def drop_db():
    db.drop_all()


def seed_db():
    for i in range(randint(5, 10)):
        experiences = []
        for j in range(randint(1, 3)):
            start_date = fake.date_between(start_date="-30y", end_date="-10y")
            end_date = fake.date_between(start_date="-30y", end_date="-10y")
            experience_summary_sentences = randint(1, 5)
            experience = Experience(
                company_name=fake.company(),
                position_title=fake.job(),
                start_date=start_date,
                end_date=end_date,
                description=fake.paragraph(
                    nb_sentences=experience_summary_sentences,
                    variable_nb_sentences=True,
                    ext_word_list=None,
                ),
            )
            db.session.add(experience)
            experiences.append(experience)

        password = fake.word().encode()
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            city_state=f"{fake.city()},{fake.state()}",
            phone_number=fake.phone_number(),
            email_address=fake.ascii_safe_email(),
            test_pass=password,
            password=hashpw(password, gensalt()),
            experiences=list(experiences)
        )
        db.session.add(user)

    db.session.commit()
