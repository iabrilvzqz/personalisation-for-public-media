from flask import Flask, request, jsonify
#from flask_cors import CORS
import os

from mongo import new_interaction, find_interaction, find_interactions_history, save_diversity_level, find_diversity_level
from recommendation_system import get_recommendations

app = Flask(__name__)
#cors = CORS(app)

serindipity_test = {
    "image": "https://m.media-amazon.com/images/M/MV5BMDAxOGNhYjctNWQ2My00MTZjLWFkNWUtNDI3N2FhNWNkZWYyXkEyXkFqcGdeQXVyNjAzNzExNTk@._V1_QL75_UY281_CR5,0,190,281_.jpg",
    "title": "This is a title",
    "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
    "tags": ["Comedy", "Family"],
    "category": "TV Show"
}

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
  results = get_recommendations(json_data['user_id'])
  return jsonify(results)

@app.route("/serindipity", methods=["GET", "POST"])
def serindipity_recommendations():
  json_data = request.json
  return jsonify(serindipity_test)

@app.route("/create_interaction", methods=["GET", "POST"])
def create_interaction():
  json_data = request.json
  new_interaction(json_data)
  return jsonify({"created": True})

@app.route("/get_interaction", methods=["GET", "POST"])
def get_interaction():
  json_data = request.json
  result = find_interaction(json_data)
  return jsonify(dict(result))

@app.route("/update_diversity_level", methods=["GET", "POST"])
def update_diversity_level():
  json_data = request.json
  result = save_diversity_level(json_data)
  return jsonify({"created": True})

@app.route("/get_diversity_level", methods=["GET", "POST"])
def get_diversity_level():
  json_data = request.json
  result = find_diversity_level(json_data)
  return jsonify({"value": result})

@app.route("/get_interactions_history", methods=["GET", "POST"])
def get_interactions_history():
  json_data = request.json
  result = find_interactions_history(json_data)
  return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)