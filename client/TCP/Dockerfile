FROM alpine/curl-http3

USER root

RUN apk add --no-cache bash

COPY tcp_send_request.sh /tcp_send_request.sh

RUN chmod +x /tcp_send_request.sh

# CMD ["./tcp_send_request.sh"]

ENTRYPOINT [ "/bin/bash", "/tcp_send_request.sh" ]