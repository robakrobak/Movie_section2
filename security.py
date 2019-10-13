from user import User

users = [User(1, "admin", "admin"), User(2, "boob", "boob")]

username_mapping = {user.username: user for user in users}
userid_mapping = {user.id: user for user in users}


# def authenticate(username, password):
#     user = username_mapping.get(username, None)
#     if user and user.password == password:
#         return user

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


# def identity(payload):
#     user_id = payload["identity"]
#     return userid_mapping.get(user_id, None)

# funkcja JWT która pozwala nam dopasować odpowiedni token do odpowiedniego uzytkownika
def identity(payload):
    user_id = payload["identity"]
    return User.find_by_id(user_id)


x = authenticate("admin", "admin")
print(x)

# users = [
#     {"id": 1, "username": "admin", "password": "admin"},
#     {"id": 2, "username": "boob", "password": "boob"},
# ]
#
# username_mapping = {
#     "admin": {"id": 1, "username": "admin", "password": "admin"},
#     "boob": {"id": 2, "username": "boob", "password": "boob"},
# }
#
# userid_mapping = {
#     1: {"id": 1, "username": "admin", "password": "admin"},
#     2: {"id": 2, "username": "boob", "password": "boob"},
# }
#
#
# def authenticate(username, password):
#     user = username_mapping.get(username, None)
#     if user and user["password"] == password:
#         return user
#
#
# def identity(payload):
#     user_id = payload["identity"]
#     return userid_mapping.get(user_id, None)
