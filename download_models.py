import os
from pathlib import Path
from huggingface_hub import hf_hub_download, snapshot_download

# Define the base directory for models relative to the project root
# This assumes this script is run from the project root or placed there
BASE_DIR = Path(__file__).parent / "pretrained_models"
BASE_DIR.mkdir(exist_ok=True)

def download_standard():
    print("Downloading Standard Chatterbox Models...")
    repo_id = "ResembleAI/chatterbox"
    dest_dir = BASE_DIR / "standard"
    dest_dir.mkdir(exist_ok=True, parents=True)
    
    files = ["ve.safetensors", "t3_cfg.safetensors", "s3gen.safetensors", "tokenizer.json", "conds.pt"]
    for filename in files:
        if (dest_dir / filename).exists():
            print(f"Skipping {filename} (already exists)")
            continue
        print(f"Downloading {filename}...")
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir=dest_dir, local_dir_use_symlinks=False)

def download_multilingual():
    print("Downloading Multilingual Chatterbox Models...")
    repo_id = "ResembleAI/chatterbox"
    dest_dir = BASE_DIR / "multilingual"
    dest_dir.mkdir(exist_ok=True, parents=True)
    
    files = ["ve.pt", "t3_mtl23ls_v2.safetensors", "s3gen.pt", "grapheme_mtl_merged_expanded_v1.json", "conds.pt", "Cangjie5_TC.json"]
    for filename in files:
        if (dest_dir / filename).exists():
            print(f"Skipping {filename} (already exists)")
            continue
        print(f"Downloading {filename}...")
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir=dest_dir, local_dir_use_symlinks=False)

def download_turbo():
    print("Downloading Chatterbox Turbo Models...")
    repo_id = "ResembleAI/chatterbox-turbo"
    dest_dir = BASE_DIR / "turbo"
    dest_dir.mkdir(exist_ok=True, parents=True)
    
    # Snapshot download for turbo
    if (dest_dir / "t3_turbo_v1.safetensors").exists():
        print("Skipping Turbo download (t3_turbo_v1.safetensors already exists)")
        return

    snapshot_download(
        repo_id=repo_id,
        local_dir=dest_dir,
        local_dir_use_symlinks=False,
        allow_patterns=["*.safetensors", "*.json", "*.txt", "*.pt", "*.model"]
    )

if __name__ == "__main__":
    download_standard()
    download_multilingual()
    download_turbo()
    print(f"\nAll models downloaded to: {BASE_DIR.absolute()}")
