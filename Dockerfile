# Gunakan image Python yang ringan
FROM python:3.10-slim

# Install FFmpeg dan dependencies sistem
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install library Telethon
RUN pip install --no-cache-dir telethon

# Copy file script ke dalam container
COPY streamer.py .

# Setup Default Environment Variables (Bisa di-override saat running)
ENV VIDEO_URL="https://tipigd.tipikug.workers.dev/0:/Me/Pencarian.Terakhir.2025.1080p.NF.WEB-DL.DDP5.1.H.264-KQRM.mkv"
ENV API_ID=961780
ENV API_HASH="bbbfa43f067e1e8e2fb41f334d32a6a7"
ENV TARGET_CHAT="@whwhwwiw"
ENV STRING_SESSION="1BVtsOHABu4d7oTmHXsUhb7ovCiAjbbhuuCIWAioaJFunUqq-SRBjREVwC5JgHOJvclvnvGbqfW3SNj2TOKY2WdzQKurUcHEJictLnN9aIWvlSXLJmXSdQichst3Pm-lKCN8UuDlp2L8Xf2tp0vXHoaU_nMuWdeFZNrY5EUkH35lTE_IsVgFvngG7GqNGdNHzvbxFJswRYl8HwpMvi8AS9umrMgMU0gtyqpb-qjqxm_oGozLiam4HIAmWKcOGAlnd9UGpMvABNE4fEATsoYXMbkpcHt0fFX67sCf7xOpXGaAne7zigOtWfMRUTnTsjeLNi_D3vZ8BQO54lskdHfdBQSyFLZoVjOQ="

# Perintah untuk menjalankan aplikasi
CMD ["python", "streamer.py"]
