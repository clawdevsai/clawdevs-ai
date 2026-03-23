FROM searxng/searxng:latest

COPY docker/searxng-runtime/limiter.toml /etc/searxng/limiter.toml

RUN set -eux; \
    cp /usr/local/searxng/searx/settings.yml /etc/searxng/settings.yml; \
    awk '\
      BEGIN { skip = 0 } \
      { \
        if ($0 ~ /^  - name: (google|ahmia|torch)$/) { skip = 1; next } \
        if (skip == 1) { \
          if ($0 ~ /^  - name: /) { skip = 0 } else { next } \
        } \
        print $0 \
      } \
    ' /etc/searxng/settings.yml > /etc/searxng/settings.yml.tmp; \
    mv /etc/searxng/settings.yml.tmp /etc/searxng/settings.yml; \
    sed -i 's/instance_name: "SearXNG"/instance_name: "ClawDevs Search"/g' /etc/searxng/settings.yml; \
    sed -i 's/default_lang: "auto"/default_lang: "pt-BR"/g' /etc/searxng/settings.yml; \
    awk '\
      { print } \
      /^  formats:$/ { \
        if (getline > 0) { \
          if ($0 ~ /^    - html$/) { \
            print $0; \
            print "    - json"; \
            next \
          } \
          print $0 \
        } \
      } \
    ' /etc/searxng/settings.yml > /etc/searxng/settings.yml.tmp; \
    mv /etc/searxng/settings.yml.tmp /etc/searxng/settings.yml
