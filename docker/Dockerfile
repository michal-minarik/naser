FROM python:3.8.5

ARG firefox_version='firefox-latest'
ARG firefox_os='linux64'
ARG firefox_language='en-US'
ENV geckodriver_version='0.29.0'
ARG ARSE_VERSION='arse:0.0.2'

ARG firefox_temporary='firefox.tar.bz2'

RUN apt update \
  && apt upgrade -y

#RUN echo "/--- Getting Firefox ---/" \
#  && wget -O /tmp/${firefox_temporary} "https://download.mozilla.org/?product=${firefox_version}&os=${firefox_os}&lang=${firefox_language}" \
#  && apt-get -y purge firefox \
#  && rm -rf /opt/firefox \
#  && mkdir -p /opt/firefox \
#  && tar xjf /tmp/${firefox_temporary} -C /opt/ \
#  && rm /tmp/${firefox_temporary} \
#  && ln -fs /opt/firefox/firefox /usr/bin/firefox

RUN echo "/--- Getting Geckodriver ---/" \
  && wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_version}/geckodriver-v${geckodriver_version}-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar zxvf /tmp/geckodriver.tar.gz -C /opt/ \
  && rm /tmp/geckodriver.tar.gz \
  && chmod 755 /opt/geckodriver \
  && ln -fs /opt/geckodriver /usr/bin/geckodriver

#ENV PATH="/opt/firefox:/opt/geckodriver:${PATH}"

# Set headless mode
ENV MOZ_HEADLESS=1

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
#
COPY . .

CMD [ "python3", "2test.py"]
