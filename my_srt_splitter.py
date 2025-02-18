import json
import argparse
import os
from datetime import datetime, timedelta


def to_seconds(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M:%S,%f').time()
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond/1000000


def format_time(seconds):
    time_obj = datetime.min + timedelta(seconds=seconds)
    return time_obj.strftime('%H:%M:%S,%f')[:-3]


def get_word_timestamps_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        j = json.load(f)
        word_timestamps = []
        if isinstance(j, list) and len(j) > 0:
            for obj in j:
                if "word_timestamps" in obj:
                    for word_obj in obj["word_timestamps"]:
                        word_timestamps.append(word_obj)
        else:
            if "word_timestamps" in j:
                for word_obj in j["word_timestamps"]:
                    word_timestamps.append(word_obj)

        return word_timestamps


def divide_subtitles(word_timestamps, max_words):
    new_subtitles = []
    current_sub = {
        'start_time': 0,
        'end_time': 0,
        'words': []
    }
    words_counter = 0

    for word_obj in word_timestamps:
        if words_counter < max_words:
            if words_counter == 0:
                current_sub["start_time"] = word_obj["start"]
            current_sub["words"].append(word_obj["word"])
            current_sub["end_time"] = word_obj["end"]
            words_counter += 1
        if words_counter == max_words or word_obj == word_timestamps[-1]:
            new_subtitles.append(current_sub)
            current_sub = {
                'start_time': 0,
                'end_time': 0,
                'words': [],
            }
            words_counter = 0

    return new_subtitles


def write_srt(new_subtitles, output_srt_path):
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        for i, sub in enumerate(new_subtitles, 1):
            f.write(f"{i}\n")
            f.write(
                f"{format_time(sub['start_time'])} --> {format_time(sub['end_time'])}\n")
            f.write(f"{' '.join(sub['words'])}\n\n")


def write_srt_words(word_timestamps, output_srt_path):
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        for i, word_obj in enumerate(word_timestamps, 1):
            f.write(f"{i}\n")
            f.write(
                f"{format_time(word_obj['start'])} --> {format_time(word_obj['end'])}\n")
            f.write(f"{word_obj['word']}\n\n")


def main():
    parser = argparse.ArgumentParser(
        description='Divide SRT file based on JSON word timestamps.')
    parser.add_argument('json_path', type=str, help='Path to the JSON file.')
    parser.add_argument('srt_path', type=str,
                        help='Path to the output SRT file.')
    parser.add_argument('max_words', type=int,
                        help='Maximum number of words per line.')

    args = parser.parse_args()

    json_path = args.json_path
    srt_path = args.srt_path
    max_words = args.max_words

    # Passo 1: Ler o arquivo JSON
    word_timestamps = get_word_timestamps_from_json(json_path)

    # Passo 2: Dividir as legendas usando o json (até max_words)
    new_subtitles = divide_subtitles(word_timestamps, max_words)

    # Passo 3: Escrever o arquivo SRT (até max_words)
    write_srt(new_subtitles, srt_path)

    # Passo 4: Escrever o arquivo SRT (uma palavra por linha)
    base_name = os.path.splitext(srt_path)[0]
    output_words_srt_path = f"{base_name}_words.srt"
    write_srt_words(word_timestamps, output_words_srt_path)

    print(f"Successfully created: {srt_path} and {output_words_srt_path}")


if __name__ == "__main__":
    main()
