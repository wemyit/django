FROM debian:stable-slim

ENV PYTHONUNBUFFERED=1 DOCKER=1 DEBIAN_FRONTEND=noninteractive

# Add support for apt-* packages caching through "apt-cacher-ng"
ARG APTPROXY
RUN bash -c 'if [ -n "$APTPROXY" ]; then echo "Acquire::HTTP::Proxy \"http://$APTPROXY\";" > /etc/apt/apt.conf.d/01proxy; fi'

## Install dependencies
RUN apt-get update \
    && apt-get --no-install-recommends install -y wget apt-utils vim-tiny \

    # Install latest NodeJS + NPM
    && apt-get --no-install-recommends install -y curl ca-certificates apt-transport-https lsb-release \
    && curl -sSL https://deb.nodesource.com/setup_7.x | bash - \
    && apt-get --no-install-recommends install -y nodejs \

    # Install global NPM packages
    && npm install -g webpack \

    # Python system packages
    && apt-get --no-install-recommends install -y python3 python3-pip python3-dev \
    # PIP build dependencies
    gcc libssl-dev \

    && pip3 install -U pip 3to2 \

    # Backup dependencies
    && wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add - \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" >> /etc/apt/sources.list.d/pgdg.list \
    && mkdir -p /usr/share/man/man1/ /usr/share/man/man7/ \
    && apt-get update && apt-get install -y postgresql-client-9.6 cron \

    # System stuff
    && apt-get --no-install-recommends install -y nginx-extras \

    # Cleanup after installation
    && npm cache clear \
    && rm -rf /tmp/npm-* \
    && apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -fr /var/lib/apt/lists/* \

    # Create basic project structure
    && mkdir -p /app/project/assets/ /app/logs /app/tmp/

WORKDIR /app/

# Add packages.json (NPM) & requirements.txt (PIP) files to the image
ADD requirements.txt /app/requirements.txt
ADD project/assets/package.json /app/project/assets/package.json

# Install NPM & Python dependencies
RUN pip3 install -U -r /app/requirements.txt --no-cache-dir
RUN cd /app/project/assets/ \
    && npm install \
    && npm cache clear

ADD . /app/

RUN cd /app/project/assets/ \
    && npm run build
RUN python3 manage.py collectstatic --noinput -v0

# Backup data every day
RUN (crontab -l 2>/dev/null; echo "00 04 * * * /app/manage.py dbbackup -z") | crontab - \
    && cron

ADD docker/production/nginx/nginx.conf /etc/nginx/sites-enabled/project
ADD docker/production/nginx/conf.d/* /etc/nginx/conf.d/

EXPOSE 80
