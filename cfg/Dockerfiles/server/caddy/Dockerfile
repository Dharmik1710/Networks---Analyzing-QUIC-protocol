FROM caddy:2.9
COPY Caddyfile /etc/caddy/Caddyfile
EXPOSE 8443

# Install bash and iproute2 using apk (Alpine's package manager)
RUN apk update && apk add --no-cache bash iproute2


RUN apk add --no-cache \
    bash \
    iproute2 \
    iputils \
    net-tools \
    tcpdump \
    curl \
    wget \
    busybox-extras \
    iperf3