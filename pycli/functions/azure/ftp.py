import shutil
import pathlib
import subprocess
from urllib.parse import urlparse
from xml.etree import cElementTree as ElementTree

DEFAULT_FILEZILLA_PATH = "C:\\Program Files\\FileZilla FTP Client\\filezilla.exe"

def open_publish_profile_in_filezilla(path_to_publish_profile: str):
    filezilla_path = shutil.which("filezilla") or DEFAULT_FILEZILLA_PATH

    if not pathlib.Path(filezilla_path).exists():
        print("FileZilla not found. Please install FileZilla and try again.")
        return
    
    absolute_path = pathlib.Path(path_to_publish_profile).absolute()
    if not absolute_path.exists():
        print(f"Publish profile not found at {absolute_path.as_posix()}.")
        return
    
    def find_ftp_profile(profile_path: str):
        tree = ElementTree.parse(profile_path)
        root = tree.getroot()

        for child in root:
            if child.attrib['publishMethod'] == 'FTP' and 'ReadOnly - FTP' not in child.attrib['profileName']:
                return child
    
    ftp_profile = find_ftp_profile(absolute_path.as_posix())
    if ftp_profile is None:
        print("No FTP profile found.")
        return
    
    server = ftp_profile.attrib['publishUrl']
    username = ftp_profile.attrib['userName']
    password = ftp_profile.attrib['userPWD']

    server_url = urlparse(server)
    host = f"{server_url.scheme}://{username}:{password}@{server_url.netloc}{server_url.path}"

    print("Opening FileZilla...")
    subprocess.Popen([filezilla_path, host])