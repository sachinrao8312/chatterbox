
import sys
import torch
import os

# Add src to path just like the app might need (though package structure suggests it's installed or in path)
sys.path.append(os.path.join(os.getcwd(), "src"))

print(f"CUDA Available? {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)}")

try:
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    print("Import successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Target Device: {DEVICE}")

try:
    print("Attempting to load model...")
    model = ChatterboxTurboTTS.from_pretrained(DEVICE)
    print("Model loaded.")
    
    print(f"T3 Device: {next(model.t3.parameters()).device}")
    print(f"S3Gen Device: {next(model.s3gen.parameters()).device}")
    
    if str(next(model.t3.parameters()).device).startswith("cuda"):
        print("✅ Model is on GPU!")
    else:
        print("❌ Model is on CPU/Other!")
        
except Exception as e:
    print(f"Failed during loading: {e}")
    import traceback
    traceback.print_exc()

