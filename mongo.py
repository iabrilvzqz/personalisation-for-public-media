from datetime import datetime
import pymongo

def create_collection(db):
    collection_parameters = { "capped" : False}
    phone_collection = db.create_collection("name_collection", **collection_parameters )


def new_interaction(db, json_data):
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    #Checking records of a collection
    records = db.interactions

    #Create new document or record inside a collection
    new_record = {
        "user_id": json_data["user_id"],
        "title": json_data["title"],
        "type": json_data["type"],
        "value": json_data["value"],
        "time":  dt_string}

    records.insert_one(new_record)

    return True

def save_diversity_level(db, json_data):
    #Checking records of a collection
    records = db.slider_value
    records.update_one({"user_id": json_data["user_id"]}, {"$set": {"value": json_data["value"]}}, upsert=True)

    return True


def find_diversity_level(db, json_data):
    #Checking records of a collection
    records = db.slider_value

    #Find filtering
    result = records.find_one({ "user_id": json_data["user_id"]})
    
    return result["value"] if result else None


def find_interaction(db, json_data):
    # Get collection
    records = db.interactions

    #Find filtering
    result = records.find_one({ "user_id": json_data["user_id"], 
                                "title": json_data["title"], 
                                "type": json_data["type"] }, sort=[( '_id', pymongo.DESCENDING )])
    
    if result: result.pop('_id', None)
    return result if result else {'null': None}


def find_interactions_history(db, json_data):
    # Get collection
    records = db.interactions

    # Find filtering
    result = records.find({ "user_id": json_data["user_id"]}, sort=[('_id', pymongo.DESCENDING)]).limit(50)

    final_result = []
    for res in result:
        res.pop('_id', None)
        final_result.append(res)
    
    return final_result