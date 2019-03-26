FROM ubuntu:latest
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2018-10-02
RUN apt-get update -y
RUN apt-get install vim samba ssh rsyslog nmap smbclient -y
RUN rm /etc/samba/smb.conf
ADD dcpromo.py /usr/local/bin/dcpromo.py
RUN mkdir /run/sshd
EXPOSE 22 53 88 135 139 389 445 464 636 1024 3268 3269
CMD /usr/local/bin/dcpromo.py
