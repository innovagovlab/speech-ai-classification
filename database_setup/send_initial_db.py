from utils import get_db_connection
import psycopg2
import csv

try:
    connection, cursor = get_db_connection(
        "db_name", "username", "host", "root_password", 5432
    )

    with open("database_setup/data.csv", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        header = True
        for row in csv_reader:
            if header:
                header = False
                continue
            else:
                cursor.execute(
                    "INSERT INTO data(id, profile, aristotelian_rhetoric, tone, approach, post_description) VALUES (%s, %s, %s, %s, %s, %s)",
                    (row[13], row[2], row[16], row[20], row[19], row[9]),
                )
                connection.commit()
except (Exception, psycopg2.Error) as error:
    print(error)
finally:
    if connection:
        cursor.close()
        connection.close()
