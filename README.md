# aws-bedrock-titan-image-verification

> [!NOTE]
> 本アプリおよび，Amazon Titan Image Generator v2 の解説記事を Qiita に投稿しております．
> 是非そちらもご覧下さい！
> <br> [Amazon Titan Image Generator v2 の全機能を徹底検証：機能解説と実践ガイド](https://qiita.com/ren8k)

<img src="./assets/demo.gif">

## 検証環境

以下の環境で動作確認済みである．AWS を利用する場合，G5 インスタンスなどを推奨する．

- OS: Ubuntu 22.04.4 LTS
- CPU: Intel(R) Core(TM) i9-12900K
- RAM: 64GB
- GPU: NVIDIA GeForce RTX 3090

> [!NOTE]
> アプリケーションのみの実行には，GPU は不要である．SAM2 を利用する場合，上記のような GPU リソースが必要となる．

## 環境構築

VSCode の Dev Container を利用する．

> [!NOTE]
> アプリケーションのみの実行には，Dev Container は不要である．SAM2 を利用する場合，pytorch，nvidia driver，cuda などの環境構築が必要となるため，Dev Container の利用を推奨する．

## アプリケーションの実行方法

```bash
cd src/app
python run_app.py
```

## SAM2 の実行方法
