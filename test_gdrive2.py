import re
import requests

def get_drive_direct_url(video_url):
    session = requests.Session()
    drive_match = re.search(r'(?:id=|\/d\/|folders\/)([a-zA-Z0-9_-]{25,})', video_url)
    if drive_match:
        file_id = drive_match.group(1)
        base_url = "https://drive.google.com/uc?export=download"
        res = session.get(base_url, params={'id': file_id})

        confirm_token = ""
        for key, value in session.cookies.get_dict().items():
            if key.startswith("download_warning"):
                confirm_token = value

        if not confirm_token:
            match = re.search(r'name="confirm" value="([^"]+)"', res.text)
            confirm_token = match.group(1) if match else "t"

        uuid_match = re.search(r'name="uuid" value="([^"]+)"', res.text)
        uuid = uuid_match.group(1) if uuid_match else ""

        if uuid:
             download_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm={confirm_token}&uuid={uuid}"
        else:
             download_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm={confirm_token}"

        return download_url, session.cookies.get_dict()

    return video_url, {}

url, cookies = get_drive_direct_url("https://drive.google.com/uc?id=1ddFW6aV5dJxhV2wdfmEFf4K48d4G9MFA&export=download")
print("URL:", url)
print("Cookies:", cookies)

headers = {"Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()])}
print("Headers:", headers)

# Use requests to simulate ffmpeg stream
r = requests.get(url, headers=headers, stream=True)
print("Status code:", r.status_code)
# print headers to see if we get actual file or still HTML
print("Content-Type:", r.headers.get("Content-Type"))
print("Content-Disposition:", r.headers.get("Content-Disposition"))

# read start of file to verify
chunk = next(r.iter_content(chunk_size=1024))
print("Start bytes:", chunk[:20])
