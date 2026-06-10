import os
import psycopg2
from flask import jsonify

LISTA_VEICOLI_AMMESSI = os.getenv("LISTA_VEICOLI_AMMESSI")

def controllo_veicolo_valido(veicolo):
    return veicolo in LISTA_VEICOLI_AMMESSI


                




