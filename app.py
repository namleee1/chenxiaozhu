
import yt_dlp
import os

def download_playlist_mp3():
    playlist_url = input("🔗 Nhập link playlist YouTube: ")

    # Tạo thư mục lưu trữ
    output_folder = "downloaded_audios"
    os.makedirs(output_folder, exist_ok=True)

    # Cấu hình yt-dlp để tải playlist dưới dạng MP3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{output_folder}/%(title)s.%(ext)s",  # Lưu theo tên video
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Chuyển sang MP3
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,  # Bỏ qua lỗi nếu có
        'yesplaylist': True,  # Xác nhận đây là playlist
        'playliststart': 1,   # Bắt đầu từ video thứ 1
        'playlistend': 50,    # Kết thúc ở video thứ 50
    }

    # Tải playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

    print(f"✅ Playlist đã được tải xong và lưu trong thư mục: {output_folder}")

# Chạy chương trình
download_playlist_mp3()

from pydub import AudioSegment
import glob
import os

# Thư mục chứa file MP3
folder = "downloaded_audios"
output_file = "merged_audio.mp3"

# Lấy danh sách file MP3
audio_files = sorted(glob.glob(os.path.join(folder, "*.mp3")))

if not audio_files:
    print("❌ Không tìm thấy file MP3 nào để gộp!")
else:
    # Gộp tất cả file lại
    merged_audio = AudioSegment.empty()
    for file in audio_files:
        audio = AudioSegment.from_file(file, format="mp3")
        merged_audio += audio  # Nối file

    # Xuất file đã gộp
    merged_audio.export(output_file, format="mp3", bitrate="192k")

    print(f"✅ File đã gộp xong: {output_file}")

