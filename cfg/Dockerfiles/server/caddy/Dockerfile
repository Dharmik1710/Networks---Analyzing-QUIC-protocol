FROM caddy:2
COPY Caddyfile /etc/caddy/Caddyfile
EXPOSE 443

# Install bash and iproute2 using apk (Alpine's package manager)
RUN apk update && apk add --no-cache bash iproute2
