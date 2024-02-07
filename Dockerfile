FROM python:3.11.4-slim-buster
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# FROM base as prod
# # install system dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc && \
#     apt-get update && apt-get install -y --no-install-recommends netcat && \
#     rm -rf /var/lib/apt/lists/*