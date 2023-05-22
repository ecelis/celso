#!/bin/sh

for i in $(cat .env); do
  export $i
done
