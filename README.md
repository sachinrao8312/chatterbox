![Chatterbox Turbo Image](./Chatterbox-Turbo.jpg)


# Chatterbox TTS - RTX 5060 Ti Optimized 🚀

> **⚡ Fork optimized for NVIDIA RTX 5060 Ti with enhanced CUDA enforcement and GPU diagnostics**

[![Alt Text](https://img.shields.io/badge/listen-demo_samples-blue)](https://resemble-ai.github.io/chatterbox_turbo_demopage/)
[![Alt Text](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/ResembleAI/chatterbox-turbo-demo)
[![GPU](https://img.shields.io/badge/GPU-RTX%205060%20Ti-76B900?logo=nvidia&logoColor=white)](https://www.nvidia.com/)
[![CUDA](https://img.shields.io/badge/CUDA-12.8-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)

_Based on Chatterbox by <a href="https://resemble.ai" target="_blank"><img width="100" alt="resemble-logo-horizontal" src="https://github.com/user-attachments/assets/35cf756b-3506-4943-9c72-c05ddfa4e525" /></a>_

---

## 🎯 What's Special About This Fork?

This is a **performance-optimized fork** of Chatterbox TTS specifically tuned for the **NVIDIA GeForce RTX 5060 Ti** and similar Blackwell/Ada Lovelace architecture GPUs.

### Key Optimizations:
- ✅ **Forced CUDA Enforcement** - Ensures all model components run on GPU, not CPU
- ✅ **Real-time GPU Diagnostics** - Monitor VRAM usage, kernel execution time, and device placement
- ✅ **Error-Resilient CUDA Handling** - Graceful recovery from transient GPU errors
- ✅ **Memory-Optimized Loading** - Efficient model loading for 16GB VRAM cards
- ✅ **Desktop Dashboard App** - Native Windows app with mode switching and auto-save
- ✅ **Bug Fixes** - Patched missing imports and edge cases from upstream

### Performance on RTX 5060 Ti:
| Mode | Generation Time | VRAM Usage |
|------|----------------|------------|
| Turbo | ~1.5-2.5s | ~3.5 GB |
| Standard | ~3-5s | ~4.5 GB |
| Multilingual | ~4-6s | ~5 GB |
| Voice Conversion | ~2-4s | ~4 GB |

---

**Chatterbox** is a family of three state-of-the-art, open-source text-to-speech models by Resemble AI.

**Chatterbox-Turbo** is the most efficient model, built on a streamlined 350M parameter architecture. **Turbo** delivers high-quality speech with less compute and VRAM than previous models. The speech-token-to-mel decoder has been distilled, reducing generation from 10 steps to just **one**.

**Paralinguistic tags** are native to the Turbo model: `[cough]`, `[laugh]`, `[chuckle]`, and more.

<img width="1200" height="600" alt="Podonos Turbo Eval" src="https://storage.googleapis.com/chatterbox-demo-samples/turbo/podonos_turbo.png" />

### ⚡ Model Zoo

| Model | Size | Languages | Key Features | Best For | 🤗 | Examples |
|:------|:-----|:----------|:-------------|:---------|:---|:---------|
| **Chatterbox-Turbo** | **350M** | **English** | Paralinguistic Tags, Low VRAM | Voice agents, Production | [Demo](https://huggingface.co/spaces/ResembleAI/chatterbox-turbo-demo) | [Listen](https://resemble-ai.github.io/chatterbox_turbo_demopage/) |
| Chatterbox-Multilingual | 500M | 23+ | Zero-shot cloning, Multi-language | Global apps, Localization | [Demo](https://huggingface.co/spaces/ResembleAI/Chatterbox-Multilingual-TTS) | [Listen](https://resemble-ai.github.io/chatterbox_demopage/) |
| Chatterbox | 500M | English | CFG & Exaggeration tuning | Creative TTS controls | [Demo](https://huggingface.co/spaces/ResembleAI/Chatterbox) | [Listen](https://resemble-ai.github.io/chatterbox_demopage/) |

## Installation (RTX 5060 Ti Optimized)

### Prerequisites
- Python 3.11+
- NVIDIA RTX 5060 Ti (or compatible GPU with 16GB+ VRAM)
- CUDA 12.4+ and cuDNN

### Quick Install
```shell
# Clone this optimized fork
git clone https://github.com/sachinrao8312/chatterbox.git
cd chatterbox

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install PyTorch with CUDA 12.4 support (for RTX 5060 Ti)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Install Chatterbox
pip install -e .
```

### Verify GPU Setup
```shell
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

Expected output:
```
CUDA: True, Device: NVIDIA GeForce RTX 5060 Ti
```

## Usage

##### Chatterbox-Turbo

```python
import torchaudio as ta
import torch
from chatterbox.tts_turbo import ChatterboxTurboTTS

# Load the Turbo model
model = ChatterboxTurboTTS.from_pretrained(device="cuda")

# Generate with Paralinguistic Tags
text = "Hi there, Sarah here from MochaFone calling you back [chuckle], have you got one minute to chat about the billing issue?"

# Generate audio (requires a reference clip for voice cloning)
wav = model.generate(text, audio_prompt_path="your_10s_ref_clip.wav")

ta.save("test-turbo.wav", wav, model.sr)
```

##### Chatterbox and Chatterbox-Multilingual

```python

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

# English example
model = ChatterboxTTS.from_pretrained(device="cuda")

text = "Ezreal and Jinx teamed up with Ahri, Yasuo, and Teemo to take down the enemy's Nexus in an epic late-game pentakill."
wav = model.generate(text)
ta.save("test-english.wav", wav, model.sr)

# Multilingual examples
multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=device)

french_text = "Bonjour, comment ça va? Ceci est le modèle de synthèse vocale multilingue Chatterbox, il prend en charge 23 langues."
wav_french = multilingual_model.generate(spanish_text, language_id="fr")
ta.save("test-french.wav", wav_french, model.sr)

chinese_text = "你好，今天天气真不错，希望你有一个愉快的周末。"
wav_chinese = multilingual_model.generate(chinese_text, language_id="zh")
ta.save("test-chinese.wav", wav_chinese, model.sr)

# If you want to synthesize with a different voice, specify the audio prompt
AUDIO_PROMPT_PATH = "YOUR_FILE.wav"
wav = model.generate(text, audio_prompt_path=AUDIO_PROMPT_PATH)
ta.save("test-2.wav", wav, model.sr)
```
See `example_tts.py` and `example_vc.py` for more examples.

## Supported Languages 
Arabic (ar) • Danish (da) • German (de) • Greek (el) • English (en) • Spanish (es) • Finnish (fi) • French (fr) • Hebrew (he) • Hindi (hi) • Italian (it) • Japanese (ja) • Korean (ko) • Malay (ms) • Dutch (nl) • Norwegian (no) • Polish (pl) • Portuguese (pt) • Russian (ru) • Swedish (sv) • Swahili (sw) • Turkish (tr) • Chinese (zh)

## Original Chatterbox Tips
- **General Use (TTS and Voice Agents):**
  - Ensure that the reference clip matches the specified language tag. Otherwise, language transfer outputs may inherit the accent of the reference clip’s language. To mitigate this, set `cfg_weight` to `0`.
  - The default settings (`exaggeration=0.5`, `cfg_weight=0.5`) work well for most prompts across all languages.
  - If the reference speaker has a fast speaking style, lowering `cfg_weight` to around `0.3` can improve pacing.

- **Expressive or Dramatic Speech:**
  - Try lower `cfg_weight` values (e.g. `~0.3`) and increase `exaggeration` to around `0.7` or higher.
  - Higher `exaggeration` tends to speed up speech; reducing `cfg_weight` helps compensate with slower, more deliberate pacing.


## Built-in PerTh Watermarking for Responsible AI

Every audio file generated by Chatterbox includes [Resemble AI's Perth (Perceptual Threshold) Watermarker](https://github.com/resemble-ai/perth) - imperceptible neural watermarks that survive MP3 compression, audio editing, and common manipulations while maintaining nearly 100% detection accuracy.


## Watermark extraction

You can look for the watermark using the following script.

```python
import perth
import librosa

AUDIO_PATH = "YOUR_FILE.wav"

# Load the watermarked audio
watermarked_audio, sr = librosa.load(AUDIO_PATH, sr=None)

# Initialize watermarker (same as used for embedding)
watermarker = perth.PerthImplicitWatermarker()

# Extract watermark
watermark = watermarker.get_watermark(watermarked_audio, sample_rate=sr)
print(f"Extracted watermark: {watermark}")
# Output: 0.0 (no watermark) or 1.0 (watermarked)
```


## Desktop Application & New Features (v2 Update)

We have introduced a unified **Desktop Dashboard** to manage your Chatterbox experience easily.

### 🚀 How to Launch
- **Windows (Command Prompt):** Double-click `Launch_App.bat` or the desktop shortcut.
- **Windows (Git Bash/MinGW):** Run `./run.sh` to avoid path issues.
- **CLI Mode:** Launch directly with `python desktop_app.py turbo|standard|multilingual|voice_conversion`

### ✨ New Features
1.  **Unified Dashboard:** Switch between **Turbo**, **Standard**, **Multilingual**, and **Voice Conversion** modes instantly without restarting the app.
2.  **Settings & Auto-Save:** Click the **⚙️ Settings** icon to choose an output folder. All generated audio is automatically saved there with timestamps.
3.  **Real-time Progress:** Visual progress bars show loading, generation, and saving status.

### 🎮 GPU Acceleration & CUDA Enforcement

The app automatically detects and **forces CUDA (NVIDIA GPU) usage** for significantly faster performance:

- **Pre-generation diagnostics** confirm all model components (T3, S3Gen, VoiceEncoder) are on GPU
- **GPU kernel timing** measures exact CUDA execution time
- **Memory tracking** shows allocated, reserved, and peak GPU memory usage
- **Error resilience** prevents crashes if CUDA encounters transient errors

When you generate audio, you'll see detailed GPU stats in the console:
```
============================================================
🎯 CUDA CORES USAGE CHECK
============================================================
CUDA Available: True
✅ GPU Device: NVIDIA GeForce RTX 5060 Ti
   CUDA Version: 12.8
   Pre-Gen Memory Allocated: 3500.00 MB
   T3 Model Device: cuda:0
   S3Gen Model Device: cuda:0
============================================================

... (generation) ...

============================================================
🚀 CUDA GENERATION COMPLETE
============================================================
   GPU Kernel Time: 2500.00 ms
   Post-Gen Memory: 3800.00 MB
   Peak Memory Used: 4200.00 MB
============================================================
```

> 📋 See [CHANGELOG.md](./CHANGELOG.md) for full technical details on GPU optimizations.

### 🛠️ Troubleshooting
- **"❌ CUDA IS NOT AVAILABLE":** Install PyTorch with CUDA support: `pip install torch --index-url https://download.pytorch.org/whl/cu124`
- **High RAM Usage:** Ensure you are using the GPU-enabled version. If the console says "Using CPU", reinstall PyTorch with CUDA.
- **CUDA Errors:** Restart the app. CUDA context can become corrupted after certain errors.


## Official Discord

👋 Join us on [Discord](https://discord.gg/rJq9cRJBJ6) and let's build something awesome together!

## Acknowledgements
- [Cosyvoice](https://github.com/FunAudioLLM/CosyVoice)
- [Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
- [HiFT-GAN](https://github.com/yl4579/HiFTNet)
- [Llama 3](https://github.com/meta-llama/llama3)
- [S3Tokenizer](https://github.com/xingchensong/S3Tokenizer)

## Citation
If you find this model useful, please consider citing.
```
@misc{chatterboxtts2025,
  author       = {{Resemble AI}},
  title        = {{Chatterbox-TTS}},
  year         = {2025},
  howpublished = {\url{https://github.com/resemble-ai/chatterbox}},
  note         = {GitHub repository}
}
```
## Disclaimer
Don't use this model to do bad things. Prompts are sourced from freely available data on the internet.
