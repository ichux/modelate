#!/bin/sh

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit

# shellcheck disable=SC2039
# fail exit if one of your pipe command fails
set -o pipefail

# exits if any of your variables is not set
set -o nounset

requirements(){
  pip install `cat requirements.txt | sed 's/==.*//g' | tr '\n' ' '`

  libraries=`cat requirements.txt | sed 's/==.*//g' | tr '\n' '|'`
  libs=$(pip list | grep -E -i "$libraries" | tr -s ' ')

  listed=`echo "${libs// /==}"`

  set +o noclobber
  # shellcheck disable=SC2039
  printf "${listed// /\\n}" | awk 'NR>2' >requirements.txt
}

requirements
