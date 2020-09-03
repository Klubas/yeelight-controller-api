#!/bin/bash 
balena build --arch amd64 --deviceType qemux86-64
docker run -p 0.0.0.0:5000:5000 yeelight-controller_main