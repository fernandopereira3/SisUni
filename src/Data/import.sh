#!/bin/bash
# Script de importação executado automaticamente na inicialização do container

CSV_FILE="db.json"

if [ -f "$CSV_FILE" ]; then
    echo "Iniciando importação de $CSV_FILE..."
    mongoimport --db cpppac --collection sentenciados --type json --file "$CSV_FILE" --jsonArray
    echo "Importação FINALIZADA."
else
    echo "Arquivo $CSV_FILE não encontrado. Importação pulada."
fi

#mongoimport --db cpppac --collection sentenciados --type csv --file "$CSV_FILE" --headerline