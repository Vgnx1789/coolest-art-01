"""make.fun coolest-art-01 entry.

The artwork ships in this repository as entry.png (a JPEG image under a
.png name, which the competition allows: the format is told from the
first bytes). This program simply delivers those exact bytes to the
output directory, so both grading runs produce the identical file.
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576  # competition cap: at most 1 MiB
SIGNATURES = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n")  # JPEG, PNG


def load_artwork() -> bytes:
    """Read the artwork and verify it still satisfies the gate's rules."""
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if not data.startswith(SIGNATURES):
        raise ValueError("entry.png is neither a JPEG nor a PNG image")
    return data


def main() -> None:
    data = load_artwork()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    with target.open("wb") as fh:
        for offset in range(0, len(data), 65_536):
            fh.write(data[offset : offset + 65_536])


if __name__ == "__main__":
    main()
