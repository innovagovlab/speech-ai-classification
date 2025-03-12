from utils import set_prompt_with_description, get_db_connection
from dotenv import load_dotenv
from openai import OpenAI
import time
import os

load_dotenv(override=True)

try:
    connection, cursor = get_db_connection(
        "video_transcription", "postgres", "localhost", "28240907", 5432
    )
    # Altere de acordo com a estratégia de prompt
    cursor.execute("SELECT id, transcription, post_description, llama_fs FROM data2")
    rows = cursor.fetchall()
    connection.commit()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    for row in rows:
        if row[3] == None:
            # Altere a entratégia de prompt utilizada
            prompt = set_prompt_with_description("./prompts/few-shot.txt", row[1], row[2])

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="meta-llama/llama-3.3-70b-instruct:free",
            )

            # Altere o campo de atualização no DB de acordo com o modelo (linha 27) e prompt (linha 36) utilizado
            cursor.execute(
                "UPDATE data2 SET llama_fs = %s WHERE id = %s",
                (chat_completion.choices[0].message.content.replace("\n", ""), row[0]),
            )
            connection.commit()
            time.sleep(15)
    print("Classificação com Llama concluída!")
except Exception as e:
    print(e)
finally:
    if connection:
        cursor.close()
        connection.close()
