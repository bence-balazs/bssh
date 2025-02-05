#!/bin/sh

debian_dockerfile="containers/Dockerfile.deb"
alpine_dockerfile="containers/Dockerfile.alp"

debian_img="pybuilder:deb"
alpine_img="pybuilder:alp"

if [ "$1" = "build" ]; then
    rm dist/*
    docker build --no-cache -t ${alpine_img} -f ${alpine_dockerfile} .
    docker build --no-cache -t ${debian_img} -f ${debian_dockerfile} .
    docker run --rm -it -v ./dist:/data ${debian_img}
    docker run --rm -it -v ./dist:/data ${alpine_img}
else
    echo "Options: [$0 build]"
fi
