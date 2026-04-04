# llm_practice

English version is first. Japanese version is below.

## English

This repository is used to manage Hugging Face study notebooks and small related experiments.

The main workflow is:

1. Work on a notebook in Google Colab
2. Download the `.ipynb` file locally
3. Place it in the appropriate folder in this repository
4. Run `python3 fix_notebooks.py`
5. Review changes with `git status`
6. Commit and push to GitHub

## Before Pushing Notebooks

If you updated any `.ipynb` files, run:

```bash
python3 fix_notebooks.py
git status
```

Then commit and push as usual:

```bash
git add .
git commit -m "update notebooks"
git push origin main
```

## Why `fix_notebooks.py` Is Required

Google Colab and Jupyter sometimes save widget state and progress-bar outputs inside notebook files.

In Hugging Face notebooks, model downloads and dataset downloads often leave widget-related outputs behind. If those outputs stay in the notebook, GitHub may fail to render the notebook preview and show `Invalid Notebook`.

`fix_notebooks.py` removes the most common sources of that problem:

- `metadata.widgets`
- outputs containing `application/vnd.jupyter.widget-view+json`

## Pre-Push Checklist

- If you changed `.ipynb` files, run `python3 fix_notebooks.py`
- Confirm `git status` does not include `*:Zone.Identifier`
- Confirm the notebook file structure is reasonable
- If needed, verify notebook preview rendering on GitHub

## Notes

- `*:Zone.Identifier` files are Windows metadata files and should never be committed
- A notebook can work in Colab and still fail in GitHub Preview
- In many cases, the notebook itself is fine and only the extra widget metadata causes the preview failure

---

## 日本語

このリポジトリは、Hugging Face 学習用の notebook と小さな実験コードを管理するためのものです。

現在の運用は、Google Colab で作成・実行した `.ipynb` をローカルに持ってきて、このリポジトリに配置し、ローカルから GitHub に push する形です。

## 基本フロー

1. Google Colab で notebook を作業する
2. `.ipynb` をローカルにダウンロードする
3. このリポジトリの適切な場所に notebook を置く
4. `python3 fix_notebooks.py` を実行する
5. `git status` で変更を確認する
6. `git add` / `git commit` / `git push` を行う

## notebook を push する前の手順

`.ipynb` を更新したときは、commit 前に次を実行してください。

```bash
python3 fix_notebooks.py
git status
```

その後、問題なければ通常どおり commit / push します。

```bash
git add .
git commit -m "update notebooks"
git push origin main
```

## なぜ `fix_notebooks.py` が必要か

Google Colab や Jupyter で notebook を実行すると、進捗バーや widget 情報が `.ipynb` に保存されることがあります。

特に Hugging Face 系の notebook では、モデルやデータセットのダウンロード進捗が widget 出力として残ることがあります。これが入ったまま GitHub に push されると、GitHub の Preview で `Invalid Notebook` になることがあります。

`fix_notebooks.py` は、GitHub Preview を壊しやすい次の情報を notebook から除去します。

- `metadata.widgets`
- `application/vnd.jupyter.widget-view+json` を含む出力

## push 前の確認ポイント

- `.ipynb` を更新したなら `python3 fix_notebooks.py` を実行したか
- `git status` に `*:Zone.Identifier` が出ていないか
- 不自然な `.ipynb` ディレクトリ構造になっていないか
- 必要なら GitHub 上で notebook Preview を開いて表示を確認する

## 補足

- `*:Zone.Identifier` は Windows 由来の不要ファイルです。このリポジトリでは commit しません
- Colab で動いても、GitHub Preview では widget 情報が原因で表示に失敗することがあります
- notebook 本体が壊れていなくても、付加情報だけで Preview が失敗することがあります
