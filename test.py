from model import Achievement,Activity,Equipment,Goal,Rating,User,Competition,Base
from model.database import init_db,engine
from sqlalchemy.orm import Session

init_db()



with Session(engine) as session:
    Dranisama = User(username="Dranislav",password="nohome",email="dranisma@gmail.com",age = 17)
    session.add(Dranisama)
    session.commit()

