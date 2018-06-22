FROM ubuntu:16.04

RUN apt-get update

WORKDIR /app

COPY ./www /app

ADD requirement.pip ./

# RUN apt-get -y install nginx
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install -r ./requirement.pip
RUN rm -f a/98df4329b7464466a1fd2dcbd153f2e3.db3
RUN rm -f test
RUN python sshop/models.py
RUN groupadd -g 344 MARS
RUN useradd -g MARS --create-home --no-log-init --shell /bin/bash MARS
RUN chown MARS /app/a -R
RUN chgrp MARS /app/a -R
RUN chmod 777 /app/a/98df4329b7464466a1fd2dcbd153f2e3.db3     
RUN chmod 544 /app/flag
RUN chmod 555 sshop/ -R
USER MARS

CMD python main.py 