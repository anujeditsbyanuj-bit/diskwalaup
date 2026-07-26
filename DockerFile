FROM python:3.10-slim

WORKDIR /app

# Only the packages the bot actually needs at runtime.
# (Removed: git, openssh-client, docker.io — the bot has no legitimate
#  reason to touch git-over-SSH or the host's Docker daemon.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg aria2 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
