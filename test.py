import datetime
from app.model import Achievement,Activity,Equipment,Goal,Rating,User,Competition,db
from app import create_app


app = create_app()



def run_seed():
    
    with app.app_context():
        dranisama = User(
            username="Dranislav",
            password_hash="nohomeqt",
            email="dranisma@gmail.com",
            age=17
        )
        db.session.add(dranisama)
        db.session.flush() 
        
        first_goal = Goal(
            target_distance=8000,
            deadline=datetime.date(2026, 3, 20),
            user_id=dranisama.id
        )
        activities = [
            Activity(stroke="FREESTYLE", distance_meters=1200, user_id=dranisama.id),
            Activity(stroke="BUTTERFLY", distance_meters=3100, user_id=dranisama.id)
        ]
        db.session.add(first_goal)
        db.session.add_all(activities)
        
        db.session.commit()
        
        db.session.refresh(first_goal)
        print(f"Goal: {first_goal.target_distance}m - Days left: {first_goal.days_left} - remaining:{first_goal.remaining_distance}")

if __name__ == "__main__":
    run_seed()
    
