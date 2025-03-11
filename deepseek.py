from utils import set_prompt, get_db_connection
from dotenv import load_dotenv
from openai import OpenAI
import time
import os

load_dotenv()

try:
    connection, cursor = get_db_connection(
        "db_name", "username", "host", "root_password", 5432
    )
    # Altere de acordo com a estratégia de prompt
    cursor.execute("SELECT id, transcription, deepseek_zs FROM data")
    rows = cursor.fetchall()
    connection.commit()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    for row in rows:
        if row[2] == None:
            # Altere a entratégia de prompt utilizada
            prompt = set_prompt("./chain-of-thought.txt", row[5])

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="deepseek/deepseek-r1:free",
            )

            # Altere o campo de atualização no DB de acordo com o modelo (linha 27) e prompt (linha 36) utilizado
            cursor.execute(
                "UPDATE data SET deepseek_zs = %s WHERE id = %s",
                (chat_completion.choices[0].message.content.replace("\n", ""), row[0]),
            )
            connection.commit()
            time.sleep(10)
    print("Classificação com DeepSeek concluída!")

except Exception as e:
    print(e)
finally:
    if connection:
        cursor.close()
        connection.close()
