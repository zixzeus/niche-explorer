# Multi-language Dockerfile for Next.js + Python LangGraph Agent

# Step 1: Base Image
FROM node:20-slim AS base

# Step 2: Install Python and System Dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHON_PATH=/usr/bin/python3

ENV PORT=8080

WORKDIR /app

# Step 3: Install Python Dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt

# Step 4: Install Node.js Dependencies
COPY web/package.json web/package-lock.json* ./web/
RUN cd web && npm install

# Step 5: Copy Source Code
COPY . .

# Step 6: Build Next.js App
RUN cd web && npm run build

# Step 7: Run Application
ENV NODE_ENV=production
EXPOSE 8080

# Next.js App Router usually starts from the web directory
WORKDIR /app/web
CMD ["npm", "start", "--", "-p", "8080"]
