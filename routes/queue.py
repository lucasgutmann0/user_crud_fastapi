from fastapi import APIRouter, Response, status
from config.db import connection
from schemas.queue import queueEntity, queuesEntity, queueEntityName, queuesEntityName
from models.queue import Queue
from bson import ObjectId

# defining routes of user
queue = APIRouter()

# user db
queue_db = connection.data_structures.queue

# get all queues
@queue.get("/queues", status_code=status.HTTP_200_OK, tags=["Queue"])
async def get_all_queue():
    return queuesEntity(queue_db.find())

# delete queue
@queue.delete("/queues/{id}", status_code=status.HTTP_200_OK)
async def delete_queue(id: str, response: Response):
    try:
        queue_db.find_one_and_delete({"_id": ObjectId(id)})
        return {"message": "Queue has been deleted succesfully"}
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "The Queue doesn't exists or has alredy been deleted"}

# get all queue names
@queue.get("/queues/names", status_code=status.HTTP_200_OK, tags=["Queue"])
async def get_all_queue_names(response: Response):
    # empty list for queues
    queue_names = []
    # get all queues from db
    queues_from_db = queue_db.find()
    # index queues to list
    for i in queues_from_db:
        queue_names.append(i["name"])
    # if theres no queues return message
    if not len(queue_names) > 0:
        response.status_code = status.HTTP_302_FOUND
        queues = {
            "message": "Theres no queues to show"
        }
    # else, return all queue names in a list with a message
    else:
        response.status_code = status.HTTP_200_OK
        queues = {
            "names": queue_names,
            "message": "These are the availables queues"
        }
    return queues

# find a queue
@queue.get("/queues/{name}", tags=["Queue"])
async def get_one_queue_by_name(name: str):
    try:
        # gettin queue based on the name
        queue = queue_db.find_one({"name": name})
        # returning user
        return queueEntity(queue)
    except:
        return {"message": "Couldn't find requested queue"}


# add element to end of queue
@queue.put("/queues/{name}/", tags=["Queue"])
async def add_element_to_end_of_queue(name: str, value: float):
    # gettin queue based on the name
    queue = queue_db.find_one({"name": name})
    if not queue == None:
        parsed_queue = queueEntity(queue)
        try:  
            parsed_queue["data"].append(value)
            parsed_queue_modified = parsed_queue
            del parsed_queue_modified["id"]
            queue_db.find_one_and_update({"name": name}, {"$set": parsed_queue_modified})
        except:
            return {"message": "Couldn't add element from the requested to the queue"}
        return parsed_queue
    return {"message": "Couldn't find requested queue"}


# add element to a queue
@queue.put("/queues/specific/{name}/", tags=["Queue"])
async def add_element_to_queue(name: str, position: int, value: float):
    # gettin queue based on the name
    queue = queue_db.find_one({"name": name})
    if not queue == None:
        parsed_queue = queueEntity(queue)
        if position < 0:
            parsed_queue["data"].insert(position, value)    
        elif position < (len(parsed_queue["data"]) - 1):
            parsed_queue["data"].insert(position, value)
        else:
            parsed_queue["data"].append(value) 
        
        parsed_queue_modified = parsed_queue
        del parsed_queue_modified["id"]
        queue_db.find_one_and_update({"name": name}, {"$set": parsed_queue_modified})
        return parsed_queue
    return {"message": "Couldn't find requested queue"}

# remove element from a queue
@queue.delete("/queues/{name}/", tags=["Queue"])
async def delete_element_to_queue(name: str, position: int):
    # gettin queue based on the name
    queue = queue_db.find_one({"name": name})
    if not queue == None:
        parsed_queue = queueEntity(queue)
        try:  
            parsed_queue["data"].pop(position)
            parsed_queue_modified = parsed_queue
            del parsed_queue_modified["id"]
            queue_db.find_one_and_update({"name": name}, {"$set": parsed_queue_modified})
        except:
            return {"message": "Couldn't delete element from the requested queue"}
        return parsed_queue
    return {"message": "Couldn't find requested queue"}

# regist a queue
@queue.post("/queues", status_code=status.HTTP_201_CREATED, tags=["Queue"])
async def create_queue(queue: Queue, response: Response):
    try:
        # create new dict with requested data
        new_queue = dict(queue)
        # insert new queue
        id = queue_db.insert_one(new_queue).inserted_id
        # get registered queue
        registered_queue = queueEntity(queue_db.find_one({"_id": id}))
        # insert message to queue
        registered_queue["message"] = "Queue was succesfully created"
        # return queue with message
        return registered_queue
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Couldn't create the User"}



