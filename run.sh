#!/bin/sh
# Run command for the grader: ./run.sh   (reads N on stdin, prints pi(N))
# Uses the committed prebuilt ./primes binary when present; otherwise builds
# it from primes.c first. (To rebuild manually:
#   gcc -O3 -march=native -std=c11 -o primes primes.c )
set -e
cd "$(dirname "$0")"
if [ ! -x primes ]; then
  gcc -O3 -march=native -std=c11 -o primes primes.c
fi
exec ./primes
