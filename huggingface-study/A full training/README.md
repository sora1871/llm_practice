# 🤗 Hugging Face Transformers 学習メモ（MRPC / BERT Fine-tuning）

このリポジトリは、Hugging Face Transformers を用いた  
**BERTのファインチューニング（GLUE MRPCタスク）**の学習内容をまとめたものです。

---

## 🎯 タスク概要

- データセット：GLUE MRPC
- タスク：2文が同じ意味かどうかの分類
  - 0：異なる
  - 1：同じ（パラフレーズ）

---

## 🧠 学習の全体フロー

```text
データ読み込み
↓
トークナイズ
↓
データ整形
↓
DataLoader作成
↓
モデル準備
↓
学習（forward → loss → backward → update）
↓
評価
📦 使用ライブラリ
transformers
datasets
torch
evaluate
accelerate
🔤 データ前処理
トークナイズ
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
ポイント
文ペアを同時にトークナイズ
truncation=True で長さ制限
🧹 データ整形
tokenized_datasets = tokenized_datasets.remove_columns(["sentence1", "sentence2", "idx"])
tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
tokenized_datasets.set_format("torch")
ポイント
不要カラム削除
label → labels（モデル仕様）
PyTorch Tensorに変換
🚚 DataLoader
train_dataloader = DataLoader(
    tokenized_datasets["train"],
    shuffle=True,
    batch_size=8,
    collate_fn=data_collator
)
ポイント
ミニバッチ処理
DataCollatorWithPadding で動的パディング
🤖 モデル
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)
ポイント
BERT + 分類ヘッド
出力：logits（形状 [batch_size, 2]）
⚙️ Optimizer
optimizer = AdamW(model.parameters(), lr=3e-5)
Adam vs AdamW
AdamWは weight decayを分離（decoupled）
より適切な正則化が可能
Transformerでは標準
📉 Scheduler
lr_scheduler = get_scheduler(
    "linear",
    optimizer=optimizer,
    num_warmup_steps=0,
    num_training_steps=num_training_steps,
)
ポイント
学習率を徐々に減少
後半の微調整を安定化
🔥 学習ループ（核心）
model.train()

for epoch in range(num_epochs):
    for batch in train_dataloader:
        outputs = model(**batch)
        loss = outputs.loss

        loss.backward()        # 勾配計算
        optimizer.step()       # 重み更新
        lr_scheduler.step()    # 学習率更新
        optimizer.zero_grad()  # 勾配リセット
💡 学習の本質
forward → loss → backward → update
loss.backward()：どこを直すか計算
optimizer.step()：実際に修正
⚡ GPU対応
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

batch = {k: v.to(device) for k, v in batch.items()}
ポイント
モデルとデータは同じデバイスに置く
🚀 Accelerate版
accelerator = Accelerator()

train_dl, eval_dl, model, optimizer = accelerator.prepare(
    train_dataloader, eval_dataloader, model, optimizer
)

accelerator.backward(loss)
メリット
GPU管理を自動化
分散学習対応
コードがシンプル
📊 評価
model.eval()

with torch.no_grad():
    outputs = model(**batch)

predictions = torch.argmax(outputs.logits, dim=-1)
ポイント
model.eval()：評価モード
torch.no_grad()：勾配計算オフ
argmax：クラス決定
🧪 評価指標（MRPC）
metric.compute()

出力例：

{'accuracy': 0.84, 'f1': 0.88}
🧠 学んだ重要ポイント
1. モデル入力
model(**batch)

👉 辞書を展開して入力

2. logits
モデルの生の出力（確率ではない）
argmaxで予測に変換
3. backwardの役割

👉 誤差をもとに修正量を計算

4. optimizer.step()

👉 実際にモデルを更新

5. zero_grad()

👉 勾配をリセット（重要）

6. 学習と評価の違い
項目	学習	評価
model.train()	✅	❌
model.eval()	❌	✅
backward	✅	❌
no_grad	❌	✅
🧩 よくあるミス
device不一致（CPU/GPU）
labelsにリネームし忘れ
zero_grad()忘れ
eval時にno_grad()しない
✨ まとめ
Transformersの学習は以下の繰り返し：
データ → 予測 → 誤差 → 修正
AdamW + Scheduler が基本構成
Accelerateでスケーラブルに拡張可能
🚀 次にやること
推論（inference）
ハイパーパラメータ調整
他タスク（NER / QA）
📎 参考
Hugging Face Transformers
GLUE Benchmark

---

# 👍 補足

もし希望あれば：

- 🔥 **もっと“強いREADME”（面接・ポートフォリオ用）**
- 📊 図付きバージョン
- 🧠 「なぜそうなるか」深掘り版

も作れます。
どっちかというと、コードの意味の説明というより、そこから学んだエッセンスとか、独自の見解を載せたいです。Markdown形式で書いてください

いい方向性です 👍
「コードの説明」ではなく、理解・抽象化・自分の言葉に振ると一気に価値が上がります。

そのコンセプトでREADMEを書きました👇

# 🧠 Hugging Face Transformers 学習ノート（本質まとめ）

このドキュメントは、BERTのファインチューニングを通して得た  
**「コードの意味」ではなく「理解した本質」**をまとめたものです。

---

## 🎯 この章でやっていたこと（本質）

一言でいうと：

> **「モデルの間違いを少しずつ減らす仕組み」**

すべてのコードは、この1行に集約できる。

```text
予測 → 誤差 → 修正 → 繰り返し
🔁 学習とは何か

