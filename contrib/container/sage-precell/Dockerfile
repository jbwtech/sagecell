FROM sagemath/sagemath:10.7 AS sage-precell

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y

COPY ./packages /tmp/

RUN apt install -y $(cat /tmp/sage-recommendations.txt)
RUN apt install -y $(cat /tmp/sage-optional.txt)
RUN apt install -y $(cat /tmp/sage-precell_1.txt)
RUN apt install -y $(cat /tmp/sage-precell_2.txt)
RUN apt clean

RUN for PKG in $(cat /tmp/sage-precell_R.txt); do Rscript -e "install.packages(${PKG})"; done

USER sage
WORKDIR /home/sage
RUN for PKG in $(cat /tmp/sage-pip-install.txt); do sage -pip install ${PKG}; done

