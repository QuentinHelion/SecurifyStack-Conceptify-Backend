from flask import Blueprint, jsonify, send_file, request
from utils.sftp_utils import connect_sftp, is_directory
from utils.terraform_utils import execute_terraform
import os
import tempfile

app_routes = Blueprint('app_routes', __name__)

SFTP_BASE_PATH = os.getenv("SFTP_BASE_PATH", ".")
LOCAL_APP_DIR = os.getenv("LOCAL_APP_DIR", "./downloaded_apps")

@app_routes.route('/apps', methods=['GET'])
def list_apps():
    sftp = connect_sftp()
    sftp.chdir(SFTP_BASE_PATH)
    app_folders = []

    for item in sftp.listdir():
        if item.startswith('.') or item == '.git':
            continue
        if not is_directory(sftp, item):
            continue
        try:
            sftp.chdir(item)
            files = sftp.listdir()
            if 'description.txt' in files:
                with sftp.open('description.txt') as f:
                    description = f.read().decode()
                app_folders.append({
                    'name': item,
                    'description': description.strip(),
                    'logo_url': f'/apps/{item}/logo'
                })
            sftp.chdir('..')
        except IOError:
            continue
    sftp.close()
    return jsonify(app_folders)

@app_routes.route('/apps/<app_name>/logo', methods=['GET'])
def get_logo(app_name):
    sftp = connect_sftp()
    try:
        sftp.chdir(f"{SFTP_BASE_PATH}/{app_name}")
        local_path = os.path.join(tempfile.gettempdir(), f"{app_name}_logo.png")
        sftp.get('logo.png', local_path)
        return send_file(local_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    finally:
        sftp.close()

@app_routes.route('/install/<app_name>', methods=['POST','GET'])
def install_app(app_name):
    sftp = connect_sftp()
    local_path = os.path.join(LOCAL_APP_DIR, app_name)
    os.makedirs(local_path, exist_ok=True)

    try:
        sftp.chdir(f"{SFTP_BASE_PATH}/{app_name}")
        for file in sftp.listdir():
            sftp.get(file, os.path.join(local_path, file))

        success, output_or_error = execute_terraform(local_path)
        if not success:
            return jsonify({'error': 'Terraform error', 'details': output_or_error}), 500

        return jsonify({'status': 'success', 'output': output_or_error})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        sftp.close()
