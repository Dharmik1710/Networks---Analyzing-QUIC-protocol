FROM node:18

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .

# Install required tools
RUN apt-get update && apt-get install -y \
    iproute2 \
    iputils-ping \
    net-tools \
    tcpdump \
    curl \
    wget \
    telnet \
    iperf3 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 9000

CMD ["node", "app.js"]
