FROM python:3.7
COPY crontask /etc/cron.d/crontask
WORKDIR /srv
RUN apt-get update && apt-get install -y --no-install-recommends cron git wget && pip install -U Flask && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* && touch /home/boot.sh && echo "#!/bin/sh\n" > /home/boot.sh && echo "service cron start" >> /home/boot.sh && echo "\n" >> /home/boot.sh && echo "/usr/local/bin/python /srv/iptv/python/main.py" >> /home/boot.sh && echo "\n" >> /home/boot.sh && echo "/bin/bash" >> /home/boot.sh && chmod +x /home/boot.sh
#RUN git clone https://github.com/CharysseZ/iptv-m3u-maker.git && mv iptv-m3u-maker iptv
WORKDIR /srv/iptv
CMD ["/bin/bash", "/home/boot.sh"]
