# Dockerized Web and Video Services with Caddy Reverse Proxy

## Overview
This project sets up two services for serving web pages and video content via **HTTP/2 (TCP)** and **HTTP/3 (QUIC)**. The system uses **Docker** to containerize both services and **Caddy** as a reverse proxy that handles HTTPS and protocol versioning. The services include:

- **web-service**: A Node.js service for handling web content (HTML, CSS, JS).
- **video-service**: A Node.js service for serving static video files and streaming video content.

Caddy will run as a Docker container, managing traffic on **port 443** and proxying requests to the web and video services.

---

## Docker Setup

## 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

## 2. Build and Start the Services with Docker Compose
Once the images are built, you can use Docker Compose to start all the services (web-service, video-service, and Caddy) together. Simply run:

```bash
docker-compose up --build
```

This will start the web-service on port 8000, the video-service on port 9000, and Caddy on port 443.

## 4. Access the Services

After running `docker-compose up`, you can access the services as follows:

```bash
# Test the web service (returns HTML content or "Hello World!")
curl http://localhost:8000/web/<optional-element>

# Test the video service (retrieves a specific video)
curl http://localhost:9000/video/<optional-element>
```

- **Web Service:** [https://localhost/web/index.html](https://localhost/web/index.html) (This will return the main web page or "Hello World!")
- **Web Service Files:** [https://localhost/web/files](https://localhost/web/files) (This will return web files)
- **Video Service:** [https://localhost/video/:filename](https://localhost/video/:filename) (Replace `:filename` with a valid video filename to fetch a video)
- **Video Stream:** [https://localhost/video/stream/:filename](https://localhost/video/stream/:filename) (Streams the video content)

### Caddy Configuration in Docker

The Caddy server in this setup is configured to handle the following:

- HTTP/3 (QUIC) support for faster connections.
- HTTPS via self-signed certificates for local testing.
- Reverse Proxy for routing requests to web-service on port 8000 and video-service on port 9000.

### Caddyfile:
Caddy uses a Caddyfile to configure its reverse proxy behavior. Here's how it's set up:

```bash
localhost:443 {
    # Enable TLS for localhost (Caddy will automatically use self-signed certs for localhost)
    tls internal

    # Set the custom header based on the request protocol version (HTTP/1.1, HTTP/2, HTTP/3)
    header {
        X-HTTPS-Version "{http.request.proto}"
    }

    # Reverse proxy requests to the web-service on localhost:8000
    reverse_proxy /web* web-service:8000

    # Reverse proxy requests to the video-service on localhost:9000
    reverse_proxy /video* video-service:9000
}
```

- TLS: Caddy will use self-signed certificates for local testing, automatically enabling HTTPS.
- Protocol header: Caddy sets the X-HTTPS-Version header to indicate the protocol version being used (HTTP/1.1, HTTP/2, or HTTP/3).
- Reverse Proxy: Requests to the root (/web/) are proxied to the web-service, and requests starting with /video/ are proxied to the video-service.

### Sending Requests (Testing with curl)
You can use curl to test the HTTP/2 (TCP) and HTTP/3 (QUIC) functionality.

#### For HTTP/3 (QUIC) Requests:
Use the --http3 flag with curl to test the video and web services:

```bash
# Test the web service (returns HTML content or "Hello World!")
curl -I -k --http3 https://localhost/web/<optional-element>

# Test the video service (retrieves a specific video)
curl -I -k --http3 https://localhost/video/<optional-element.mp4>

# Test video streaming
curl -I -k --http3 https://localhost/video/stream/<optional-element.mp4>
```

#### For HTTP/2 (TCP) Requests:
To test HTTP/2 (TCP), just omit the --http3 flag:

```bash
# Test the web service with HTTP/2
curl -I -k https://localhost/web/<optional-element>

# Test the video service with HTTP/2
curl -I -k https://localhost/video/<optional-element.mp4>
```

#### For Dockerized curl with HTTP/3:
Alternatively, you can run curl inside a Docker container that supports HTTP/3:

```bash
# Test the web service with HTTP/3 in Docker
docker run -ti --network host --rm alpine/curl-http3 curl --insecure --http3 -I https://localhost/web/index.html

# Test the video service with HTTP/3 in Docker
docker run -ti --network host --rm alpine/curl-http3 curl --insecure --http3 -I https://localhost/video/your-video.mp4
```

## Dockerized Services
Both the web-service and video-service are running in their own Docker containers. Here’s a quick overview:

Dockerfile: Each service has its own Dockerfile that sets up the necessary environment and dependencies.
Docker Compose: The docker-compose.yml file orchestrates the containers, setting up networks and linking services together.

### Useful Troubleshoot Commands:
To start the services, just run:

```bash
docker-compose up
docker images
docker logs <continer-id>
docker ps
docker-compose restart <service-name>

# When you encounter service build issues due to existing processes
sudo lsof -i :<PID>
sudo kill <PID>



```
This will automatically build and run all the containers.

## Node.js Backend Servers
Both web-service and video-service are Node.js applications, and you can run them within Docker containers, which eliminates the need for manual setup outside the container.

web-service: This service handles the web content (HTML, CSS, JS).
video-service: This service serves video files and streams video content.
Both services are started automatically when you run docker-compose up.

## Conclusion
This setup uses Docker to containerize the web-service, video-service, and Caddy as a reverse proxy. Caddy handles the HTTPS traffic, provides HTTP/3 (QUIC) support, and proxies the requests to the appropriate services. Docker Compose is used to manage the services, and the containers communicate with each other over a private network.