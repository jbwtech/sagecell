FROM debian:13-slim

RUN apt update && apt upgrade -y

RUN apt install -y python3 git

COPY ./builder /builder

WORKDIR /builder

CMD ["/bin/bash"]

