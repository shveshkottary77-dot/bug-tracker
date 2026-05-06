# ─────────────────────────────────────────────
# Stage 1: Base Image
# ─────────────────────────────────────────────
# Use official lightweight Python image
FROM python:3.11-slim

# ─────────────────────────────────────────────
# Stage 2: Set Working Directory
# ─────────────────────────────────────────────
# All commands will run from /app inside the container
WORKDIR /app

# ─────────────────────────────────────────────
# Stage 3: Install Dependencies
# ─────────────────────────────────────────────
# Copy requirements first (Docker caches this layer for faster rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────
# Stage 4: Copy Application Code
# ─────────────────────────────────────────────
COPY . .

# ─────────────────────────────────────────────
# Stage 5: Expose Port & Run
# ─────────────────────────────────────────────
# Tell Docker this container listens on port 5000
EXPOSE 5000

# Run using gunicorn (production server) with 3 worker processes
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]
