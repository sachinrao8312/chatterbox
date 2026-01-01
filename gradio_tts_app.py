import random
import numpy as np
import torch
import gradio as gr
from chatterbox.tts import ChatterboxTTS
import audio_saver


print("="*50)
print(f"Diagnostics: Python {random.__file__}") # Just to see path
if torch.cuda.is_available():
    print(f"✅ CUDA Available! Found {torch.cuda.device_count()} device(s).")
    print(f"   Current Device: {torch.cuda.get_device_name(0)}")
    print(f"   CUDA Version: {torch.version.cuda}")
    DEVICE = "cuda"
else:
    print("⚠️ CUDA NOT Available. Using CPU (High RAM usage expected).")
    print(f"   Torch Version: {torch.__version__}")
    DEVICE = "cpu"
print("="*50)

# NOTE: We avoid torch.set_default_device("cuda") to allow CPU operations for UI/Audio


def set_seed(seed: int):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)


def load_model():
    model = ChatterboxTTS.from_pretrained(DEVICE)
    return model


import audio_saver

def generate(model, text, audio_prompt_path, exaggeration, temperature, seed_num, cfgw, min_p, top_p, repetition_penalty, progress=gr.Progress()):
    if model is None:
        progress(0, "Loading Model...")
        model = ChatterboxTTS.from_pretrained(DEVICE)

    if seed_num != 0:
        set_seed(int(seed_num))

    progress(0.2, "Generating...")
    
    # --- GPU ENFORCEMENT & DIAGNOSTICS ---
    print(f"\n{'='*60}")
    print(f"🎯 CUDA CORES USAGE CHECK (Standard TTS)")
    print(f"{'='*60}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        print(f"✅ GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"   Pre-Gen Memory Allocated: {torch.cuda.memory_allocated()/1024**2:.2f} MB")
        print(f"   Model Device: {getattr(model, 'device', 'unknown')}")
        if hasattr(model, 't3'):
            print(f"   T3 Model Device: {next(model.t3.parameters()).device}")
        if hasattr(model, 's3gen'):
            print(f"   S3Gen Model Device: {next(model.s3gen.parameters()).device}")
    else:
        print("❌ CUDA IS NOT AVAILABLE! Generation will use CPU (very slow).")
    print(f"{'='*60}")
    
    # GPU timing
    if torch.cuda.is_available():
        start_event = torch.cuda.Event(enable_timing=True)
        end_event = torch.cuda.Event(enable_timing=True)
        start_event.record()
    # -----------------
    
    wav = model.generate(
        text,
        audio_prompt_path=audio_prompt_path,
        exaggeration=exaggeration,
        temperature=temperature,
        cfg_weight=cfgw,
        min_p=min_p,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
    )
    
    # --- GPU POST-GENERATION DIAGNOSTICS ---
    if torch.cuda.is_available():
        end_event.record()
        torch.cuda.synchronize()
        gpu_time_ms = start_event.elapsed_time(end_event)
        print(f"\n{'='*60}")
        print(f"🚀 CUDA GENERATION COMPLETE (Standard TTS)")
        print(f"{'='*60}")
        print(f"   GPU Kernel Time: {gpu_time_ms:.2f} ms")
        print(f"   Post-Gen Memory: {torch.cuda.memory_allocated()/1024**2:.2f} MB")
        print(f"   Peak Memory: {torch.cuda.max_memory_allocated()/1024**2:.2f} MB")
        print(f"{'='*60}\n")
    # -----------------
    
    progress(0.9, "Saving...")
    audio_data = wav.squeeze(0).numpy()
    audio_saver.save_audio_output(model.sr, audio_data, "Standard")
    
    return (model.sr, audio_data)


with gr.Blocks() as demo:
    model_state = gr.State(None)  # Loaded once per session/user

    with gr.Row():
        with gr.Column():
            text = gr.Textbox(
                value="Now let's make my mum's favourite. So three mars bars into the pan. Then we add the tuna and just stir for a bit, just let the chocolate and fish infuse. A sprinkle of olive oil and some tomato ketchup. Now smell that. Oh boy this is going to be incredible.",
                label="Text to synthesize (max chars 300)",
                max_lines=5
            )
            ref_wav = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Reference Audio File", value=None)
            exaggeration = gr.Slider(0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5, extreme values can be unstable)", value=.5)
            cfg_weight = gr.Slider(0.0, 1, step=.05, label="CFG/Pace", value=0.5)

            with gr.Accordion("More options", open=False):
                seed_num = gr.Number(value=0, label="Random seed (0 for random)")
                temp = gr.Slider(0.05, 5, step=.05, label="temperature", value=.8)
                min_p = gr.Slider(0.00, 1.00, step=0.01, label="min_p || Newer Sampler. Recommend 0.02 > 0.1. Handles Higher Temperatures better. 0.00 Disables", value=0.05)
                top_p = gr.Slider(0.00, 1.00, step=0.01, label="top_p || Original Sampler. 1.0 Disables(recommended). Original 0.8", value=1.00)
                repetition_penalty = gr.Slider(1.00, 2.00, step=0.1, label="repetition_penalty", value=1.2)

            run_btn = gr.Button("Generate", variant="primary")

        with gr.Column():
            audio_output = gr.Audio(label="Output Audio")

    demo.load(fn=load_model, inputs=[], outputs=model_state)

    run_btn.click(
        fn=generate,
        inputs=[
            model_state,
            text,
            ref_wav,
            exaggeration,
            temp,
            seed_num,
            cfg_weight,
            min_p,
            top_p,
            repetition_penalty,
        ],
        outputs=audio_output,
    )

if __name__ == "__main__":
    demo.queue(
        max_size=50,
        default_concurrency_limit=1,
    ).launch(share=True)
