#!/bin/bash

# pingar a rota que eu sei que vai gerar log e a'i sim criar o index
curl --insecure https://django/favicon.ico

# sleep pra garantir que o index foi criado já
sleep 5

# e vai tomando
# fazer a requisição pra criar a policy
curl -k --silent --fail -X PUT "http://elasticsearch:9200/django-logs/_settings?pretty" --user "elastic:$ELASTIC_PASSWORD"  -H 'Content-Type: application/json' -d '{
  "index": {
    "lifecycle": {
      "name": "kibana-event-log-policy"
    }
  }
}'

# criar o dataview pra não ter que ficar abrindo e dando discovery
curl --fail -X POST "http://kibana:5601/api/data_views/data_view" \
                     -H 'kbn-xsrf: true' -H 'Content-Type: application/json' \
                     --user "elastic:$ELASTIC_PASSWORD" \
                     -d '{ "data_view": { "title": "django-logs", "name": "django-logs" , "timeFieldName": "@timestamp" } }'

