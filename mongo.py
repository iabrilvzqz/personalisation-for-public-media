import pymongo 

def create_collection(db):
    collection_parameters = { "capped" : False}
    phone_collection = db.create_collection("name_collection", **collection_parameters )


def new_interaction(db, json_data):
    #Checking records of a collection
    records = db.interactions

    #Create new document or record inside a collection
    new_record = {
        "user_id": json_data["user_id"],
        "title": json_data["title"],
        "type": json_data["type"],
        "value": json_data["value"] }

    records.insert_one(new_record)

    return True


def find_interaction(db, json_data):
    # Get collection
    records = db.interactions

    #Find filtering
    result = records.find_one({ "user_id": json_data["user_id"], 
                                "title": json_data["title"], 
                                "type": json_data["type"] }, sort=[( '_id', pymongo.DESCENDING )])
    
    if result: result.pop('_id', None)
    return result if result else {'null': None}

