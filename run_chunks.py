import json
import subprocess

# Load JSON file
with open("/content/F5-TTS-Vietnamese/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Common CLI options - Updated for Vietnamese
base_cmd = [
    "f5-tts_infer-cli",
    "--model", "F5TTS_Base",
    "--ref_audio", "/content/F5-TTS-Vietnamese/mien_nam.wav",
    "--ref_text", "tâm tỉnh dậy trong dinh thự, nhìn xuống ao tôm mênh mông. nhưng giàu sang không mua được mạng sống.",
    "--speed", "1",
    "--vocoder_name", "vocos",
    "--vocab_file", "F5-TTS-Vietnamese-ViVoice/vocab.txt",
    "--ckpt_file", "F5-TTS-Vietnamese-ViVoice/model_last.pt"
]

# Run for each chunk
for chunk in chunks:
    chunk_id = chunk["id"]
    script = chunk["script"]
    output_file = f"result_{chunk_id}.wav"

    cmd = base_cmd + ["--gen_text", script, "-w", output_file]

    print(f"Running chunk {chunk_id} -> {output_file}")
    subprocess.run(cmd, check=True)
