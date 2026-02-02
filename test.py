from model import Achievement,Activity,Equipment,Goal,Rating,User,Competition,Base
from model.database import init_db,engine
from sqlalchemy.orm import Session

init_db()

#Activ = Activity(stroke="freestyle",distance = 14.5)

with Session(engine) as session:
    Dranisama = User(username="Dranislav",password="nohome",email="dranisma@gmail.com")
    session.add(Dranisama)
    session.commit()

