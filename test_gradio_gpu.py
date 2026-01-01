
import gradio as gr
import torch
import sys

print(f"Python: {sys.executable}")
print(f"Torch: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)}")

def greet(name):
    return "Hello " + name

if __name__ == "__main__":
    print("Launching Gradio interface...")
    # Minimal launch to see if it crashes or suppresses CUDA
    # We won't actually block forever, just setup
    demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    print("Gradio initialized.")
    # Don't launch to avoid blocking, just checking init
