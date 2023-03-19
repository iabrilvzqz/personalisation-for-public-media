# Personalisation of (Public) Media
This is the back end part for the Personalisation of Public Media Final Project.

## Getting Started
1. Install flask with `pip install flask`.
1. Once the installation is complete, run the following command to confirm the installation: `python -c "import flask; print(flask.__version__)"`
1. To run the application, you can use `python flask_app.py`. The default server will start on port 5000 `http://127.0.0.1:5000/`. Changes made to the code may not always be automatically reflected in the application.

## Using a compiled Angular project in Flask

Follow these steps:

Build your Angular project using the Angular CLI command `ng build --prod`. This will create a dist folder in your project directory with the compiled code.

In the Flask application, there's a directory called `static`. Move the contents of the dist folder from the Angular project to the static folder in the Flask application.