学習ループは複雑に見えるが、本質は非常にシンプル：

1. モデルが予測する
2. 正解と比較する（loss）
3. どこを直すべきか計算する（backward）
4. 実際に修正する（optimizer.step）

重要なのは：

「モデルは正解を知らないが、間違いは教えられる」

⚙️ backward と step の役割

ここが最も重要な理解ポイントだった。

loss.backward()
→ どのパラメータをどれだけ動かすべきか計算する
optimizer.step()
→ 実際にパラメータを更新する

つまり：

backward = 計画
step     = 実行
📉 loss の意味

lossは単なる数値ではなく：

「モデルの現在の理解のズレ」

小さいほど正しい方向にいる。

🧠 logits の理解

モデルの出力（logits）は確率ではない。

logits = モデルの「自信スコア」

最終的な予測は：

argmax(logits)

つまり：

「一番自信がある答えを選ぶ」

🧩 モデルは何を学んでいるのか

モデルは「文章の意味」を理解しているわけではない。

「パターン」を学習している

単語の組み合わせ
文の構造
似ている/似ていない特徴
🔒 正則化（Adam vs AdamW）

ここはかなり重要な気づきだった。

Adam：正則化が勾配に混ざる
AdamW：正則化を分離する

つまり：

学習（勾配）と制約（正則化）は別物

👉 AdamWの方が「役割が明確」

📉 学習率のスケジューリング

学習率は固定ではなく、時間とともに変化させる。

最初：大きく学ぶ
後半：慎重に調整

これは人間の学習にも近い。

⚡ GPUと計算の本質

重要なルール：

モデルとデータは同じ場所に置く

CPU ↔ GPU が混ざると壊れる
🚀 Accelerateの本質

Accelerateは単なる便利ツールではない。

「計算環境の抽象化レイヤー」

device管理
分散処理
mixed precision

を隠してくれる

🧪 学習と評価の違い

これは明確に分ける必要がある：

学習	評価
間違いから学ぶ	成績を測る
backwardあり	backwardなし
trainモード	evalモード
🔁 データ処理の本質

トークナイズの本質は：

「テキストを数値に変換する」

モデルは数値しか扱えない。

📦 DataLoaderの役割

DataLoaderはただの便利機能ではなく：

「データの供給装置」

バッチ化
シャッフル
パディング
💡 一番大きな気づき

今回一番重要だった理解はこれ：

ディープラーニングは「賢さ」を作っているのではなく「誤差を減らしている」

🧠 メタな理解

Transformerを使った学習は：

大量のパラメータを
↓
少しずつ調整して
↓
誤差を最小化するプロセス
✨ 最後に

この章を通して感じたのは：

複雑に見えるが、本質は非常に単純

そして：

理解すべきは「コード」ではなく「流れ」

🚀 次に意識すること
なぜこのハイパーパラメータなのか
なぜこのモデル構造なのか
どうすれば精度が上がるのか
🔚 総括
機械学習 = 間違いを減らす仕組み

これに尽きる。