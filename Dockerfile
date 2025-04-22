# using python official base image 3.10
FROM python:3.10.14-slim

# install image container dependencies
RUN apt-get update && \
    apt install -y \
    fonts-dejavu-core rsync git jq moreutils aria2 wget libgoogle-perftools-dev libtcmalloc-minimal4 procps libgl1 libglib2.0-0 build-essential && \
    apt-get autoremove -y && rm -rf /var/lib/apt/lists/* && apt-get clean -y
    
# add content of src dir into image root test
ADD src .

# change permission to executable and run start.sh on container start
RUN chmod +x /start.sh
CMD /start.sh
