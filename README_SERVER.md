This is as of Nov 11, 2024.   
Will move to docker images for caddy and nodejs application in future

**Install Caddy**
```
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```
```
cd /etc/caddy
```

**Modify Caddyfile** 
```
  The Caddyfile is an easy way to configure your Caddy web server.
#
# Unless the file starts with a global options block, the first
# uncommented line is always the address of your site.
#
# To use your own domain name (with automatic HTTPS), first make
# sure your domain's A/AAAA DNS records are properly pointed to
# this machine's public IP, then replace ":80" below with your
# domain name.

localhost:443 {
    # Enable TLS for localhost (Caddy will automatically use self-signed certs for localhost)
    tls internal

    # Set the custom header based on the request protocol version (HTTP/1.1, HTTP/2, HTTP/3)
    header {
        X-HTTPS-Version "{http.request.proto}"
    }

    # Reverse proxy requests to your Node.js backend on localhost:8000
    reverse_proxy localhost:8000
}


# Refer to the Caddy docs for more information:
# https://caddyserver.com/docs/caddyfile

```


**Install Node**
```
# installs nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
# download and install Node.js (you may need to restart the terminal)
nvm install 22
# verifies the right Node.js version is in the environment
node -v # should print `v22.11.0`
# verifies the right npm version is in the environment
npm -v # should print `10.9.0`

```
**Backend Nodejs server**
```
cd server
npm start
```

**Test using curl- http2 (TCP) and http3 (QUIC)**
```
    # Response: "Hello World!" (Text) 
    docker run -ti --network host --rm alpine/curl-http3 curl --insecure --http3 -I https://localhost  

    # Response: html and css files
    docker run -ti --network host --rm alpine/curl-http3 curl --insecure --http3 -I https://localhost/files 
```
<!-- for installing curl with http3 -->
<!-- sudo LDFLAGS="-Wl,-rpath,/usr/local/openssl/lib64" ./configure --with-openssl=/usr/local --with-nghttp3=/usr/local --with-ngtcp2=/usr/local -->