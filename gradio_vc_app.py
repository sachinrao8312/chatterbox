import torch
import gradio as gr
from chatterbox.vc import ChatterboxVC



print("="*50)
if torch.cuda.is_available():
    print(f"✅ CUDA Available! Found {torch.cuda.device_count()} device(s).")
    print(f"   Current Device: {torch.cuda.get_device_name(0)}")
    print(f"   CUDA Version: {torch.version.cuda}")
    DEVICE = "cuda"
else:
    print("⚠️ CUDA NOT Available. Using CPU (High RAM usage expected).")
    DEVICE = "cpu"
print("="*50)


model = ChatterboxVC.from_pretrained(DEVICE)

def generate(audio, target_voice_path):
    # --- GPU ENFORCEMENT & DIAGNOSTICS ---
    print(f"\n{'='*60}")
    print(f"🎯 CUDA CORES USAGE CHECK (Voice Conversion)")
    print(f"{'='*60}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    start_event = None
    end_event = None
    
    if torch.cuda.is_available():
        try:
            torch.cuda.synchronize()
            print(f"✅ GPU Device: {torch.cuda.get_device_name(0)}")
            print(f"   Pre-Gen Memory Allocated: {torch.cuda.memory_allocated()/1024**2:.2f} MB")
            print(f"   Model Device: {getattr(model, 'device', 'unknown')}")
        except Exception as e:
            print(f"⚠️ CUDA diagnostic error: {e}")
            try:
                torch.cuda.empty_cache()
            except:
                pass
    else:
        print("❌ CUDA IS NOT AVAILABLE! Generation will use CPU (very slow).")
    print(f"{'='*60}")
    
    # GPU timing
    if torch.cuda.is_available():
        try:
            start_event = torch.cuda.Event(enable_timing=True)
            end_event = torch.cuda.Event(enable_timing=True)
            start_event.record()
        except Exception as e:
            print(f"   [GPU] Warning: Could not create CUDA events: {e}")
    # -----------------
    
    wav = model.generate(
        audio, target_voice_path=target_voice_path,
    )
    
    # --- GPU POST-GENERATION DIAGNOSTICS ---
    if torch.cuda.is_available():
        try:
            if end_event is not None:
                end_event.record()
                torch.cuda.synchronize()
                gpu_time_ms = start_event.elapsed_time(end_event)
                print(f"\n{'='*60}")
                print(f"🚀 CUDA GENERATION COMPLETE (Voice Conversion)")
                print(f"{'='*60}")
                print(f"   GPU Kernel Time: {gpu_time_ms:.2f} ms")
                print(f"   Post-Gen Memory: {torch.cuda.memory_allocated()/1024**2:.2f} MB")
                print(f"   Peak Memory: {torch.cuda.max_memory_allocated()/1024**2:.2f} MB")
                print(f"{'='*60}\n")
        except Exception as e:
            print(f"   [GPU] Post-generation diagnostic error: {e}")
            try:
                torch.cuda.empty_cache()
            except:
                pass
    # -----------------
    
    return model.sr, wav.squeeze(0).numpy()


demo = gr.Interface(
    generate,
    [
        gr.Audio(sources=["upload", "microphone"], type="filepath", label="Input audio file"),
        gr.Audio(sources=["upload", "microphone"], type="filepath", label="Target voice audio file (if none, the default voice is used)", value=None),
    ],
    "audio",
)

if __name__ == "__main__":
    demo.launch()
