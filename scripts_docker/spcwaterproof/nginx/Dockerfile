FROM nginx



WORKDIR /etc/nginx/

ADD nginx.conf.envsubst nginx.https.available.conf.envsubst spcwaterproof.conf ./

ADD docker-autoreload.sh docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
RUN chmod +x /docker-autoreload.sh
RUN chmod +x /docker-entrypoint.sh

CMD ["nginx", "-g", "daemon off;"]