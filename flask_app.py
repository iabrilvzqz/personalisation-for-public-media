from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from mongo import new_interaction, find_interaction, find_interactions_history, save_diversity_level, find_diversity_level
from recommendation_system import main_recommendations_by_npo, get_recommendations_by_interactions, get_personalised_recommendations, get_serindipity_recommendation, get_top_ten_recommendation

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def serve_index():
  return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
  if filename != "null" and os.path.isfile(os.path.join(app.static_folder, filename)):
    return app.send_static_file(filename)
  else:
    return app.send_static_file('index.html')

@app.route("/personalised_recommendations", methods=["GET", "POST"])
def personalised_recommendations():
  json_data = request.json
  results = get_personalised_recommendations(json_data['user_id'])
  return jsonify(results)

@app.route("/similar_recommendations", methods=["GET", "POST"])
def similar_recommendations():
  json_data = request.json
  results = get_recommendations_by_interactions(json_data['user_id'])
  return jsonify(results)

@app.route("/top_ten_recommendations", methods=["GET"])
def get_top_ten():
  results = get_top_ten_recommendation()
  return jsonify(results)

@app.route("/serindipity_recommendations", methods=["GET", "POST"])
def serindipity_recommendations():
  json_data = request.json
  results = get_serindipity_recommendation(json_data['user_id'])
  return jsonify(results)

@app.route("/npo_recommendation", methods=["GET", "POST"])
def npo_recommendation():
  results = main_recommendations_by_npo()
  return jsonify(results)

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