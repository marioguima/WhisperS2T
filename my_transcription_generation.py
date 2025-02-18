import whisper_s2t
from whisper_s2t.backends.ctranslate2.model import BEST_ASR_CONFIG
import gc
import torch
import argparse


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files.")
    parser.add_argument("files", nargs="+", type=str,
                        help="List of audio files to transcribe.")
    parser.add_argument("--save_dir", type=str, default="./save_dir",
                        help="Directory to save the output files.")
    args = parser.parse_args()

    with torch.cuda.device(0):
        model_kwargs = {
            # Note int8 is only supported for CTranslate2 backend, for others only float16 is supported for lower precision.
            'compute_type': 'int8',
            'asr_options': {'word_timestamps': True}
        }

        model = whisper_s2t.load_model(
            model_identifier="large-v2", backend='CTranslate2', **model_kwargs)

        files = args.files
        lang_codes = ['pt']
        tasks = ['transcribe']
        initial_prompts = [None]

        out = model.transcribe_with_vad(files,
                                        lang_codes=lang_codes,  # pass lang_codes for each file
                                        tasks=tasks,  # pass transcribe/translate
                                        # to do prompting (currently only supported for CTranslate2 backend)
                                        initial_prompts=initial_prompts,
                                        batch_size=16)

        whisper_s2t.write_outputs(
            out, format='srt', ip_files=files, save_dir=args.save_dir)  # Save outputs
        # whisper_s2t.write_outputs(
        #     out, format='vtt', ip_files=files, save_dir=args.save_dir)  # Save outputs
        whisper_s2t.write_outputs(
            out, format='json', ip_files=files, save_dir=args.save_dir)  # Save outputs
        # whisper_s2t.write_outputs(
        #     out, format='tsv', ip_files=files, save_dir=args.save_dir)  # Save outputs

        print(out[0][0])  # Print first utterance for first file

    gc.collect()
    torch.cuda.empty_cache()
    del model


if __name__ == "__main__":
    main()
