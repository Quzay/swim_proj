import factory
from app.model import User,Goal,Competition,Achievement,Rating,Activity,Equipment, db, UserRole, Stroke_type


class SQLAlcemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        # sqlalchemy_session = db.session

class UserFactory(SQLAlcemyFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Faker("email")
    role = UserRole.USER
    age = factory.Faker("random_int" , min = 5, max = 100)
    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password("default_password")

class GoalFactory(SQLAlcemyFactory):
    class Meta:
        model = Goal
    
    target_distance = factory.Faker("random_int", min = 100, max = 10000)
    deadline = factory.Faker("date_between", start_date="today", end_date="+1y")

class ActivityFactory(SQLAlcemyFactory):
    class Meta:
        model = Activity

    
    day = factory.Faker("date_time")
    stroke = Stroke_type.FREESTYLE
    distance_meters = factory.Faker("random_int" , min = 100, max = 10000)
    
class CompetitionFactory(SQLAlcemyFactory):
    class Meta:
        model = Competition

    name = factory.Faker("name")
    location = factory.Faker("city")
    date = factory.Faker("date_between", start_date="-25y", end_date="+10y")



factories = [UserFactory,GoalFactory,ActivityFactory, CompetitionFactory]