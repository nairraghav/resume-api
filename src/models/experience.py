from sqlalchemy import Column, Integer, String, Date, ForeignKey
from src.config import db, marsh


class Experience(db.Model):
    __tablename__ = "experiences"
    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    position_title = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


class ExperienceSchema(marsh.Schema):
    class Meta:
        fields = (
            "id",
            "company_name",
            "position_title",
            "start_date",
            "end_date",
            "description",
            "user_id",
        )


experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)
