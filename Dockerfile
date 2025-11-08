# --- Base Image ---
FROM python:3.10-slim

# --- Set Working Directory ---
WORKDIR /app

# --- Install Dependencies ---
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy Application Code ---
COPY . .

# --- Set Default Command ---
CMD ["python", "src/train.py"]