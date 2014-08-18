FROM ubuntu:utopic
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV REFRESHED_AT 2014-08-17-2
# Add PPA and refresh
RUN apt-get -yqq update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:niklas-andersson/dcpromo
RUN apt-get -yqq update
# debconf dcpromo and install
ADD dcpromo.debconf /tmp/dcpromo.debconf
RUN debconf-set-selections /tmp/dcpromo.debconf
RUN apt-get install dcpromo -y
RUN dcpromo
# Add the docker fix
ADD dc.sh /usr/local/bin/dc.sh
#RUN samba-tool user create nandersson Secret012
CMD /usr/local/bin/dc.sh
EXPOSE 53 88 111 135 139 389 445 464 636 1024 3268 3269
