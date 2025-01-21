from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
from app.database import engine
from cryptography.fernet import Fernet

# Generar una clave única para el cifrado (debería ser gestionada de manera segura)
cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)

def encrypt_data(value: str) -> str:
    """
    Cifra un valor. Convierte valores no string a string antes de cifrar.
    """
    if value is not None:
        # Asegúrate de que el valor sea una cadena
        value = str(value)
        return cipher.encrypt(value.encode()).decode()
    return value


def process_csv_batch(file, table_name: str, batch_size: int = 3000):
    """
    Procesa un archivo CSV y lo inserta en la tabla especificada por lotes,
    asegurando que IDENTITY_INSERT esté activado.
    """
    # Leer el archivo CSV
    data = pd.read_csv(file)
    print(f"Datos leídos del archivo:\n{data.head()}")

    # Reemplazar NaN con None en todas las columnas del DataFrame
    data = data.where(pd.notnull(data), None)


    # Limpiar todas las columnas reemplazando cadenas vacías por None
    data = data.applymap(lambda x: None if isinstance(x, str) and x == "" else x)


    # Cifrar datos sensibles antes de la inserción
    if "email" in data.columns:
        data["email"] = data["email"].apply(encrypt_data)
    if "identification_number" in data.columns:
        data["identification_number"] = data["identification_number"].apply(encrypt_data)

    with Session(engine) as session:
        rows_inserted = 0

        try:
            # Activar IDENTITY_INSERT
            session.execute(text(f"SET IDENTITY_INSERT {table_name} ON"))
            session.commit()

            for i in range(0, len(data), batch_size):
                # Seleccionar un lote de datos
                batch = data.iloc[i:i + batch_size]

                # Crear una lista de diccionarios para la inserción
                records = batch.to_dict(orient="records")

                # Generar la consulta de inserción manualmente
                for record in records:
                    columns = ', '.join(record.keys())
                    values = ', '.join([f":{key}" for key in record.keys()])
                    query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
                    session.execute(query, record)

                rows_inserted += len(batch)
                print(f"Lote de {len(batch)} filas insertado.")

            # Confirmar la transacción
            session.commit()
            print(f"Total de filas insertadas: {rows_inserted}")

        except Exception as e:
            session.rollback()
            print(f"Error durante la inserción: {e}")
            raise e

        finally:
            try:
                # Asegurarse de desactivar IDENTITY_INSERT
                session.execute(text(f"SET IDENTITY_INSERT {table_name} OFF"))
                session.commit()
            except Exception as e:
                print(f"Error al desactivar IDENTITY_INSERT: {e}")

        return rows_inserted
