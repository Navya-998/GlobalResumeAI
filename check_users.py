from app import app
from extensions import bcrypt
from models.user import User

with app.app_context():

    users = User.query.all()

    print("Total Users:", len(users))

    for user in users:

        print("---------------------------")
        print("ID:", user.id)
        print("Email:", user.email)

        print(
            "Password = test123 :",
            bcrypt.check_password_hash(
                user.password_hash,
                "test123"
            )
        )

        print(
            "Password = password :",
            bcrypt.check_password_hash(
                user.password_hash,
                "password"
            )
        )