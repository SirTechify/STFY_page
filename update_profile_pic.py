import os
import requests
from pathlib import Path

# Create profile directory if it doesn't exist
profile_dir = Path("static/images/profile")
profile_dir.mkdir(parents=True, exist_ok=True)

# Download the profile picture
url = "https://avatars.githubusercontent.com/u/25069177?v=4"
response = requests.get(url)
response.raise_for_status()

# Save the image
with open(profile_dir / "profile.jpg", 'wb') as f:
    f.write(response.content)

print("Profile picture updated successfully!")
