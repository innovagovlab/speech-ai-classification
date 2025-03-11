from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from utils import extract_audio, get_db_connection
import psycopg2
import librosa
import torch


try:
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3-turbo"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True,
    )

    connection, cursor = get_db_connection(
        "db_name", "username", "host", "root_password", 5432
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    connection.commit()

    for row in rows:
        if row[5] == None:
            # Caso esteja utilizando a pasta de áudios já separado dos vídeos, adaptar esse if para pegar diretamente o path de áudio
            video_path = f"path_para_pasta_videos/@{row[1]}{row[0]}.mp4"
            save_path = f"./extracted-audio/@{row[1]}{row[0]}.mp3"
            extract_audio(video_path, save_path)

            audio, sr = librosa.load(save_path)
            result = pipe(audio, generate_kwargs={"language": "portuguese"})

            cursor.execute(
                "UPDATE data SET transcription = %s WHERE id = %s",
                (result["text"], row[0]),
            )
            connection.commit()
except (Exception, psycopg2.Error) as error:
    print(error)
finally:
    if connection:
        cursor.close()
        connection.close()
