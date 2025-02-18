# Como usar o gerador de legenda automático

Execute esse comando para gerar a legenda

```bash
python my_transcription_generation.py "file1.mp3" "file2.mp3" --save_dir "output_directory"
```

Replace `"file1.mp3"`, `"file2.mp3"` with the actual paths to your audio files, and `"output_directory"` with the desired output directory.

Exemplo de utilização:

```bash
python my_transcription_generation.py "E:\Mário Guimarães\products\ebook-lucrativo\pro\ads\criativos\video\v1\audios\V1-1-cut-aprimorado-v2.wav" --save_dir "E:\Mário Guimarães\products\ebook-lucrativo\pro\ads\criativos\video\v1\audios\legendas"
```

Depois de gerar a transcrição será gerado dois arquivos na pasta destino informada, um com .json outro com .srt

O .json tem a transcrição palavra por palavra, o .srt tem a transcrição do texto por blocos

Para gerar um arquivo de legenda palavra por palavra com a estrutura .srt, para importar no premiere ou capcut, por exemplo, basta executar o conversor da seguinte maneira

```bash
python my_srt_splitter.py 'E:\Mário Guimarães\products\ebook-lucrativo\pro\ads\criativos\video\v1\audios\legendas\0_V1-1-cut-aprimorado-v2.json' 'E:\Mário Guimarães\products\ebook-lucrativo\pro\ads\criativos\video\v1\audios\legendas\V1-1-cut-aprimorado-v2.srt' 4
```

```bash
python my_files_to_text.py --path "D:\courses\Leandro Ladeira\Stories 10x" --all_files mp4 --output_txt --output_srt --output_json
```

```bash
python my_audio_to_text.py "E:\Mário Guimarães\products\criacao-produto-perpetuo\0f1be034444e4fc98fd0fcb2441f673d-1739619871707.mp4" --save_dir "E:\Mário Guimarães\products\criacao-produto-perpetuo"
```

