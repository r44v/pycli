from openai import OpenAI
import uuid
from urllib.request import urlretrieve
from pathlib import Path

def create(prompt: str) -> str:
    client = OpenAI()

    response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
        )

    image_urls = [x.url for x in response.data]

    windows_user_donwload_folder = Path.home() / "Downloads"

    for i, url in enumerate(image_urls):
        filepath = windows_user_donwload_folder / f"dalle3_{uuid.uuid4()}.png"
        urlretrieve(url, filepath)
    
    # open the last image
    import os
    os.startfile(filepath)
