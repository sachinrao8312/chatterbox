# Changelog - Chatterbox TTS (RTX 5060 Ti Optimized)

All notable changes to this **RTX 5060 Ti optimized fork** of Chatterbox TTS will be documented in this file.

---

## [Unreleased] - 2026-01-01

### 🚀 CUDA Enforcement & GPU Optimization

This update ensures that **all TTS models use CUDA cores (GPU) instead of CPU/memory** for maximum performance.

#### Changes Made

##### Core Fixes
- **Fixed missing `import logging`** in `src/chatterbox/models/s3gen/utils/mask.py`
  - This was causing a `NameError` during speech token processing, which then corrupted the CUDA context

##### GPU Diagnostics Added (All Apps)
Enhanced GPU monitoring and enforcement in all Gradio applications:
- `multilingual_app.py` - Multilingual TTS
- `gradio_tts_app.py` - Standard TTS
- `gradio_tts_turbo_app.py` - Turbo TTS
- `gradio_vc_app.py` - Voice Conversion

##### New Features

1. **Pre-Generation Diagnostics**
   ```
   ============================================================
   🎯 CUDA CORES USAGE CHECK
   ============================================================
   CUDA Available: True
   ✅ GPU Device: NVIDIA GeForce RTX 5060 Ti
      CUDA Version: 12.8
      Pre-Gen Memory Allocated: 3500.00 MB
      Model Device: cuda
      T3 Model Device: cuda:0
      S3Gen Model Device: cuda:0
      VoiceEncoder Device: cuda:0
   ============================================================
   ```

2. **GPU Kernel Timing**
   - Accurate measurement of GPU execution time using CUDA events
   - Shows exact time spent on CUDA cores during generation

3. **Post-Generation Metrics**
   ```
   ============================================================
   🚀 CUDA GENERATION COMPLETE
   ============================================================
      GPU Kernel Time: 2500.00 ms
      Post-Gen Memory Allocated: 3800.00 MB
      Peak Memory Used: 4200.00 MB
   ============================================================
   ```

4. **Error Resilience**
   - All CUDA synchronize calls wrapped in try-except blocks
   - Prevents app crashes when CUDA enters error state
   - Automatic recovery using `torch.cuda.empty_cache()`

5. **Model Component Verification**
   - Confirms T3 (text-to-tokens), S3Gen (speech generation), and VoiceEncoder are all on GPU
   - Warns if any component is unexpectedly on CPU

##### Desktop App Updates
- Added `voice_conversion` to CLI mode options in `desktop_app.py`
- Can now launch directly with: `python desktop_app.py voice_conversion`

#### Files Modified

| File | Description |
|------|-------------|
| `src/chatterbox/models/s3gen/utils/mask.py` | Added missing `import logging` |
| `multilingual_app.py` | Full CUDA enforcement + error handling |
| `gradio_tts_app.py` | Full CUDA enforcement + error handling |
| `gradio_tts_turbo_app.py` | Full CUDA enforcement + error handling |
| `gradio_vc_app.py` | Full CUDA enforcement + error handling |
| `desktop_app.py` | Added `voice_conversion` CLI mode |

#### Technical Details

The CUDA enforcement works by:
1. Calling `torch.cuda.synchronize()` before and after generation to ensure accurate memory readings
2. Using `torch.cuda.Event` with `enable_timing=True` to measure GPU kernel execution time
3. Checking device placement of all model components (T3, S3Gen, VoiceEncoder)
4. Wrapping all CUDA operations in try-except to handle transient GPU errors gracefully

#### Troubleshooting

If you see "❌ CUDA IS NOT AVAILABLE!" in the logs:
1. Ensure you have an NVIDIA GPU
2. Install PyTorch with CUDA support: `pip install torch --index-url https://download.pytorch.org/whl/cu124`
3. Verify CUDA installation: `nvidia-smi`

If you see "⚠️ CUDA diagnostic error":
1. Restart the application (CUDA context may be corrupted)
2. Check if another process is using too much GPU memory
3. Try `torch.cuda.empty_cache()` in Python to clear memory

---

## Previous Versions

### v0.1.6 - Initial Desktop App
- Introduced unified Dashboard with mode switching
- Added Settings panel for output directory
- Real-time progress bars
- GPU acceleration detection
