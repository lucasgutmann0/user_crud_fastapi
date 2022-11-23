from itertools import count
from fastapi import APIRouter, Response, status
from config.db import connection
from schemas.user import userEntity, usersEntity
from models.user import User, UserLogin
from passlib.hash import sha256_crypt
from bson import ObjectId

# defining routes of user
user = APIRouter()

# user db
user_db = connection.users.user

# get all users
@user.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users():
    return usersEntity(connection.users.user.find())


# create user
@user.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, response: Response):
    try:
        # create new dict with requested data
        new_user = dict(user)
        # encrypt password
        new_user["password"] = sha256_crypt.encrypt(new_user["password"])
        # inser into mongo db - get id of the element
        id = user_db.insert_one(new_user).inserted_id
        # get the user recently created
        user = user_db.find_one({"_id": id})
        # assign message to variable
        created_user = userEntity(user)
        # Add message to the json that is about to be returned
        created_user["message"] = "User was created succesfully created"
        # return the user data and the message
        return created_user
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Couldn't create the User"}

# login to app
@user.post("/login/")
async def get_user(request: UserLogin, response: Response):
    # create new dict with data of the request
    login_data = dict(request)
    # save requested user on variable
    req_email = user_db.find_one({"email": login_data["email"]})
    # TRY to find a user with that email
    if req_email != None:
        # validate if password is valid
        if sha256_crypt.verify(login_data["password"], userEntity(req_email)["password"]):
            response.status_code = status.HTTP_200_OK
            return userEntity(req_email)
        # else return 403 forbidden
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Wrong Password"}
    # else not found and message
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Couldn't find a User with that Email"}


# find a user
@user.get("/users/{id}")
async def get_user(id: str):
    try:
        # gettin user based on the id
        user = user_db.find_one({"_id": ObjectId(id)})
        # returning user
        return userEntity(user)
    except:
        return {"message": "Couldn't find requested user"}


# update user data
@user.put("/users/{id}")
async def update_user(id: str, user: User ,response: Response):
    try:
        user_db.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
        return {"message": "User has been updated succesfully"}
    except:
        return {"message": "Couldn't update the requested user"}


# delete user
@user.delete("/users/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: str, response: Response):
    try:
        user_db.find_one_and_delete({"_id": ObjectId(id)})
        return {"message": "User has been deleted succesfully"}
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "The user doesn't exists or has alredy been deleted"}
