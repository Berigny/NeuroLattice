import json
from pathlib import Path

def load_brand_kernel(path='memory/brand_identity_kernel.json'):
    with open(Path(path), 'r') as f:
        return json.load(f)
