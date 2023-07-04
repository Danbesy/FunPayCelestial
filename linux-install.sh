#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

set -e

echo -e "${MAGENTA}Установщик FunPayCelestial${NC}"
echo -e "${MAGENTA}By Danbesy${NC}\n"

echo -e "${MAGENTA}Обновление пакетов..${NC}"
sudo apt update -y && sudo apt upgrade -y

echo -e "${MAGENTA}Установка языкового пакета..${NC}"
sudo apt install -y language-pack-ru

echo -e "${MAGENTA}Проверка локалей..${NC}"
if ! locale -a | grep -q 'ru_RU.utf8'; then
    echo -e "${MAGENTA}Обновление локалей..${NC}"
    sudo update-locale LANG=ru_RU.utf8

    echo -e "${MAGENTA}Локали ещё не установлены. Пожалуйста, перезапустите терминал и повторите команду запуска скрипта.${NC}"
    exit 1
fi

echo -e "${MAGENTA}Установка software-properties-common..${NC}"
sudo apt install -y software-properties-common

echo -e "${MAGENTA}Добавление репозитория deadsnakes/ppa..${NC}"
sudo add-apt-repository -y ppa:deadsnakes/ppa

echo -e "${MAGENTA}Переход в домашнюю директорию..${NC}"
cd ~

echo -e "${MAGENTA}Установка Python 3.11 и зависимостей..${NC}"
sudo apt install -y python3.11 python3.11-dev python3.11-gdbm python3.11-venv
wget https://bootstrap.pypa.io/get-pip.py -nc
sudo python3.11 get-pip.py

rm -rf get-pip.py

echo -e "${MAGENTA}Установка git..${NC}"
sudo apt install -y git

sudo rm -rf FunPayCelestial 

echo -e "${MAGENTA}Клонирование репозитория FunPayCelestial..${NC}"
git clone https://github.com/Danbesy/FunPayCelestial 

echo -e "${MAGENTA}Переход в директорию FunPayCelestial..${NC}"
cd FunPayCelestial

echo -e "${MAGENTA}Установка зависимостей бота..${NC}"
sudo python3.11 setup.py

echo -e "${MAGENTA}Сейчас необходимо выполнить первичную установку${NC}"
sudo python3.11 main.py

echo -e "${MAGENTA}Хорошо, теперь добавим бота как фоновый процесс${NC}"

echo -e "${MAGENTA}Установка curl..${NC}"
sudo apt-get install -y curl

echo -e "${MAGENTA}Загрузка NodeJS..${NC}"
curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -

echo -e "${MAGENTA}Установка NodeJS..${NC}"
sudo apt -y install nodejs

echo -e "${MAGENTA}Установка pm2..${NC}"
sudo npm install -g pm2

pm2 start main.py --interpreter=python3.11 --name=FunPayCelestial
pm2 save
pm2 startup

echo -e "\n${MAGENTA}Установка FunPayCelestial завершена!${NC}"
echo -e "${MAGENRA}Для просмотра логов используйте команду: pm2 logs FunPayCelestial${NC}"

pm2 logs FunPayCelestial 