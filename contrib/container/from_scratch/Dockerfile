FROM debian:12-slim AS os-updates

RUN apt update && apt upgrade -y


FROM os-updates AS base

RUN apt install -y python3 git

COPY ./builder /builder

WORKDIR /builder

RUN ./build_base.py


FROM os-updates AS sage-build

WORKDIR /builder

RUN ./build_main.py


CMD ["/bin/bash"]

