import torch
import sys
import os

log_file = "cuda_check_result.txt"

with open(log_file, "w") as f:
    f.write(f"Python: {sys.executable}\n")
    f.write(f"Torch: {torch.__version__}\n")
    f.write(f"CUDA Available: {torch.cuda.is_available()}\n")
    if torch.cuda.is_available():
        f.write(f"Device Count: {torch.cuda.device_count()}\n")
        f.write(f"Current Device: {torch.cuda.current_device()}\n")
        f.write(f"Device Name: {torch.cuda.get_device_name(0)}\n")
    else:
        f.write("CUDA NOT AVAILABLE\n")

print(open(log_file).read())
