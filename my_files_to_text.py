import whisper_s2t
from whisper_s2t.backends.ctranslate2.model import BEST_ASR_CONFIG
import gc
import torch
import argparse
import os
import glob
import time


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files.")
    parser.add_argument("--path", type=str, required=True,
                        help="Path to the directory containing audio files.")
    parser.add_argument("--all_files", type=str, required=True,
                        help="File type to transcribe (e.g., mp4, wav).")
    parser.add_argument("--save_dir", type=str,
                        help="Directory to save the output files. Defaults to the input path if not specified.")
    parser.add_argument("--output_txt", action="store_true",
                        help="Save a .txt file with only the transcription.")
    parser.add_argument("--output_srt", action="store_true",
                        help="Save a .srt file with the transcription.")
    parser.add_argument("--output_json", action="store_true",
                        help="Save a .json file with the transcription.")
    args = parser.parse_args()

    if args.save_dir:
        output_dir = args.save_dir
    else:
        output_dir = args.path

    if not os.path.isdir(args.path):
        print(
            f"Erro: O diretório especificado em --path não existe: {args.path}")
        return

    if output_dir != args.path and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Diretório de saída criado: {output_dir}")
        except OSError as e:
            print(f"Erro ao criar o diretório de saída: {e}")
            return

    search_pattern = os.path.join(args.path, f"*.{args.all_files}")
    files = glob.glob(search_pattern)

    if not files:
        print(f"Nenhum arquivo .{args.all_files} encontrado em {args.path}")
        return

    with torch.cuda.device(0):
        model_kwargs = {
            'compute_type': 'int8',
            'asr_options': {'word_timestamps': False}
        }

        model = whisper_s2t.load_model(
            model_identifier="large-v2", backend='CTranslate2', **model_kwargs)

        lang_codes = ['pt']
        tasks = ['transcribe']
        initial_prompts = [None]

        total_start_time = time.time()  # Tempo inicial (total)
        all_files_time = {}  # Dicionário para armazenar tempos por arquivo

        for i, file in enumerate(files):
            try:
                file_start_time = time.time()  # Tempo inicial (arquivo individual)
                out = model.transcribe_with_vad([file],  # Passa apenas o arquivo atual
                                                lang_codes=lang_codes,
                                                tasks=tasks,
                                                initial_prompts=initial_prompts,
                                                batch_size=16)
                file_end_time = time.time()  # Tempo final (arquivo individual)
                file_elapsed_time = file_end_time - file_start_time
                # Armazena o tempo do arquivo
                all_files_time[file] = file_elapsed_time
                print(
                    f"Tempo de transcrição ({os.path.basename(file)}): {file_elapsed_time:.2f} segundos")

                full_text = ""
                # Acessa o primeiro (e único) elemento de 'out'
                for segment in out[0]:
                    full_text += segment['text'] + " "
                full_text = full_text.strip()

                base_name = os.path.splitext(os.path.basename(file))[0]

                if args.output_txt:
                    output_file_txt = os.path.join(
                        output_dir, f"{base_name}.txt")
                    with open(output_file_txt, "w", encoding="utf-8") as f:
                        f.write(full_text)
                    print(f"Transcrição (txt) salva em: {output_file_txt}")

                if args.output_srt:
                    output_file_srt = os.path.join(
                        output_dir, f"{base_name}.srt")
                    # Passa o out completo, pois é um único arquivo
                    whisper_s2t.write_outputs(
                        out, format='srt', ip_files=[file], save_dir=output_dir)
                    print(f"Transcrição (srt) salva em: {output_file_srt}")

                if args.output_json:
                    output_file_json = os.path.join(
                        output_dir, f"{base_name}.json")
                    # Passa o out completo, pois é um único arquivo
                    whisper_s2t.write_outputs(
                        out, format='json', ip_files=[file], save_dir=output_dir)
                    print(f"Transcrição (json) salva em: {output_file_json}")

            except Exception as e:
                print(f"Erro ao processar/salvar o arquivo {file}: {e}")
                import traceback
                traceback.print_exc()

        total_end_time = time.time()  # Tempo final (total)
        total_elapsed_time = total_end_time - total_start_time

        print("\n--- Resumo dos Tempos ---")
        for file, elapsed_time in all_files_time.items():
            print(
                f"Arquivo: {os.path.basename(file)}, Tempo: {elapsed_time:.2f} segundos")
        print(f"Tempo total de transcrição: {total_elapsed_time:.2f} segundos")

        # if out:  # Verifica apenas se out não está vazio
        #     print(out[0]['text'])

    gc.collect()
    torch.cuda.empty_cache()
    del model


if __name__ == "__main__":
    main()
