from flask import Flask, jsonify
import os


app = Flask(__name__)
app.config['TERRAFORMS_PATH'] = os.getenv('TERRAFORMS_PATH', './SecurifyStack-Terraforms')

os.makedirs(app.config['TERRAFORMS_PATH'], exist_ok=True)


@app.route('/list')
def list_modules():
    """
    List all available Terraform modules
    :return:
    """
    result = [
        directory for directory in os.listdir(app.config['TERRAFORMS_PATH'])
        if os.path.isdir(os.path.join(app.config['TERRAFORMS_PATH'], directory)) and directory != ".git"
    ]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
