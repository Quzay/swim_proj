import datetime
from model import Achievement,Activity,Equipment,Goal,Rating,User,Competition,Base
from model.database import init_db,engine
from sqlalchemy.orm import Session

init_db()



with Session(engine) as session:
    Dranisama = User(username="Dranislav",password="nohome",email="dranisma@gmail.com",age = 17)
    session.add(Dranisama)
    session.flush()
    
    First_Goal = Goal(
        target_distance = 8000,
        deadline = datetime.date(2026,3,20),
        user_id = Dranisama.id
        )
    First_Activity = Activity(stroke = "Freestyle",distance_meters = 1200,user_id = Dranisama.id)
    Second_Activity = Activity(stroke = "Freestyle",distance_meters = 3100,user_id = Dranisama.id)

    session.add_all([First_Goal,First_Activity,Second_Activity])
    session.commit()
    
    session.refresh(First_Goal)
    print(f"Goal: {First_Goal.target_distance}m")
    print(f"Distance to go: {First_Goal.remaining_distance}m")
    print(f"Days left to finish: {First_Goal.days_left} days")
