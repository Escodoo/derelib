from pathlib import Path

SAMPLES = Path(__file__).resolve().parent / "samples" / "v1_2_0"

EVENT_SAMPLES = {
    "D-1001": "d1001.xml",
    "D-1011": "d1011.xml",
    "D-1101": "d1101.xml",
    "D-1106": "d1106.xml",
    "D-1121": "d1121.xml",
    "D-1198": "d1198.xml",
    "D-1199": "d1199.xml",
}


def sample_xml(name: str) -> str:
    return (SAMPLES / name).read_text(encoding="utf-8")
