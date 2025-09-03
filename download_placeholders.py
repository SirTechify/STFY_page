import os
import requests
from pathlib import Path

# Create directories if they don't exist
base_dir = Path("static/images")
base_dir.mkdir(parents=True, exist_ok=True)

# Image URLs (free-to-use placeholder images)
images = {
    "profile/profile.jpg": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop&crop=faces",
    "projects/race-predictor.jpg": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop",
    "projects/robo-demo-1000.jpg": "https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=1200&h=630&fit=crop",
    "projects/project3.jpg": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=1200&h=630&fit=crop",
    "background/hero-bg.jpg": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&h=1080&fit=crop",
    "background/pattern.png": "https://www.transparenttextures.com/patterns/45-degree-fabric-light.png",
    "icons/python.png": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
    "icons/flask.png": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg",
    "icons/electronics.png": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/raspberrypi/raspberrypi-original.svg",
    "icons/ai-ml.png": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg"
}

# Download images
for path, url in images.items():
    file_path = base_dir / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading {path}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"  -> Saved to {file_path}")
    except Exception as e:
        print(f"  -> Error downloading {path}: {e}")

print("\nAll done! Placeholder images have been downloaded.")
print("You can now update your HTML/CSS to use these images.")
