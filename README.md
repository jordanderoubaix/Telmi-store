# Project Title

Generate json store file for a Telmi library.

## Pre-requisites
On a server / synology, there must be a folder with the Telmi library.
In this example, the share is mounted on /mnt/nfs/telmiLibrary

In the folder, it will store all .zip folder for all stories and a new folder "data" will be generated with the extracted files (json, images):
- zip: contains the zip files of stories
- data: contains the extracted zip files

## Installation

Add NFS share to host

```bash
sudo mount -t nfs
```

Build docker image

```bash
docker build -t telmi-store .
```

Run docker image

```bash
docker run -d -p 80:8888 \
  -e TARGET_URL="http://new.target.url" \
  -e BANNER_IMAGE="http://new.banner.image" \
  -e BANNER_LINK="http://new.banner.link" \
  -e BANNER_BACKGROUND="#123456" \
  -e LOG_LEVEL="DEBUG" \
  -v /MountedVolumeOnHost/Stories:/mnt/nfs/telmiLibrary \
  jordanderoubaix/telmi-store:latest
```
