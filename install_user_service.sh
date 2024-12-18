#!/bin/bash

mkdir -p ~/.config/systemd/user
sed "s:PATH_TO_SERVER_SCRIPT:$(pwd)/wol_http_server.py:" wol-http-trigger.service > ~/.config/systemd/user/wol-http-trigger.service