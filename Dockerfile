FROM python:3.10.14-slim

ADD src .

RUN chmod +x /start.sh
CMD /start.sh
