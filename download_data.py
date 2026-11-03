"""Download the release data, verify SHA-256, and decompress the two models."""
from pathlib import Path
import gzip
import hashlib
import shutil
import urllib.request

RELEASE = "https://github.com/wille614/a4-19-6-8-certificate/releases/download/v1.0.0/"
MODELS = {
    "compressed_model.json": "576bf52f6215a94876ca80ec768620ea052e5c544df1d55d15aa7559942df0a5",
    "compressed.dat-s": "370d99f1ca1acdcb6e5cda21946b0533da236c3544235a807efaa367b1708cdb",
}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    root = Path(__file__).resolve().parent
    data = root / "data"
    data.mkdir(exist_ok=True)
    manifest = (root / "SHA256SUMS").read_text(encoding="utf-8")
    for line in manifest.splitlines():
        expected, name = line.split()
        destination = data / name
        print("Downloading " + name, flush=True)
        with urllib.request.urlopen(RELEASE + name, timeout=120) as response:
            with destination.open("xb") as output:
                shutil.copyfileobj(response, output, 1048576)
        if digest(destination) != expected:
            raise ValueError("SHA-256 mismatch: " + name)
        print("SHA-256 OK: " + name, flush=True)
    for name, expected in MODELS.items():
        destination = data / name
        with gzip.open(data / (name + ".gz"), "rb") as source:
            with destination.open("xb") as output:
                shutil.copyfileobj(source, output, 1048576)
        if digest(destination) != expected:
            raise ValueError("Decompressed SHA-256 mismatch: " + name)
        print("SHA-256 OK: " + name, flush=True)


if __name__ == "__main__":
    main()
