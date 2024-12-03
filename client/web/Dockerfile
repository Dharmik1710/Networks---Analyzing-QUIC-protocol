FROM alpine/curl-http3
USER root
RUN apk add --no-cache bash
RUN mkdir -p /CURL_logs /QUIC_captures /TCP_captures
COPY curl_request.sh /curl_request.sh
RUN chmod +x /curl_request.sh
ENTRYPOINT ["/bin/bash", "/curl_request.sh"]
