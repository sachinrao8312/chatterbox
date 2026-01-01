
import sys
import torch
import os


log_file = "check_gpu_log.txt"
def log(msg):
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

if os.path.exists(log_file):
    os.remove(log_file)

log("="*40)
log("     GPU DIAGNOSTIC TOOL")
log("="*40)

log(f"Python Directory: {sys.executable}")
log(f"Python Version: {sys.version}")
log(f"Torch Version: {torch.__version__}")
log("-" * 20)

cuda_avail = torch.cuda.is_available()
log(f"CUDA Available: {cuda_avail}")

if cuda_avail:
    log(f"CUDA Version: {torch.version.cuda}")
    log(f"CuDNN Version: {torch.backends.cudnn.version()}")
    log(f"Device Count: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        log(f"  Device {i}: {torch.cuda.get_device_name(i)}")
        try:
            p = torch.cuda.get_device_properties(i)
            log(f"    Memory: {p.total_memory / 1024**3:.2f} GB")
            log(f"    Capability: {p.major}.{p.minor}")
        except Exception as e:
            log(f"    Error getting properties: {e}")
            
    log("-" * 20)
    log("Testing Tensor Allocation on CUDA...")
    try:
        x = torch.rand(1000, 1000).to("cuda")
        log("  ✅ Allocation successful!")
        log(f"  Tensor device: {x.device}")
        del x
        torch.cuda.empty_cache()
    except Exception as e:
        log(f"  ❌ Allocation FAILED: {e}")

else:
    log("No CUDA devices found.")
    log("Possibilities:")
    log("  1. No NVIDIA GPU installed.")
    log("  2. Incorrect drivers installed.")
    log("  3. PyTorch installed without CUDA support (CPU-only build).")

log("="*40)

