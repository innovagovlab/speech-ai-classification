from utils import get_db_connection

try:
    connection, cursor = get_db_connection(
        "video_transcription", "postgres", "localhost", "28240907", 5432
    )
    # Altere de acordo com a estratégia de prompt
    cursor.execute("SELECT id, transcription FROM data")
    rows = cursor.fetchall()
    connection.commit()

    for row in rows:
        words = row[1].split()
        word_count = len(words)
        char_count = len(row[1].strip())
        
        cursor.execute(
            "UPDATE data SET transcription_word_count = %s, transcription_char_count = %s WHERE id = %s",
            (word_count, char_count, row[0]),
        )
        connection.commit()
except Exception as e:
    print(e)
finally:
    if connection:
        cursor.close()
        connection.close()
