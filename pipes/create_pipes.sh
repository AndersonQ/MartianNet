#!/bin/bash

./remove_pipes.sh

mkfifo /tmp/mars_in_pipe
mkfifo /tmp/mars_out_pipe
mkfifo /tmp/earth_in_pipe
mkfifo /tmp/earth_out_pipe
chmod 777 /tmp/mars_in_pipe
chmod 777 /tmp/mars_out_pipe
chmod 777 /tmp/earth_in_pipe
chmod 777 /tmp/earth_out_pipe
