#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
VENV_DIR="venv"
MAIN_SCRIPT="main.py"
FIRST_LAUNCH=0

export PIP_IGNORE_INSTALLED=0

delimiter="################################################################"

printf "\n%s\n" "${delimiter}"
printf "\e[1m\e[32mStable Diffusion Manager\e[0m"
printf "\n%s\n" "${delimiter}"

if [[ $(id -u) -eq 0 ]]
then
    printf "\n%s\n" "${delimiter}"
    printf "\e[1m\e[31mERROR: This script must not be launched as root, aborting...\e[0m"
    printf "\n%s\n" "${delimiter}"
    exit 1
else
    printf "\n%s\n" "${delimiter}"
    printf "Running on \e[1m\e[32m%s\e[0m user" "$(whoami)"
    printf "\n%s\n" "${delimiter}"
fi

if [[ $(getconf LONG_BIT) = 32 ]]
then
    printf "\n%s\n" "${delimiter}"
    printf "\e[1m\e[31mERROR: Unsupported Running on a 32bit OS\e[0m"
    printf "\n%s\n" "${delimiter}"
    exit 1
fi

if ! python3 -c "import venv" &>/dev/null
then
    printf "\n%s\n" "${delimiter}"
    printf "\e[1m\e[31mERROR: python3-venv is not installed, aborting...\e[0m"
    printf "\n%s\n" "${delimiter}"
    exit 1
fi

if [ -z "${VIRTUAL_ENV}" ];
then
    printf "\n%s\n" "${delimiter}"
    printf "\e[1m\e[32mVirtual Environment Manager\e[0m"
    printf "\n%s\n" "${delimiter}"

    if [[ ! -d "${VENV_DIR}" ]]
    then
        printf "%s\n" "Creating new virtual environment"
        python3 -m venv "${VENV_DIR}"
        FIRST_LAUNCH=1
    fi

    if [[ -f "${VENV_DIR}"/bin/activate ]]
    then
        printf "%s" "Activating virtual environment"
        source "${VENV_DIR}"/bin/activate
        printf "\n%s\n" "${delimiter}"
    else
        printf "\n%s\n" "${delimiter}"
        printf "\e[1m\e[31mERROR: Cannot activate virtual environment, aborting...\e[0m"
        printf "\n%s\n" "${delimiter}"
        exit 1
    fi
else
    printf "\n%s\n" "${delimiter}"
    printf "virtual environment is already active"
    printf "\n%s\n" "${delimiter}"
fi

if [[ ${FIRST_LAUNCH} -eq 1 ]]
then
    printf "\n%s\n" "${delimiter}"
    printf "\e[1m\e[32mInstalling requirements\e[0m"
    printf "\n%s\n" "${delimiter}"
    pip install -r "${SCRIPT_DIR}"/requirements.txt
fi

python3 -u "${MAIN_SCRIPT}" "$@"