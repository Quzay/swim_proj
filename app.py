from model.database import app,init_db
import controller.user_contoller

init_db()

if __name__ == "__main__":
    app.run(debug=True)