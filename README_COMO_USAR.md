# Manual de Uso - Ferramentas de Transcrição

Este manual descreve como utilizar os scripts Python para transcrever arquivos de áudio/vídeo e manipular os arquivos de legenda gerados.

## Pré-requisitos

Certifique-se de ter o Python instalado e as bibliotecas necessárias, incluindo `whisper-s2t`. Você pode instalar as dependências executando:

```bash
pip install -r requirements.txt
```

(Assumindo que `requirements.txt` contém as dependências necessárias, como `whisper-s2t` e `torch`).

## 1. Geração de Transcrição com Word Timestamps (`my_transcription_generation.py`)

Este script é ideal para gerar a transcrição inicial de um ou mais arquivos de áudio/vídeo, incluindo timestamps para cada palavra. O arquivo `.json` gerado por este script é necessário para utilizar o `my_srt_splitter.py`.

**Uso:**

```bash
python my_transcription_generation.py <arquivos> [--save_dir <diretorio_saida>]
```

*   `<arquivos>`: Lista de caminhos para os arquivos de áudio/vídeo a serem transcritos (separados por espaço). **Obrigatório**.
*   `--save_dir <diretorio_saida>`: Diretório onde os arquivos de saída (.srt e .json) serão salvos. Se não especificado, o padrão é `./save_dir`. **Opcional**.

**Saída:**

Este script gera dois arquivos para cada arquivo de entrada no diretório especificado por `--save_dir`:
*   Um arquivo `.srt` com a transcrição dividida em blocos.
*   Um arquivo `.json` contendo a transcrição detalhada, incluindo timestamps para cada palavra. Este arquivo é crucial para o script `my_srt_splitter.py`.

**Exemplo:**

```bash
python my_transcription_generation.py "audio1.wav" "video2.mp4" --save_dir "./legendas_geradas"
```

## 2. Transcrição Simples de Áudio (`my_audio_to_text.py`)

Este script transcreve um ou mais arquivos de áudio/vídeo, gerando um arquivo `.srt` por padrão. Ele também pode gerar um arquivo `.txt` contendo apenas o texto da transcrição. Por padrão, ele não gera timestamps por palavra, tornando-o mais rápido para transcrições simples.

**Uso:**

```bash
python my_audio_to_text.py <arquivos> [--save_dir <diretorio_saida>] [--output_txt] [--lang_code <codigo_idioma>]
```

*   `<arquivos>`: Lista de caminhos para os arquivos de áudio/vídeo a serem transcritos (separados por espaço). **Obrigatório**.
*   `--save_dir <diretorio_saida>`: Diretório onde os arquivos de saída (.srt e opcionalmente .txt) serão salvos. Se não especificado, o padrão é `./save_dir`. **Opcional**.
*   `--output_txt`: Se presente, salva um arquivo `.txt` com apenas o texto da transcrição. **Opcional**.
*   `--lang_code <codigo_idioma>`: Código do idioma para a transcrição (ex: "en" para inglês, "pt" para português). O padrão é "pt". **Opcional**.

**Saída:**

Este script gera um arquivo `.srt` para cada arquivo de entrada no diretório especificado por `--save_dir`. Se a flag `--output_txt` for usada, também gera um arquivo `.txt`.

**Exemplo:**

```bash
python my_audio_to_text.py "meu_audio.mp3" --save_dir "./transcricoes" --output_txt --lang_code "en"
```

## 3. Transcrição em Lote de Arquivos em um Diretório (`my_files_to_text.py`)

Este script transcreve todos os arquivos de um tipo específico (por exemplo, todos os `.mp4` ou `.wav`) dentro de um diretório. Ele permite escolher quais formatos de saída (.txt, .srt, .json) serão gerados.

**Uso:**

```bash
python my_files_to_text.py --path <diretorio_entrada> --all_files <tipo_arquivo> [--save_dir <diretorio_saida>] [--output_txt] [--output_srt] [--output_json]
```

*   `--path <diretorio_entrada>`: Caminho para o diretório contendo os arquivos a serem transcritos. **Obrigatório**.
*   `--all_files <tipo_arquivo>`: Extensão dos arquivos a serem transcritos (ex: `mp4`, `wav`). **Obrigatório**.
*   `--save_dir <diretorio_saida>`: Diretório onde os arquivos de saída serão salvos. Se não especificado, os arquivos serão salvos no diretório de entrada (`--path`). **Opcional**.
*   `--output_txt`: Se presente, salva arquivos `.txt`. **Opcional**.
*   `--output_srt`: Se presente, salva arquivos `.srt`. **Opcional**.
*   `--output_json`: Se presente, salva arquivos `.json`. **Opcional**.

**Saída:**

Para cada arquivo encontrado no diretório de entrada com a extensão especificada, este script gera os formatos de saída (.txt, .srt, .json) conforme as flags `--output_txt`, `--output_srt`, `--output_json` utilizadas. Os arquivos são salvos no diretório especificado por `--save_dir` ou no diretório de entrada se `--save_dir` não for usado. O script também reporta o tempo de processamento para cada arquivo e o tempo total.

**Exemplo:**

```bash
python my_files_to_text.py --path "D:/videos_para_transcrever" --all_files mp4 --output_srt --output_json --save_dir "./saida_lote"
```

## 4. Divisão de Legendas SRT Baseada em JSON (`my_srt_splitter.py`)

Este script utiliza o arquivo `.json` gerado por `my_transcription_generation.py` ou `my_files_to_text.py` (com `--output_json`) para criar novas versões do arquivo SRT. Ele pode gerar um SRT com um número máximo de palavras por linha e outro SRT com uma palavra por linha, útil para edição em softwares como Premiere ou CapCut.

**Uso:**

```bash
python my_srt_splitter.py <caminho_json> <caminho_srt_saida> <max_palavras>
```

*   `<caminho_json>`: Caminho para o arquivo `.json` gerado anteriormente (contendo word timestamps). **Obrigatório**.
*   `<caminho_srt_saida>`: Caminho e nome para o arquivo SRT de saída que terá no máximo `<max_palavras>` por linha. **Obrigatório**.
*   `<max_palavras>`: Número máximo de palavras permitidas por linha no arquivo SRT de saída principal. **Obrigatório**.

**Saída:**

Este script gera dois arquivos SRT:
*   Um arquivo no caminho especificado por `<caminho_srt_saida>`, com no máximo `<max_palavras>` por linha.
*   Um segundo arquivo no mesmo diretório do `<caminho_srt_saida>`, com o nome `{nome_base_srt}_words.srt`, onde cada linha contém apenas uma palavra.

**Exemplo:**

```bash
python my_srt_splitter.py "./legendas_geradas/audio1.json" "./legendas_finais/audio1_split.srt" 5
```

Este comando usará o `audio1.json` para criar `audio1_split.srt` (com no máximo 5 palavras por linha) e `audio1_split_words.srt` (com uma palavra por linha) dentro do diretório `./legendas_finais`.

## Fluxo de Trabalho Típico

1.  Use `my_transcription_generation.py` ou `my_files_to_text.py` (com `--output_json`) para transcrever seus arquivos e gerar os arquivos `.srt` e `.json`.
2.  Use `my_srt_splitter.py` com o arquivo `.json` gerado na etapa 1 e especifique o número máximo de palavras por linha desejado para obter arquivos SRT formatados para edição.
