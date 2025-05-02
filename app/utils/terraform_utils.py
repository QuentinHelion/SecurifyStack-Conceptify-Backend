import subprocess

def execute_terraform(path):
    try:
        init = subprocess.run(['terraform', 'init'], cwd=path, capture_output=True, text=True)
        if init.returncode != 0:
            return False, init.stderr

        apply = subprocess.run(['terraform', 'apply', '-auto-approve'], cwd=path, capture_output=True, text=True)
        if apply.returncode != 0:
            return False, apply.stderr

        return True, apply.stdout
    except Exception as e:
        return False, str(e)
