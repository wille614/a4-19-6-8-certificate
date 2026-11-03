# Exact rational certificate for A(19,6,8) ≤ 673

This repository accompanies Jiang Chang, **[A new upper bound for A(19,6,8)](https://arxiv.org/abs/2611.00173)**, arXiv:2611.00173.

For binary constant weight codes of length 19, weight 8, and minimum Hamming distance 6, the certificate establishes

```text
A(19,6,8) <= A4(19,6,8) <= U
U = 841300017883100309254921891583162664400313 / 1250000000000000000000000000000000000000
  = 673.0400143064802474039375132665301315202504
```

Since the code size is an integer, **A(19,6,8) ≤ 673**. The numerical solution was obtained with MOSEK 11.2.7. Verification uses only Python's standard-library `fractions.Fraction`; neither MOSEK nor a solver license is required.

## Reproduce the verification

Requirements: Git, CPython 3.11 or newer, an internet connection for downloading the release, and sufficient disk space and memory as described below. CPython 3.13.5 was used for the measured reproduction. There are no third-party Python dependencies; `requirements.txt` documents this empty dependency set.

Clone the repository:

```console
git clone https://github.com/wille614/a4-19-6-8-certificate.git
cd a4-19-6-8-certificate
```

On Windows, in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe download_data.py
.\.venv\Scripts\python.exe verify_certificate.py data
```

On Linux or macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python download_data.py
.venv/bin/python verify_certificate.py data
```

The download command fetches the three data files from **[Release v1.0.0](https://github.com/wille614/a4-19-6-8-certificate/releases/tag/v1.0.0)**, checks every compressed file against the repository's `SHA256SUMS`, decompresses both models, and checks their original hashes. Run it in a fresh checkout: it refuses to overwrite existing data files. After downloading, verification works offline. Do not use Python's `-O` or `-OO` options or set `PYTHONOPTIMIZE`, because the verifier uses assertions.

Alternatively, download the three data attachments and `SHA256SUMS` from the release into `data/`, verify their hashes from that directory with `sha256sum -c SHA256SUMS` (Linux) or `Get-FileHash -Algorithm SHA256` (PowerShell), and decompress the two model `.gz` files. Keep `certificate.json.gz` compressed. The verification directory must contain:

```text
data/
  certificate.json.gz
  compressed_model.json
  compressed.dat-s
```

## Expected result

The verifier prints a JSON object and writes `data/verification.json`. Successful verification has exit code 0 and these exact values (elapsed time and the certificate hash are also reported):

```json
{
  "status": "PASS",
  "arithmetic": "Python fractions.Fraction; no floating-point acceptance",
  "bound": "841300017883100309254921891583162664400313/1250000000000000000000000000000000000000",
  "integer_bound": 673,
  "blocks": 9123,
  "coefficients_checked": 59471389
}
```

Verification checks the two model hashes; reconstructs every rational LDLᵀ factorization with nonnegative diagonal; checks block dimensions and the objective; streams all 59,471,389 SDP coefficients; recomputes every residual, the box compensation, and the exact upper bound. The compensation is zero for this certificate. The checker does not import the model generator or the certificate producer.

## Model and data

The supplied SDP was constructed from the formulas in S. C. Polak, *Semidefinite programming bounds for constant-weight codes*, IEEE Transactions on Information Theory 65 (2019), 28–38, [arXiv:1703.05171](https://arxiv.org/abs/1703.05171), using the normalization and exact compression described in the accompanying paper. It has 8,603 variables and 9,123 blocks, of maximum order 79.

This release reproduces the exact certificate check for the supplied SDP. The derivation of the SDP from Polak's formulation is described in the paper. A model generator is not included because a standalone, byte-identical regeneration has not been validated for this release.

The uncompressed model hashes are listed below. The SDPA file has only a neutralized first comment; every byte after that comment is unchanged. The JSON model is byte-identical to the model used for the paper.

| File | Bytes | SHA-256 |
|---|---:|---|
| `compressed_model.json` | 1217249410 | `576bf52f6215a94876ca80ec768620ea052e5c544df1d55d15aa7559942df0a5` |
| `compressed.dat-s` | 1276809081 | `370d99f1ca1acdcb6e5cda21946b0533da236c3544235a807efaa367b1708cdb` |

All release attachment hashes are in [`SHA256SUMS`](SHA256SUMS). The certificate's public format identifier is `rational-ldlt-v1`; the format name and the SDPA file hash are the only updated certificate metadata. All rational entries, factorizations, residuals, and the bound are unchanged.

## Measured resources

Measured on 3 November 2026 with CPython 3.13.5, Windows 11 Pro 10.0.26200, an Intel Core i9-13980HX (32 logical processors), and 33954377728 bytes of installed memory:

| Measurement | Value |
|---|---:|
| Verification time reported by the checker | 593.273600 seconds |
| Complete process wall time | 595.172314 seconds |
| Peak working set of the Python verifier | 11489628160 bytes |

These timings exclude downloading and decompressing the data. Memory is the actual Python process's lifetime peak working set, obtained with Windows `GetProcessMemoryInfo`; the virtual-environment launcher is tracked separately. Verification is single-process. Allow 16 GB of RAM and 6 GB of free disk space for the downloaded data, decompressed models, and environment. Runtime depends on hardware and Python version.

## Citation and licenses

Please cite the paper; machine-readable metadata is provided in [`CITATION.cff`](CITATION.cff).

```bibtex
@article{Chang2026A1968,
  author = {Jiang Chang},
  title = {A new upper bound for {A(19,6,8)}},
  journal = {arXiv preprint arXiv:2611.00173},
  year = {2026},
  url = {https://arxiv.org/abs/2611.00173}
}
```

Copyright © 2026 Jiang Chang. Code is licensed under the **Apache License 2.0** ([official text](LICENSE)); the certificate and model data are licensed under **Creative Commons Attribution 4.0 International** ([official text](LICENSE-DATA)). Attribute data reuse to Jiang Chang and cite the paper above.
