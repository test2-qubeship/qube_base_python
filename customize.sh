#!/bin/bash
module=$1
repo=$2
sonar_key=$3
language=$4
listener_port=$5
service=$6

if [ -z "$service" ]
then
    echo "Service name is required"
    exit 0
fi

for file in `find . -type f  | grep -v customize.sh| grep -v .whl | grep -v .git| xargs grep -Ril qube_placeholder`; do
  echo "renaming  qube_placeholder to $module in $file"
  sed -i".bak" "s/qube_placeholder/$module/g" $file;
  rm -rf $file.*bak*
done
for file in `find . -type f  | grep -v customize.sh| grep -v .whl | grep -v .git| xargs grep -Ril QUBE_SONAR_KEY`; do
  echo "renaming  QUBE_SONAR_KEY to $sonar_key in $file"
  sed -i".bak" "s/QUBE_SONAR_KEY/$sonar_key/g" $file;
  rm -rf $file.*bak*
done
for file in `find . -type f  | grep -v customize.sh| grep -v .whl | grep -v .git| xargs grep -Ril qube_repo`; do
  echo "renaming  qube_repo to $repo in $file"
  sed -i".bak" "s/qube_repo/$repo/g" $file;
  rm -rf $file.*bak*
done
for file in `find . -type f  | grep -v customize.sh| grep -v .whl| grep -v .git | xargs grep -Ril qube_language`; do
  echo "renaming  qube_language to $language in $file"
  sed -i".bak" "s/qube_language/$language/g" $file;
  rm -rf $file.*bak*
done

for file in `find . -type f  | grep -v customize.sh| grep -v .whl | grep -v .git | xargs grep -Ril qube_listener_port`; do
  echo "renaming  qube_listener_port to $listener_port in $file"
  sed -i".bak" "s/qube_listener_port/$listener_port/g" $file;
  rm -rf $file.*bak*
done

for file in `find . -type f | grep -v .git| grep hello`; do
    service="{$1,,}"
    newfile="${file/hello/$service}"
    echo "renaming $file to $newfile"
    mv $file $newfile
done

for file in `find . -type f  | grep -v customize.sh| grep -v .whl | grep -v .git| xargs grep -Ril Hello`; do
  echo "renaming Hello to $service in $file"
  sed -i".bak" "s/Hello/$service/g" $file;
  rm -rf $file.*bak*
done

for file in `find . -type f  | grep -v customize.sh| grep -v .whl | grep -v .git| xargs grep -Ril hello`; do
  service="{$1,,}"
  echo "renaming hello to $service in $file"
  sed -i".bak" "s/hello/$service/g" $file;
  rm -rf $file.*bak*
done

