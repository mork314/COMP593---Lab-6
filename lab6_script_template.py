import hashlib
import requests
import os
import subprocess

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()
    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    hash_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.9.2/win64/vlc-3.0.9.2-win64.exe.sha256'
    #Send GET request for hash
    resp = requests.get(hash_url)
    if resp.ok:
        file_hash = resp.text
        file_hash = file_hash.split(' ')[0]
        return file_hash

def download_installer():
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.9.2/win64/vlc-3.0.9.2-win64.exe'
    response = requests.get(file_url)
    
    if response.status_code == requests.codes.ok:

        file_content = response.content

    return file_content

def installer_ok(installer_data, expected_sha256):
    installer_hash = hashlib.sha256(installer_data).hexdigest()
    
    if installer_hash == expected_sha256:
        return True
    else:
        return False

def save_installer(installer_data):
    installer_path = r'C:\temp'
    with open(installer_path, 'wb') as file:
            file.write(installer_data)
    return installer_path

def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'])    
    return
    
def delete_installer(installer_path):
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()