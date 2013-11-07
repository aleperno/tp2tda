#!/bin/bash

count=1

banner(){
echo "################################"
echo "#          Prueba$count        #"
echo "################################"
count=$((count+1))
}

stop(){
echo -e "Presione enter para la siguiente prueba\n"
read opcion
}

banner 
./tdatp2.py "h la" "h la" "costos.txt"
stop

banner
./tdatp2.py "asaods" "dos" "costos.txt"
stop

banner
./tdatp2.py "asaods" "dos" "costos2.txt"
stop

banner
./tdatp2.py "holasobra" "hola" "costos2.txt"
stop

banner
./tdatp2.py "sobre" "sobrefalta" "costos2.txt"
stop

echo "No hay más pruebas"