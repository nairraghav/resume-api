from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.experience import ExperienceSchema
from src.config import db, marsh


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    city_state = Column(String)
    phone_number = Column(String)
    email_address = Column(String, unique=True)
    test_pass = Column(String)
    password = Column(String)
    experiences = relationship("Experience", backref="User", lazy="dynamic")


class UserSchema(marsh.ModelSchema):
    experience = marsh.Nested(ExperienceSchema, many=True)

    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)
