FROM python:3.11-slim

RUN mkdir /action
WORKDIR /action
RUN pip install pipenv
COPY Pipfile          ./
COPY Pipfile.lock     ./
RUN pipenv sync
COPY ghpkgadmin.py    ./
#COPY entrypoint.sh ./
#RUN ["chmod", "+x", "entrypoint.sh"]

#ENTRYPOINT ["/entrypoint.sh"]
#CMD ["help"]
#ENTRYPOINT ["/.local/bin/pipenv" "run" "ghpkgadmin"]
#CMD ["--help"]
ENTRYPOINT ["/usr/local/bin/pipenv", "run", "ghpkgadmin"]
CMD ["--help"]