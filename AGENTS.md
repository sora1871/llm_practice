# AGENTS.md

## Purpose

This repository contains Hugging Face study and project notebooks. Many `.ipynb` files are created in Google Colab and then uploaded to this repository.

## Notebook Handling Rules

- Treat Google Colab exported notebooks as potentially incompatible with GitHub Preview until verified.
- Each notebook directory should contain both the `.ipynb` file and a `README.md` that records the key takeaways or notes for that notebook.
- Before pushing any changed `.ipynb`, check whether the notebook contains broken widget metadata or widget-view outputs that can cause GitHub to show `Invalid Notebook`.
- If a notebook came from Colab, or if it contains progress bars / widget outputs, run `python3 fix_notebooks.py` before commit.
- After notebook cleanup, verify that changed `.ipynb` files no longer contain top-level `metadata.widgets` and no longer contain `application/vnd.jupyter.widget-view+json` outputs.
- Do not commit `*:Zone.Identifier` files. They must remain ignored.

## Pre-Push Expectation

When working on notebook changes, the agent should:

- inspect changed `.ipynb` files before push,
- confirm the notebook file itself is present in its directory before push,
- confirm that the same directory also includes a `README.md` with the notebook's takeaways or notes before push,
- run `python3 fix_notebooks.py` when needed,
- include notebook cleanup in the commit if widget-related incompatibility is present,
- verify GitHub Preview compatibility when the user asks for push verification.
