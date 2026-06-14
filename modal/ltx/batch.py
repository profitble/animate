import json
import re
from pathlib import Path

from run import app, generate

WORKFLOW = Path(__file__).parent.parent / "workflows" / "ltx-api.json"

_PAIR_RE = re.compile(
    r"## Pair (\d+) — `([a-f0-9]+)`\s*\n"
    r"- \*\*Image:\*\* (\S+)\s*\n"
    r"- \*\*Video:\*\* (\S+)",
    re.MULTILINE,
)


def parse_pairs(path: str) -> list[dict]:
    text = Path(path).read_text()
    pairs = []
    for m in _PAIR_RE.finditer(text):
        pairs.append({
            "local_index": int(m.group(1)),
            "pair_code": m.group(2),
            "image_url": m.group(3),
            "video_url": m.group(4),
        })
    if not pairs:
        raise ValueError(f"No pairs found in {path}")
    return pairs


@app.local_entrypoint()
def batch(pairs_file: str = "../pairs.md"):
    pairs = parse_pairs(pairs_file)
    with open(WORKFLOW) as f:
        workflow_data = json.load(f)

    print(f"Spawning {len(pairs)} jobs ...\n")

    calls = []
    for pair in pairs:
        call = generate.spawn(workflow_data, pair["image_url"], pair.get("prompt", ""), pair["pair_code"])
        calls.append((pair, call))
        print(f"  spawned {pair['local_index']}")

    print(f"\n{len(pairs)} jobs running ...\n")
    for pair, call in calls:
        try:
            path = call.get()
            print(f"  {pair['local_index']} done → {path}")
        except Exception as e:
            print(f"  {pair['local_index']} failed: {e}")

    print("\ndone. get outputs: modal volume get ltx-outputs / .")
