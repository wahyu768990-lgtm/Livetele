import asyncio
import os
import subprocess
import time
from telethon import TelegramClient, functions
from telethon.sessions import StringSession

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", 961780))
API_HASH = os.environ.get("API_HASH", 'bbbfa43f067e1e8e2fb41f334d32a6a7')
STRING_SESSION = os.environ.get("STRING_SESSION")
TARGET_CHAT = os.environ.get("TARGET_CHAT", '@whwhwwiw')
VIDEO_URL = os.environ.get("VIDEO_URL")
STREAM_DURATION = 3 * 3600  # 3 Jam dalam detik

async def main():
    if not STRING_SESSION:
        print("Error: STRING_SESSION tidak ditemukan!")
        return

    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Sesi tidak valid!")
        return

    print(f"Berhasil login! Target: {TARGET_CHAT}")

    try:
        entity = await client.get_entity(TARGET_CHAT)
        
        # 1. Pastikan Group Call aktif
        try:
            await client(functions.phone.CreateGroupCallRequest(peer=entity, title="NOBAR 3 JAM", rtmp_stream=True))
        except Exception:
            pass

        # 2. Ambil RTMP URL
        call_info = await client(functions.phone.GetGroupCallStreamRtmpUrlRequest(peer=entity, revoke=False))
        full_rtmp = f"{call_info.url}{call_info.key}"

        # 3. Filter FFmpeg (Ditambah -stream_loop -1 untuk loop video)
        v_filter = (
            "scale=1920:1080:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:-1:-1:color=black,"
            "drawtext=text='LIVE 3 JAM':fontcolor=white:fontsize=24:x=30:y=30"
        )

        ffmpeg_cmd = [
            "ffmpeg", "-re", 
            "-stream_loop", "-1",  # Mengulang video terus menerus
            "-i", VIDEO_URL,
            "-vf", v_filter,
            "-c:v", "libx264", "-preset", "veryfast", "-b:v", "3000k", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-ac", "2",
            "-f", "flv", full_rtmp
        ]

        print(f"Streaming dimulai. Akan berhenti otomatis dalam 3 jam...")
        process = subprocess.Popen(ffmpeg_cmd)

        # Timer logic
        start_time = time.time()
        while time.time() - start_time < STREAM_DURATION:
            # Cek jika proses FFmpeg mati mendadak (misal: koneksi putus)
            if process.poll() is not None:
                print("FFmpeg terhenti mendadak, memulai ulang...")
                process = subprocess.Popen(ffmpeg_cmd)
            
            await asyncio.sleep(10) # Cek setiap 10 detik

        print("Waktu 3 jam tercapai. Mematikan stream...")
        process.terminate()

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
