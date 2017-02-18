#!/usr/bin/env bats


data='{
    "name": "test123123124"
}'

#TOKEN="valueDoesnotMatter"
APIHOST="localhost"
DEFAULT_LISTENER_PORT="3333"

create_sample_data() {
  id=$(curl -H "Authorization: Bearer $TOKEN" -X POST -H "Content-Type: application/json"  -d "${data}" "$URLPATH" | jq '.id' | sed 's/\"//g')
  echo $id >> /tmp/test.out
}

setup() {
    if [ -z "$TOKEN" ]; then
        echo "Please supply access token"> /tmp/error.out
        exit -1;
    fi
    if [ -z "$APIHOST" ]; then
      echo "Please supply API HOST"> /tmp/error.out
      exit -1;
    fi
    if [ -z "DEFAULT_LISTENER_PORT" ]; then
      echo "Please supply DEFAULT_LISTENER_PORT" > /tmp/error.out
      exit -1;
    fi

    if [ -z "$(which jq)" ]; then
         echo "Please install jq" > /tmp/error.out
         exit -1;
    fi
  # source the file, now all mcwrapper functions
  # are available in all my tests
  #APIHOST="localhost"
  #DEFAULT_LISTENER_PORT="9000"
  URL="http://$APIHOST:${DEFAULT_LISTENER_PORT}"
  URLPATH="$URL/hello"
  create_sample_data
}

teardown() {
  delete_sample_data
}

delete_sample_data() {
  echo curl -H "Authorization: Bearer $TOKEN" -X DELETE -H "Content-Type: application/json" "$URLPATH/$id" >> /tmp/test.out
  curl -H "Authorization: Bearer $TOKEN" -X DELETE -H "Content-Type: application/json" "$URLPATH/$id" >> /tmp/test.out
}

@test "get_status_code" {

	run curl -H "Authorization: Bearer $TOKEN" -s -w "%{http_code}" -X GET -o /dev/null $URLPATH
  echo "get_status_code" $id $status $output $URLPATH >> /tmp/test.out
  [ "$output" -eq 200 ]
}

