import factory
from app.model import User,Goal,Competition,Achievement,Rating,Activity,Equipment, db, UserRole


class SQLAlcemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session

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
    
    target_distance = factory.Faker("random_int", min = 5, max = 120)
    deadline = factory.Faker("date")


factories = [UserFactory,GoalFactory]