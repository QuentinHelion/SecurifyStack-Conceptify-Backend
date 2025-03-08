from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests
import paramiko

app = Flask(__name__)
app.secret_key = os.getenv('PROXMOX_SECRET_KEY', 'my-secret-key')  # Change this in production
# UPLOAD_FOLDER = 'images'
# PROXMOX_HOST = '192.168.1.250'  # Adresse IP de Proxmox
# PROXMOX_USER = 'root'
# PROXMOX_PASSWORD = '!Quentin123'
# PROXMOX_TARGET_PATH = '/var/lib/vz/template/iso/'

app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploaded_images')
app.config['ALLOWED_EXTENSIONS'] = os.getenv('ALLOWED_EXTENSIONS', 'iso,img,tar.gz').split(',')
app.config['PROXMOX_HOST'] = os.getenv('PROXMOX_HOST', 'your-proxmox-server')
app.config['PROXMOX_USERNAME'] = os.getenv('PROXMOX_USERNAME', 'root@pam')
app.config['PROXMOX_PASSWORD'] = os.getenv('PROXMOX_PASSWORD', 'your-password')
app.config['PROXMOX_NODE'] = os.getenv('PROXMOX_NODE', 'pve')  # Nom du noeud Proxmox
app.config['PROXMOX_STORAGE'] = os.getenv('PROXMOX_STORAGE', 'local')  # Stockage cible
app.config['DISTRIBUTIONS_FILE'] = os.getenv('DISTRIBUTIONS_FILE', 'distributions.json')
app.config['PROXMOX_TARGET_PATH'] = os.getenv('PROXMOX_TARGET_PATH', '/var/lib/vz/template/iso/')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)




@app.route('/')
def index():
    images = list_downloaded_images()
    return render_template('index.html', images=images, cloud_images=CLOUD_IMAGES)





if __name__ == '__main__':
    app.run(debug=True)