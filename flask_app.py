from flask import Flask, request, jsonify
import os

app = Flask(__name__)

serindipity_test = {
    "image": "assets/images/small/img-1.jpg",
    "title": "This is a title",
    "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
    "tags": ["Comedy", "Family"],
    "category": "TV Show"
}

diversity_test = [
    {
      "image": "https://picsum.photos/200/300",
      "title": "Title 1",
      "description": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Hic, eius laboriosam at est modi veniam quidem voluptatum nemo quas suscipit consequatur delectus ducimus atque, odio, consectetur error corporis consequuntur. Necessitatibus.",
      "tags": ["Comedy", "Family"],
      "category": "TV Show"
    },
    {
      "image": "https://picsum.photos/200/300",
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
  email = json_data["email"]
  return jsonify(diversity_test)

@app.route("/serindipity", methods=["GET", "POST"])
def serindipity_recommendations():
  json_data = request.json
  email = json_data["email"]
  return jsonify(serindipity_test)

if __name__=="__main__":
    app.run(debug=True)