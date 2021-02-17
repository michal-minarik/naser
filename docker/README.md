# Docker image

```bash
./create_container.sh && docker run -it --rm arse:0.0.2 /bin/bash && docker image prune -f
```

Start Selenum grid

```
docker run -d -p 4444:4444 --name selenium-hub selenium/hub:3.4.0
docker run -d --link selenium-hub:hub --shm-size 2g --name firefox selenium/node-firefox:3.4.0
```

Start single node Selenuim
```
docker run -d -p 5901:5901-p 4444:4444 --shm-size 2g selenium/standalone-firefox:4.0.0-beta-1-prerelease-20210128
```
