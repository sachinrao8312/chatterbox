
import os
import datetime
import torch
import numpy as np

# Try importing soundfile, or fallback to scipy
try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False
    try:
        import scipy.io.wavfile as wavfile
        HAS_SCIPY = True
    except ImportError:
        HAS_SCIPY = False

def save_audio_output(sr, audio_data, mode_prefix="Audio"):
    """
    Saves audio to the directory specified in CHATTERBOX_OUTPUT_DIR env var.
    If not set, does nothing.
    """
    output_dir = os.environ.get("CHATTERBOX_OUTPUT_DIR")
    if not output_dir:
        return

    # Ensure valid directory
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create output directory {output_dir}: {e}")
        return

    # Generate filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Chatterbox_{mode_prefix}_{timestamp}.wav"
    filepath = os.path.join(output_dir, filename)

    print(f"Saving copy to: {filepath}")
    
    try:
        # audio_data is typically (channels, samples) or (samples,)
        # It needs to be handled correctly depending on the library
        
        # Ensure it's CPU numpy
        if isinstance(audio_data, torch.Tensor):
            audio_data = audio_data.cpu().numpy()
            
        if HAS_SOUNDFILE:
            sf.write(filepath, audio_data, sr)
        elif HAS_SCIPY:
            # Scipy expects int16 or float32. 
            # Gradio often returns float32 in -1.0 to 1.0.
            wavfile.write(filepath, sr, audio_data)
        else:
            print("Warning: Neither soundfile nor scipy installed. Cannot save copy.")
            return None
            
        return filepath
            
    except Exception as e:
        print(f"Error saving audio copy: {e}")
        return None
