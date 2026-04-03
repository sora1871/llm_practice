# llm_practice

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
