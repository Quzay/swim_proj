import factory
from app.model import User,Goal,Competition,Rating,Activity,Equipment, db, UserRole, Stroke_type, Status, Equipment_type, ModelName, Challenge


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
    status = Status.ACTIVE

class ActivityFactory(SQLAlcemyFactory):
    class Meta:
        model = Activity
    referense_id = factory.Faker("random_int")
    model_name = ModelName.CHALLENGE
    time_s = factory.Faker("pyfloat" , min_value =20 , max_value = 600 , right_digits = 2)
    stroke = Stroke_type.FREESTYLE
    distance_meters = factory.Faker("random_int" , min = 100, max = 10000)
    user_id = factory.Faker("random_int")
    
class CompetitionFactory(SQLAlcemyFactory):
    class Meta:
        model = Competition
    amount = factory.Faker("random_int", min = 2 , max = 15)
    name = factory.Faker("name")
    location = factory.Faker("city")
    date = factory.Faker("date_between", start_date="+1y", end_date="+10y")
    status = Status.ACTIVE
    is_open = True

class RatingFactory(SQLAlcemyFactory):
    class Meta:
        model = Rating
    value = factory.Faker("pyfloat",min_value= 3, max_value = 10, right_digits =2 )


class EquipmentFactory(SQLAlcemyFactory):
    class Meta:
        model = Equipment
    name = factory.Faker("name")
    type = Equipment_type.FLIPPERS
    brand = factory.Faker("name")
    is_broken = False

class ChallengeFactory(SQLAlcemyFactory):
    class Meta:
        model = Challenge
    name = factory.Faker("name")
    description = factory.Faker("name")
    distance = factory.Faker("random_int" , min = 100, max = 1000)
    stroke = Stroke_type.FREESTYLE

factories = [UserFactory,GoalFactory,ActivityFactory, CompetitionFactory, RatingFactory, EquipmentFactory, ChallengeFactory]