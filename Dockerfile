FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Creating working directory
RUN mkdir /app
WORKDIR /app

# Set timezone
RUN echo "Asia/Dhaka" > /etc/timezone

# Copy requirements files
COPY ./requirements.txt ./

# Install project dependencies
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends build-essential tzdata
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Add and use a non-root user
RUN useradd --no-create-home --user-group --system --shell /bin/false app
RUN chown -R app:app /app
USER app