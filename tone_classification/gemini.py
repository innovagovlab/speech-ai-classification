from utils import set_prompt_with_description, get_db_connection
from google import genai
from dotenv import load_dotenv
import time
import os

load_dotenv(override=True)

try:
    connection, cursor = get_db_connection(
        "video_transcription", "postgres", "localhost", "28240907", 5432
    )
    # Altere de acordo com a estratégia de prompt
    cursor.execute("SELECT id, transcription, post_description, tone_gemini_cot FROM data")
    rows = cursor.fetchall()
    connection.commit()

    key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=key)

    for row in rows:
        if row[3] == None:
            # Altere a entratégia de prompt utilizada
            prompt = set_prompt_with_description(
                "tone_classification/prompts/tone-chain-of-thought.txt", row[1], row[2]
            )

            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )

            # Altere o campo de atualização no DB de acordo com o modelo (linha 27) e prompt (linha 36) utilizado
            cursor.execute(
                "UPDATE data SET tone_gemini_cot = %s WHERE id = %s",
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
