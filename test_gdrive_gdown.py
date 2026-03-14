import subprocess
import os

url = "https://drive.google.com/uc?id=1ddFW6aV5dJxhV2wdfmEFf4K48d4G9MFA&export=download"

# Try getting direct link via gdown
try:
    import gdown
    print(gdown.download(id="1ddFW6aV5dJxhV2wdfmEFf4K48d4G9MFA", output="film_gdown.mkv", quiet=False, fuzzy=True))
except Exception as e:
    print("gdown failed:", e)
