# EPG POC

The EPG PoC is some ideas with meaning - How to implement EPG

## Current content

- [x] simple ETL (get_data.py). It extracts data from API, transforms to json and 'loads' (saves) in local directory
- [x] simple web application (Python3.6, Bottle)
- [x] Dockerfile and additional tools for Docker image as environment for web service

## How to start:

 * clone the repo (# git clone ...)
 * do to a cloned directory (# cd ./epg)
 * build Docker image
 ```docker build --network=host -t epg-poc:0.1 .```
 * run Docker instance 
 ```docker run --rm -ti --network host -p 8080 epg-poc:0.1```
 * got to a web browser and use an address http://localhost:8080
 * wait 2-3 minutes during first run, ETL extracts data from API
