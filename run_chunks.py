#!/usr/bin/env python3
import json
import subprocess
import argparse
import os
import sys

DEFAULT_CHUNKS = "/content/F5-TTS-Vietnamese/chunks.json"
DEFAULT_TEMPLATES_FILE = "templates.json"

# Built-in templates (will be overridden by templates.json if present)
BUILTIN_TEMPLATES = {
    "mien_nam": {
        "ref_audio": "/content/F5-TTS-Vietnamese/mien_nam.wav",
        "ref_text": "tâm tỉnh dậy trong dinh thự, nhìn xuống ao tôm mênh mông. nhưng giàu sang không mua được mạng sống."
    },
    "lieubachhop": {
        "ref_audio": "/content/F5-TTS-Vietnamese/0119.WAV",
        "ref_text": "chỉ cho mọi người một cách nói yêu mà không cần dùng chữ yêu, ừ thì tôi lỡ bước, lỡ bước vào mắt xanh"
    },
    "nhiii": {
        "ref_audio": "/content/F5-TTS-Vietnamese/0124.WAV",
        "ref_text": "và một muỗng canh tương ớt là 20 gam tương ớt, nấu mắm nêm mình nhớ cho thêm tương ớt vào, để cho vừa tạo độ sánh mà cái mắm nêm mình [...]"
    }
}

def load_templates(path):
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # accept either dict or list-of-objects; normalize to dict
            if isinstance(data, dict):
                return data
            elif isinstance(data, list):
                # list of {"name": "...", "ref_audio": "...", "ref_text": "..."}
                out = {}
                for item in data:
                    name = item.get("name")
                    if not name:
                        continue
                    out[name] = {"ref_audio": item.get("ref_audio", ""), "ref_text": item.get("ref_text", "")}
                return out
            else:
                print(f"Unrecognized templates.json format, using builtin templates.", file=sys.stderr)
        except Exception as e:
            print(f"Failed to load templates from {path}: {e}", file=sys.stderr)
    return BUILTIN_TEMPLATES

def main():
    p = argparse.ArgumentParser(description="Run TTS inference on chunks with selectable voice/text templates.")
    p.add_argument("--chunks-file", default=DEFAULT_CHUNKS, help="Path to chunks.json")
    p.add_argument("--templates-file", default=DEFAULT_TEMPLATES_FILE, help="Path to templates.json (optional)")
    p.add_argument("--template", help="Name of template to use (from templates.json or builtin)")
    p.add_argument("--list-templates", action="store_true", help="List available templates and exit")
    p.add_argument("--output-prefix", default="result_", help="Prefix for output files (default: result_)")
    p.add_argument("--model", default="F5TTS_Base", help="Model name")
    p.add_argument("--vocoder", default="vocos", help="Vocoder name")
    p.add_argument("--vocab-file", default="F5-TTS-Vietnamese-ViVoice/vocab.txt", help="Vocab file")
    p.add_argument("--ckpt-file", default="F5-TTS-Vietnamese-ViVoice/model_last.pt", help="Checkpoint file")
    p.add_argument("--speed", default="1", help="Speed multiplier")
    p.add_argument("--continue-on-error", action="store_true", help="Continue to next chunk if a command fails")
    args = p.parse_args()

    templates = load_templates(args.templates_file)

    if args.list_templates:
        print("Available templates:")
        for name, val in templates.items():
            print(f"- {name}: ref_audio={val.get('ref_audio')}, ref_text={val.get('ref_text')!r}")
        return

    if not args.template:
        print("No template selected. Use --template NAME or --list-templates to see options.", file=sys.stderr)
        sys.exit(1)

    if args.template not in templates:
        print(f"Template '{args.template}' not found. Use --list-templates to see available templates.", file=sys.stderr)
        sys.exit(1)

    template = templates[args.template]
    ref_audio = template.get("ref_audio")
    ref_text = template.get("ref_text")

    # Load chunks
    if not os.path.isfile(args.chunks_file):
        print(f"Chunks file not found: {args.chunks_file}", file=sys.stderr)
        sys.exit(1)

    with open(args.chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Common CLI options (without ref_audio/ref_text which come from template)
    base_cmd = [
        "f5-tts_infer-cli",
        "--model", args.model,
        "--speed", args.speed,
        "--vocoder_name", args.vocoder,
        "--vocab_file", args.vocab_file,
        "--ckpt_file", args.ckpt_file
    ]

    # Append template-specific options
    if ref_audio:
        base_cmd += ["--ref_audio", ref_audio]
    if ref_text:
        base_cmd += ["--ref_text", ref_text]

    for chunk in chunks:
        chunk_id = chunk.get("id")
        script = chunk.get("script", "")
        output_file = f"{args.output_prefix}{chunk_id}.wav"

        cmd = base_cmd + ["--gen_text", script, "-w", output_file]

        print(f"Running chunk {chunk_id} -> {output_file}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Chunk {chunk_id} failed: {e}", file=sys.stderr)
            if not args.continue_on_error:
                raise
            else:
                continue

if __name__ == "__main__":
    main()