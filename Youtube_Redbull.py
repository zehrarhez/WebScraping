import pandas as pd
import requests

def yt_channel_search(channel_name):
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    url = "https://www.googleapis.com/youtube/v3/search"

    parameters = {
        "part": "snippet",
        "q": channel_name,
        "key": api_key,
        "type": "channel",
        "maxResults": 10,
        "order": "videoCount"
    }

    channel_resp = requests.get(url, params=parameters)
    return channel_resp.json()

def get_videos(channelId):
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    url = "https://www.googleapis.com/youtube/v3/search"

    parameters = {
        "part": "snippet",
        "channelId": channelId,
        "key": api_key,
        "order": "date",
        "type": "video",
        "publishedAfter": "2021-01-01T00:00:00Z",
        "maxResults": "50"
    }

    video_resp = requests.get(url, params=parameters)
    return video_resp.json()


channel_request = yt_channel_search("Red Bull")

channelId = None
if "items" in channel_request:
    for result in channel_request["items"]:
        for k, v in result["snippet"].items():
            if (k == "title") and (v == "Red Bull"):
                channelId = result["snippet"]["channelId"]
                break

if channelId is not None:
    recent_videos = get_videos(channelId)
else:
    print("Kanal kimliği bulunamadı.")

def data_extractor(raw_data, first_loop, second_loop, col_name):
    ext_data = [result[second_loop][col_name] for result in raw_data[first_loop]]
    return ext_data
if recent_videos is not None:
    video_id = data_extractor(recent_videos, "items", "id", "videoId")
    publish_date = data_extractor(recent_videos, "items", "snippet", "publishedAt")
    title = data_extractor(recent_videos, "items", "snippet", "title")
    desc = data_extractor(recent_videos, "items", "snippet", "description")


for i in range(len(title)):
    print(f"{i+1}.", f"Video Title: {title[i]} - Video ID: {video_id[i]}")

# Verileri bir DataFrame'e dönüştürme
data = {
    "Video Title": title,
    "Video ID": video_id,
    "Publish Date": publish_date,
    "Description": desc
}

df = pd.DataFrame(data)

# CSV dosyasına aktarma
df.to_csv("redbull_videos.csv", index=False)
