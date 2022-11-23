# defininig in a function the structure (schema) of a user
def queueEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": str(item["name"]),
        "info": list(item["info"])
    }
    
def queuesEntity(entity) -> list:
     return [ 
                queueEntity(item) for item in entity
            ]


def queueEntityName(item) -> dict:
    return {
        "name": str(item["name"]),
    }

def queuesEntityName(entity) -> list:
     return [ 
                queueEntityName(item) for item in entity
            ]