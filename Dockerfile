# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /FlaskApi/requirements.txt

# switch working directory
WORKDIR /FlaskApi

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /FlaskApi

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["api.py" ]