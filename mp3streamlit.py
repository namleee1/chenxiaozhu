#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import os
from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
import imageio_ffmpeg

# === CONFIG ===
API_KEY = 'AIzaSyC5a25Hg2aJuEsQdbZ5eF4N4h0gIm9KoCk'  # Thay bằng API key của bạn

# === GET LATEST VIDEO URLs ===
def get_latest_video_urls(api_key, channel_id, num_videos=3):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        order='date',
        maxResults=num_videos
    )
    response = request.execute()

    video_urls = []
    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':
            video_id = item['id']['videoId']
            video_urls.append(f'https://www.youtube.com/watch?v={video_id}')
    return video_urls

# === DOWNLOAD AUDIO ===
def download_audio(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(filename)[0] + '.mp3'
        return mp3_filename



# === STREAMLIT UI ===
st.title("🎶 Tải nhạc mới từ YouTube Channel")

# User input for channel ID and number of videos
channel_id = st.text_input("Nhập Channel ID YouTube:", "")
num_videos = st.slider("Chọn số bài hát muốn tải:", min_value=1, max_value=10)

# User input for the download path
download_path = st.text_input("Nhập đường dẫn thư mục để lưu bài hát:", "")

if st.button("Tải về các bài hát mới"):
    if channel_id and download_path:
        st.info("Đang lấy danh sách bài hát...")
        urls = get_latest_video_urls(API_KEY, channel_id, num_videos)

        all_downloaded = True
        for url in urls:
            st.write(f"🎧 Đang tải: {url}")
            try:
                # Kiểm tra xem đường dẫn có hợp lệ không
                if not os.path.exists(download_path):
                    os.makedirs(download_path)

                mp3_file = download_audio(url, download_path)
                if os.path.exists(mp3_file):
                    with open(mp3_file, "rb") as f:
                        st.download_button(
                            label="📥 Tải về " + os.path.basename(mp3_file),
                            data=f,
                            file_name=os.path.basename(mp3_file),
                            mime="audio/mpeg"
                        )
            except Exception as e:
                st.error(f"Lỗi khi tải {url}: {e}")
                all_downloaded = False  # Nếu có lỗi xảy ra, thay đổi biến thành False

        # Thông báo khi tải xong tất cả
        if all_downloaded:
            st.success("✅ Đã tải xong tất cả!")
        else:
            st.warning("Một số bài hát không thể tải.")
    else:
        st.error("Vui lòng nhập Channel ID và đường dẫn thư mục!")

