import os
import psycopg2
from flask import jsonify

def connessione_db():
    return psycopg2.connect(
        host = os.getenv("DB_HOST", "localhost"),
        port = os.getenv("DB_PORT", "5432"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

def inizializza_db():
    comandi = (
        """
        CREATE TABLE IF NOT EXISTS riders(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            vehicle VARCHAR(255) NOT NULL,
            total_deliveries INTEGER NOT NULL DEFAULT 0,
            CONSTRAINT check_rider_vehicle CHECK (LOWER(vehicle) IN ('auto', 'moto', 'scooter', 'bicicletta', 'furgone'))
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews(
            id SERIAL PRIMARY KEY,
            rider_id INTEGER NOT NULL REFERENCES riders(id) ON DELETE CASCADE,
            customer_name VARCHAR(255) NOT NULL,
            rating INTEGER NOT NULL CHECK (rating>=1 AND rating<=5),
            comment TEXT
        );
        """
    )

    conn_db = None
    try:
        conn_db = connessione_db()
        cursore = conn_db.cursor()

        for comando in comandi:
            cursore.execute(comando)

        conn_db.commit()
        cursore.close()
        print("Database PostgreSQL inizializzato con successo (tabelle create/verificate)!")

    except (Exception, psycopg2.DatabaseError) as e:
        raise Exception(f"Errore durante l'inizializzazione del database: {e}")
    finally:
        if conn_db is not None:
            conn_db.close()

def inserisci_rider_nel_db(nome, veicolo, consegne_totali):
    conn_db = None
    try:
        conn_db = connessione_db()
        cursore = conn_db.cursor()
        query = """
            INSERT INTO riders (name, vehicle, total_deliveries)
            VALUES (%s, %s, %s)
            RETURNING id;
        """

        cursore.execute(query, (nome, veicolo, consegne_totali))
        id_generato = cursore.fetchone()[0]
        conn_db.commit()
        cursore.close()
        return id_generato
    except (Exception, psycopg2.DatabaseError) as e:
        raise Exception(f"Errore database: {e}")
    finally:
        if conn_db is not None:
            conn_db.close()