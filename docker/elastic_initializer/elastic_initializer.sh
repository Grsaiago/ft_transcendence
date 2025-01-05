#!/bin/bash

# Blocks until the Django service is up
wait_for_django() {
  echo "Waiting for Django service to be available..."
  until curl --insecure --silent --fail https://django/metrics > /dev/null; do
    echo "Django is not ready yet. Retrying in 5 seconds..."
    sleep 5
  done
  echo "Django service is up!"
}

# Blocks until django-logs index is created on elasticsearch
wait_for_elastic_index() {
  echo "Waiting for elastic index to be created"
  until curl --silent --head --fail -X HEAD "http://elasticsearch:9200/django-logs" --user "elastic:$ELASTIC_PASSWORD"; do
    # TODO: essa parte de pingar a rota pode sair quando a gente colocar pra aplicação startar dando um log de ok
    # pingar a rota que eu sei que vai gerar log e aí sim criar o index
    echo "Elastic django-logs index not up yet. Pinging log route on django and then Retrying in 5 seconds..."
    curl --insecure https://django/favicon.ico
    sleep 5
  done
  echo "Elastic index 'django-logs' created!"
}

create_elastic_policy() {
# e vai tomando
# fazer a requisição pra criar a policy
  echo "Requesting policy creation on Elastic..."
  until curl -k --silent --fail -X PUT "http://elasticsearch:9200/django-logs/_settings?pretty" --user "elastic:$ELASTIC_PASSWORD"  -H 'Content-Type: application/json' -d '{"index": {"lifecycle": { "name": "kibana-event-log-policy" }}}'; do
    echo "Policy creation on Elastic failed. Retrying in 5 Seconds..."
    sleep 5
  done
  echo "Elastic Policy created!"
}

# criar o dataview pra não ter que ficar abrindo e dando discovery
create_kibana_data_view() {
echo "Requesting data_view creation on Kibana..."
until curl --fail -X POST "http://kibana:5601/api/data_views/data_view" \
                     -H 'kbn-xsrf: true' -H 'Content-Type: application/json' \
                     --user "elastic:$ELASTIC_PASSWORD" \
                     -d '{ "title": "django-logs", "name": "django-logs" , "timeFieldName": "@timestamp" }'; do
    echo "data_view creation on Kibana failed. Retrying in 5 Seconds..."
    sleep 5
                   done
echo "Kibana Dataview created!"
}


# Wait for Django to be up
wait_for_django

# wait for the elastic index 'django-logs' to be created
wait_for_elastic_index

create_elastic_policy

create_kibana_data_view

