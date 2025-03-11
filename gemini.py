from utils import set_prompt, get_db_connection
from google import genai
from dotenv import load_dotenv
import time
import os

load_dotenv()

try:
    connection, cursor = get_db_connection(
        "db_name", "username", "host", "root_password", 5432
    )
    # Altere de acordo com a estratégia de prompt
    cursor.execute("SELECT id, transcription, gemini_zs FROM data")
    rows = cursor.fetchall()
    connection.commit()

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    for row in rows:
        if row[2] == None:
            # Altere a entratégia de prompt utilizada
            prompt = set_prompt("./prompts/zero-shot.txt", row[5])

            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )

            # Altere o campo de atualização no DB de acordo com o modelo (linha 27) e prompt (linha 36) utilizado
            cursor.execute(
                "UPDATE data SET gemini_zs = %s WHERE id = %s",
                (response.text.replace("\n", ""), row[0]),
            )
            connection.commit()
            time.sleep(15)
    print("Classificação com Gemini concluída!")
except Exception as e:
    print(e)
finally:
    if connection:
        cursor.close()
        connection.close()
