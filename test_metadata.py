import subprocess
import json
import os

VIDEO_INPUT = "dummy.mp4"

# Generate a 1-second dummy video to test metadata extraction
os.system(f"ffmpeg -f lavfi -i testsrc=duration=1:size=1280x720:rate=30 -c:v libx264 -metadata title='My Awesome Video' {VIDEO_INPUT} -y")

def get_video_metadata():
    print("Mengambil metadata video...")
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", VIDEO_INPUT
    ]

    title = "Tidak diketahui"
    quality = "Tidak diketahui"
    meta_info = "Tidak diketahui"
    duration_info = "Tidak diketahui"

    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(res.stdout)

        format_info = data.get('format', {})
        tags = format_info.get('tags', {})

        # Try to get title from metadata, fallback to filename if missing
        title = tags.get('title')
        if not title:
            # use VIDEO_INPUT filename if title is not present
            title = os.path.basename(VIDEO_INPUT)

        video_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
        if video_streams:
            best_stream = sorted(video_streams, key=lambda x: x.get('width', 0), reverse=True)[0]

            width = best_stream.get('width', '?')
            height = best_stream.get('height', 0)
            codec = best_stream.get('codec_name', '?').upper()
            meta_info = f"{width}x{height} ({codec})"

            if isinstance(height, int):
                if height >= 2160:
                    quality = "4K UHD"
                elif height >= 1080:
                    quality = "1080p FHD"
                elif height >= 720:
                    quality = "720p HD"
                elif height >= 480:
                    quality = "480p SD"
                elif height >= 360:
                    quality = "360p SD"
                else:
                    quality = f"{height}p"

        duration = float(format_info.get('duration', 0))
        if duration > 0:
            m, s = divmod(int(duration), 60)
            h, m = divmod(m, 60)
            duration_info = f"{h:02d}:{m:02d}:{s:02d}"

    except Exception as e:
        print(f"Gagal mengambil metadata: {e}")

    return title, quality, meta_info, duration_info

t, q, mi, d = get_video_metadata()
print(f"Title: {t}\nQuality: {q}\nDetail: {mi}\nDuration: {d}")
