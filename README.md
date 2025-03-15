# F5-TTS-Vietnamese
Fine-tuning pipline for training a Vietnamese speech synthesis model using the F5-TTS architecture.

## Installation

### Create a separate environment if needed

```bash
# Create a python 3.10 conda env (you could also use virtualenv)
conda create -n f5-tts python=3.10
conda activate f5-tts
```

### Install PyTorch

> ```bash
> # Install pytorch with your CUDA version, e.g.
> pip install torch==2.4.0+cu124 torchaudio==2.4.0+cu124 --extra-index-url https://download.pytorch.org/whl/cu124
> ```

### Install f5-tts module:

> ```bash
> git clone https://github.com/SWivid/F5-TTS.git
> cd F5-TTS
> # git submodule update --init --recursive  # (optional, if need > bigvgan)
> pip install -e .
> ```

### Install sox, ffmpeg

> ```bash
> sudo apt-get update
> sudo apt-get install sox ffmpeg
> ```

## Fine-tuning pipline

Steps:

- Prepare audio_name data and corresponding text
- Add vocabulary from your dataset that is not present in the pretrained model's vocabulary
- Expand the pretrained model's embedding to support the new vocabulary set
- Perform fine-tuning

```bash
bash fine-tuning.sh
```