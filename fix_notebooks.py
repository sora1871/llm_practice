import json
from pathlib import Path

for path in Path(".").rglob("*.ipynb"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            nb = json.load(f)

        changed = False

        # notebook全体の metadata.widgets を修正
        metadata = nb.get("metadata", {})
        if "widgets" in metadata:
            widgets = metadata["widgets"]

            # widgets が辞書なら state を補う
            if isinstance(widgets, dict):
                if "state" not in widgets:
                    widgets["state"] = {}
                    changed = True
            else:
                # 想定外の形式なら削除
                del metadata["widgets"]
                changed = True

        # 各セル内の metadata.widgets があれば削除
        for cell in nb.get("cells", []):
            cell_metadata = cell.get("metadata", {})
            if "widgets" in cell_metadata:
                del cell_metadata["widgets"]
                changed = True

        if changed:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(nb, f, ensure_ascii=False, indent=1)
            print(f"fixed: {path}")

    except Exception as e:
        print(f"skip: {path} -> {e}")