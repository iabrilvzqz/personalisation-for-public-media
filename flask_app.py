from flask import Flask, request, jsonify
from pymongo import MongoClient
#from flask_cors import CORS
import os

from mongo import new_interaction, find_interaction

app = Flask(__name__)
#cors = CORS(app)

client = MongoClient("mongodb+srv://test:test@rs.qug52es.mongodb.net/?retryWrites=true&w=majority", connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db = client.get_database('RS')

serindipity_test = {
    "image": "https://m.media-amazon.com/images/M/MV5BMDAxOGNhYjctNWQ2My00MTZjLWFkNWUtNDI3N2FhNWNkZWYyXkEyXkFqcGdeQXVyNjAzNzExNTk@._V1_QL75_UY281_CR5,0,190,281_.jpg",
    "title": "This is a title",
    "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
    "tags": ["Comedy", "Family"],
    "category": "TV Show"
}

diversity_test = [
    {
      "image": "https://m.media-amazon.com/images/M/MV5BOWEwZGNmYzctZmMzOS00YzZmLWE5MzktMjFlMGQ4OTBiZDUyXkEyXkFqcGdeQXVyMjY2NjQ2MDY@._V1_QL75_UY281_CR5,0,190,281_.jpg",
      "title": "Title 1",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://m.media-amazon.com/images/M/MV5BOGMyYjM3M2UtOGZiMC00NTU3LWE0Y2EtZjUzNDk5NmMyNDIzXkEyXkFqcGdeQXVyMTE2NzA0Ng@@._V1_QL75_UX190_CR0,4,190,281_.jpg",
      "title": "Title 2",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://picsum.photos/200/300",
      "title": "Title 3",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://picsum.photos/200/300",
      "title": "Title 4",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://picsum.photos/200/300",
      "title": "Title 5",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://picsum.photos/200/300",
      "title": "Title 6",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://picsum.photos/200/300",
      "title": "Title 7",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://picsum.photos/200/300",
      "title": "Title 8",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    }
]

@app.route('/')
def serve_index():
  return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
  print(filename)
  if filename != "null" and os.path.isfile(os.path.join(app.static_folder, filename)):
    return app.send_static_file(filename)
  else:
    return app.send_static_file('index.html')

@app.route("/diversity", methods=["GET", "POST"])
def diversity_recommendations():
  json_data = request.json
  return jsonify(diversity_test)

@app.route("/serindipity", methods=["GET", "POST"])
def serindipity_recommendations():
  json_data = request.json
  return jsonify(serindipity_test)

@app.route("/create_interaction", methods=["GET", "POST"])
def create_interaction():
  json_data = request.json
  new_interaction(db, json_data)

  return jsonify({"created": True})

@app.route("/get_interaction", methods=["GET", "POST"])
def get_interaction():
  json_data = request.json
  result = find_interaction(db, json_data)
  return jsonify(dict(result))

if __name__=="__main__":
    app.run(debug=True)