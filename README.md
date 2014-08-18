Docker DC is an implementation of Samba4 AD DC in Docker.

Prerequisites:

 * The Ubuntu images. Utopic is essential when we later want to join using realmd. Samba 4.1.6 in Trusty wont work.  (sudo docker pull ubuntu)

Howto:

 * Modify the contents of dcpromo.debconf to reflect your domain.
 * Build the image: (sudo docker -t xnandersson/dc:utopic .)
 * Run it: (sudo docker run -d -P --hostname=dc --name=dc xnandersson/dc:utopic)

