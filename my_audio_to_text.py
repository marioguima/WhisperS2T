import whisper_s2t
from whisper_s2t.backends.ctranslate2.model import BEST_ASR_CONFIG
import gc
import torch
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files.")
    parser.add_argument("files", nargs="+", type=str,
                        help="List of audio files to transcribe.")
    parser.add_argument("--save_dir", type=str, default="./save_dir",
                        help="Directory to save the output files.")
    parser.add_argument("--output_txt", action="store_true",
                        help="Save a .txt file with only the transcription.")
    parser.add_argument("--lang_code", type=str, default="pt",
                        help="Language code for transcription (default: pt).")

    args = parser.parse_args()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model_kwargs = {
        'compute_type': 'int8',
        'asr_options': {'word_timestamps': False}  # Desativa timestamps
    }

    model = whisper_s2t.load_model(
        model_identifier="large-v2", backend='CTranslate2', **model_kwargs)

    files = args.files
    lang_codes = [args.lang_code]  # Usa o idioma passado como argumento
    tasks = ['transcribe']
    initial_prompts = [None]

    out = model.transcribe_with_vad(
        files, lang_codes=lang_codes, tasks=tasks, initial_prompts=initial_prompts, batch_size=16)

    whisper_s2t.write_outputs(
        out, format='srt', ip_files=files, save_dir=args.save_dir)

    if args.output_txt:
        for i, file in enumerate(files):
            try:
                # Corrigido para melhor manipulação
                full_text = " ".join(segment['text'] for segment in out[i])

                base_name = os.path.splitext(os.path.basename(file))[0]
                output_file = os.path.join(args.save_dir, f"{base_name}.txt")

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(full_text.strip())

                print(f"Transcrição salva em: {output_file}")
            except Exception as e:
                print(f"Erro ao processar/salvar o arquivo {file}: {e}")
                import traceback
                traceback.print_exc()

    # Exibe o primeiro segmento do primeiro arquivo processado
    if out and out[0]:
        print(out[0][0]['text'])

    # Libera memória
    del model
    gc.collect()
    torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
