FROM alpine/curl-http3
USER root

# Install bash and the required networking tools
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

RUN mkdir -p /CURL_logs /QUIC_captures /TCP_captures
COPY curl_request.sh /curl_request.sh
RUN chmod +x /curl_request.sh
# ENTRYPOINT ["/bin/bash", "/curl_request.sh"]
