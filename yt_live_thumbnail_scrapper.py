from googleapiclient.discovery import build
import requests
import os
from PIL import Image
import imagehash
from datetime import datetime

# ========== CONFIG ==========
API_KEY = "Youtube_API_KEY"  # Replace with your YouTube Data API key
CHANNEL_HANDLE = "@Munnabhaigaming"  # Replace with channel handle
SAVE_DIR = "past_live_thumbnails_all"
MIN_DURATION_SECONDS = 3600  # 1 hour
HASH_SIZE = 16
TOLERANCE = 5
# ============================

os.makedirs(SAVE_DIR, exist_ok=True)
youtube = build("youtube", "v3", developerKey=API_KEY)

# Step 1: Get channel ID and uploads playlist
channel_resp = youtube.channels().list(
    part="id,contentDetails",
    forHandle=CHANNEL_HANDLE
).execute()

if not channel_resp["items"]:
    raise ValueError(" Could not find channel. Check the handle.")

uploads_playlist_id = channel_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
print(f"Uploads playlist ID: {uploads_playlist_id}")

# Step 2: Perceptual hash check for duplicates
hashes_seen = {}

def is_duplicate(img_path):
    try:
        img = Image.open(img_path)
        h = imagehash.phash(img, hash_size=HASH_SIZE)
        for existing_hash in hashes_seen:
            if h - existing_hash <= TOLERANCE:
                return True
        hashes_seen[h] = img_path
        return False
    except:
        return False

# Step 3: Get all video IDs from uploads playlist
video_ids = []
next_page_token = None

while True:
    playlist_resp = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    for item in playlist_resp.get("items", []):
        video_ids.append(item["contentDetails"]["videoId"])

    next_page_token = playlist_resp.get("nextPageToken")
    if not next_page_token:
        break

print(f"Total videos found: {len(video_ids)}")

# Step 4: Filter past livestreams & download thumbnails
count = 0
for i in range(0, len(video_ids), 50):
    batch_ids = video_ids[i:i+50]
    videos_resp = youtube.videos().list(
        part="liveStreamingDetails",
        id=",".join(batch_ids)
    ).execute()

    for item in videos_resp.get("items", []):
        live = item.get("liveStreamingDetails", {})
        if all(k in live for k in ["actualStartTime", "actualEndTime", "scheduledStartTime"]):
            start = datetime.fromisoformat(live["actualStartTime"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(live["actualEndTime"].replace("Z", "+00:00"))
            duration = (end - start).total_seconds()

            if duration >= MIN_DURATION_SECONDS:  # Only long livestreams
                vid = item["id"]
                thumb_url = f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"

                try:
                    img_data = requests.get(thumb_url).content
                    file_path = os.path.join(SAVE_DIR, f"{vid}.jpg")
                    with open(file_path, "wb") as f:
                        f.write(img_data)

                    # Check for duplicate and remove if necessary
                    if is_duplicate(file_path):
                        os.remove(file_path)
                        print(f" Removed duplicate for video: {vid}")
                    else:
                        print(f" Downloaded past livestream thumbnail: {vid}")
                        count += 1

                except Exception as e:
                    print(f"Error downloading {vid}: {e}")

print(f" Done! Downloaded {count} unique past livestream thumbnails.")
