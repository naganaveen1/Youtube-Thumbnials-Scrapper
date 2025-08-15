# Youtube-Thumbnials-Scrapper

# Youtube-Thumbnails-Scraper

A Python script designed to automatically scrape and download unique thumbnails from past livestreams of a specific YouTube channel. The script uses the YouTube Data API to fetch video details and employs a perceptual hashing algorithm to identify and remove duplicate thumbnails, ensuring you maintain a clean and organized collection.

## 🌟 Key Features

* **Automated Scraping:** Efficiently fetches video data from a specified YouTube channel.
* **Duplicate Prevention:** Utilizes perceptual hashing (phash) to compare and eliminate duplicate or near-identical thumbnails.
* **Customizable:** Easily configure the channel handle, output directory, minimum livestream duration, and duplicate tolerance.
* **High-Resolution Downloads:** Downloads thumbnails in their highest available resolution (`maxresdefault.jpg`).

## 🛠️ Prerequisites

To run this script, you will need to have Python 3.6 or higher installed. The following libraries are also required:

* `google-api-python-client`
* `requests`
* `Pillow`
* `imagehash`

You can install all necessary dependencies using pip:

```bash
pip install google-api-python-client requests Pillow imagehash
```

## 🚀 Getting Started

### Step 1: Obtain a YouTube Data API Key

1. Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. In the project dashboard, go to **APIs & Services** and select **Library**.
4. Search for and enable the **YouTube Data API v3**.
5. Go to **Credentials** and create a new **API Key**.
6. Copy the generated API key.

### Step 2: Configure the Script

Open the `yt_live_thumbnail_scrapper.py` file and update the variables in the `CONFIG` section with your specific information:

```python
# ========== CONFIG ==========
API_KEY = "YOUR_YOUTUBE_API_KEY"  # Paste your API key here
CHANNEL_HANDLE = "@Munnabhaigaming"  # Replace with the handle of the channel you want to scrape
SAVE_DIR = "past_live_thumbnails_all"
MIN_DURATION_SECONDS = 3600  # Minimum duration of a livestream to be considered (e.g., 3600 for 1 hour)
HASH_SIZE = 16  # Size of the hash, a larger value is more precise
TOLERANCE = 5  # The maximum difference between two hashes to be considered a duplicate
# ============================
```

### Step 3: Run the Script

Execute the script from your terminal:

```bash
python yt_live_thumbnail_scrapper.py
```

The script will begin by finding the uploads playlist for the specified channel, iterating through the videos, and downloading thumbnails for long-form livestreams. It will also print progress and a final summary of how many unique thumbnails were downloaded.

## 🤝 Contribution

Contributions are welcome! If you have any suggestions for improvements or bug fixes, please open an issue or submit a pull request on this repository.
