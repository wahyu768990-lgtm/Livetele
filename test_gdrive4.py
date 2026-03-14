import re
import requests

def get_drive_direct_url(video_url):
    session = requests.Session()
    drive_match = re.search(r'(?:id=|\/d\/|folders\/)([a-zA-Z0-9_-]{25,})', video_url)
    if drive_match:
        file_id = drive_match.group(1)
        base_url = "https://drive.google.com/uc?export=download"
        res = session.get(base_url, params={'id': file_id})

        # We need to extract confirm token and download url correctly
        # In the response text, look for <form id="download-form" action="https://drive.usercontent.google.com/download" method="get">
        # Then all the hidden inputs.

        action_match = re.search(r'id="download-form" action="([^"]+)"', res.text)
        action_url = action_match.group(1) if action_match else "https://drive.usercontent.google.com/download"

        inputs = re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]+)">', res.text)
        params = {}
        for name, value in inputs:
            params[name] = value

        if not params:
            # Fallback
            confirm_token = ""
            for key, value in session.cookies.get_dict().items():
                if key.startswith("download_warning"):
                    confirm_token = value
            if not confirm_token:
                match = re.search(r'name="confirm" value="([^"]+)"', res.text)
                confirm_token = match.group(1) if match else "t"
            params['confirm'] = confirm_token
            params['id'] = file_id
            params['export'] = 'download'

        return action_url, params, session.cookies.get_dict(), session

    return video_url, {}, {}, session

url, params, cookies, session = get_drive_direct_url("https://drive.google.com/uc?id=1ddFW6aV5dJxhV2wdfmEFf4K48d4G9MFA&export=download")

print("URL:", url)
print("Params:", params)

r = session.get(url, params=params, stream=True)
print("Status code:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Content-Disposition:", r.headers.get("Content-Disposition"))

chunk = next(r.iter_content(chunk_size=1024))
print("Start bytes:", chunk[:20])
