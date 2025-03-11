## Classificação de transcrição de vídeos
Repositório utilizado para armazenar os códigos de teste para os experimentos de pesquisa relacionado a classificação da retórica aristotélica dos discursos transcritos de vídeos das redes sociais de políticos.
## Requisitos
 - Python 3.12.7
 - Postgresql 17
 - [OpenRouter API Key](https://openrouter.ai/)
 - [Google Gemini API Key](https://aistudio.google.com/app/apikey)


## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/ed-cavalcanti/speech-ai-classification
```

Entre no diretório do projeto

```bash
  cd speech-ai-classification
```

Criar o ambiente virtual:
```bash
  python -m venv venv
```

Ativar o ambiente virtual:

No Windows:

```bash
venv\Scripts\activate
```

No macOS/Linux:

```bash
source venv/bin/activate
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```

Abra o código com a IDE de sua preferencia

Faça uma cópia do arquivo `.env.example` e renomei para `.env`

Adicione suas chaves de API ao arquivo `.env` recem criado

---

## Subindo o banco de dados

Cria um novo banco de dados no Postgres:

```bash
  CREATE DATABASE video_transcription;
```

Utilize o arquivo `db.sql` contido dentro da pasta `database_setup` para criar a tabela de dados

No arquivo `send_initial_db` adicione suas credencias do banco de dados Postgress

Rode o script para enviar as informações iniciais do CSV original para o banco de dados:
```bash
  python .\database_setup\send_initial_db.py
```


## Documentação

### Transcrição de áudio

Foi utilizado a função `extract_audio` no arquivo `utils.py` que utiliza como base a biblioteca `moviepy` para separar a faixa de áudio dos vídeos.

- Arquivos de faixa de áudio separados:

Utiliza o modelo Whisper V3 Large Turbo, disponibilizado no [Hugging Face](https://huggingface.co/openai/whisper-large-v3-turbo)

Antes de transcrever o audio, atente-se as configurações do arquivo `audio-transcription.py`:


- Atualize o caminho para a pasta de vídeos
- Atualize o caminho onde deseja salvar as faixas de áudio
- Insira as credenciais do seu banco de dados

Execute o arquivo `audio-transcription.py`:
```bash
  python audio-transcription.py
```
⚠️ A transcrição de áudio precisa ser executada apenas uma vez

### Classificação com Gemini

Foi utilizado a API do Google com o pacote `google-genai` para realizar chamadas ao modelo `Gemini 2.0 Flash`

Antes de executar o arquivo `gemini.py`, atente-se as configurações do arquivo:

- Insira as credenciais do seu banco de dados
- Verifique se a chave `GEMINI_API_KEY` está corretamente inserida no arquivo `.env`
- Altere as estratégias de prompt de acordo com as necessidades, atualizando as linhas 14, 23 e 31

Execute o arquivo `gemini.py`:
```bash
  python gemini.py
```
A execução pode demorar algumas horas, aguarde a mensagem de finalização do script.

### Classificação com Llama e DeepSeek

Foi utilizado a API do OpenRouter com o pacote `openai` para realizar chamadas ao modelo `Llama 3.3 70B` e `DeepSeek R1`

Antes de executar o arquivo `llama.py` ou `deepseek.py`, atente-se as configurações do arquivo:

- Insira as credenciais do seu banco de dados
- Verifique se a chave `OPENROUTER_API_KEY` está corretamente inserida no arquivo `.env`
- Altere as estratégias de prompt de acordo com as necessidades, atualizando as linhas 14, 26 e 40

⚠️ A chave de API do OpenRouter é limitada a 200 requisições diárias aos modelos da categoria `free`

Execute o arquivo `llama.py`:
```bash
  python llama.py
```

ou

```bash
  python deepseek.py
```
A execução pode demorar algumas horas, aguarde a mensagem de finalização do script.

### Métricas

Foram utilizadas as bibliotecas `sklearn` para cálculo das métricas, e a biblioteca `mlxtend` para plotagem da matriz de confusão

Antes de executar o arquivo `metrics.py`, atente-se as configurações do arquivo:

- Insira as credenciais do seu banco de dados
- Altere o modelo e estratégia de prompt calculada na linha 20 conforme desejado

Execute o arquivo `metrics.py`:
```bash
  python metrics.py
```