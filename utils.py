import psycopg2
from moviepy import *


def set_prompt(prompt, transcription: str) -> str:
    try:
        with open(prompt, "r", encoding="utf8") as file:
            text = file.read()
            new_prompt = text.replace("[discurso]", transcription)
            return new_prompt
    except Exception as e:
        print("Erro ao configurar o prompt: ", e)


def set_prompt_with_description(prompt, transcription: str, description: str) -> str:
    try:
        with open(prompt, "r", encoding="utf8") as file:
            text = file.read()
            new_prompt = text.replace("[discurso]", transcription)
            new_prompt = new_prompt.replace("[descrição]", description)
            return new_prompt
    except Exception as e:
        print("Erro ao configurar o prompt: ", e)


def extract_audio(video_path, save_path):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(save_path)
    except Exception as e:
        print("Erro ao extrair o áudio: ", e)


def get_db_connection(db_name: str, user: str, host: str, password: str, port: int):
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=user,
            host=host,
            password=password,
            port=port,
        )
        return connection, connection.cursor()
    except Exception as e:
        print("Erro ao tentar estabelecer conexão: ", e)
