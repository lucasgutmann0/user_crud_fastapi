# defininig in a function the structure (schema) of a user
def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "lastname": item["lastname"],
        "age": item["age"],
        "email": item["email"],
        "phone_number": item["phone_number"],
        "password": item["password"]
    }
    
def usersEntity(entity) -> list:
     return [ 
                userEntity(item) for item in entity
            ]