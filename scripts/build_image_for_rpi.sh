#!bin/bash
docker buildx build -t cthulhu:1.0.0 -t cthulhu:latest --no-cache --platform linux/arm/v7 --output "type=docker,dest=/Users/grzegorzstysiak/Repos/images/rpi_build.tar" .