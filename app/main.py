from flask import Flask
from routes.app_routes import app_routes
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_routes)

if __name__ == '__main__':
    os.makedirs(os.getenv("LOCAL_APP_DIR", "./downloaded_apps"), exist_ok=True)
    app.run(debug=True, port=5000)