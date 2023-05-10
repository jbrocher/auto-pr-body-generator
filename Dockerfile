# Container image that runs your code
FROM python:3.10.8

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY main.py /main.py
COPY entrypoint.sh /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
