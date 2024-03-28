FROM python:3.11-slim

RUN mkdir /action
WORKDIR /action
RUN pip install pipenv
COPY Pipfile          ./
COPY Pipfile.lock     ./
RUN pipenv sync --system
COPY entrypoint.sh ./
RUN ["chmod", "+x", "entrypoint.sh"]
COPY ghpkgadmin.py    ./

ENTRYPOINT [ "/action/entrypoint.sh" ]
CMD ["--help"]