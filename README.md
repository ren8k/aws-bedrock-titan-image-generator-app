# Amazon Titan Image Generator v2 Application

本リポジトリでは，以下に示す Amazon Titan Image Generator v2 の全機能を利用可能な streamlit アプリケーションと，SAM2 によるセグメンテーション実行用の Jupyter Notebook を公開している．

- Amazon Titan Image Generator v2 の全機能を利用するためのアプリケーションの実装
- [Segment Anything Model 2 (SAM 2)](https://github.com/facebookresearch/segment-anything-2)を利用したセグメンテーションマスク生成用の Jupyter Notebook

> [!NOTE]
> Amazon Titan Image Generator v2 の解説記事を Qiita に投稿しております．
> 是非そちらもご覧下さい！
> <br> [Amazon Titan Image Generator v2 の全機能を徹底検証：機能解説と実践ガイド](https://qiita.com/ren8k)

<img src="./assets/demo.gif">

> Amazon Titan Image Generator v2 の全機能が利用可能な streamlit アプリケーション

| 入力画像                                          | セグメンテーションマスク画像                            |
| ------------------------------------------------- | ------------------------------------------------------- |
| <img src="./images/input/dogcat.png" width="300"> | <img src="./images/mask/masks_dog_cat.png" width="300"> |

> SAM2 によるセグメンテーション実行結果

## 検証環境

以下の環境で動作確認済みである．AWS を利用する場合，G5 インスタンスなどを推奨する．

- OS: Ubuntu 22.04.4 LTS
- CPU: Intel(R) Core(TM) i9-12900K
- RAM: 64GB
- GPU: NVIDIA GeForce RTX 3090

> [!WARNING]
> アプリケーションの実行には GPU は不要である．SAM2 を利用する場合，上記のような GPU リソースが必要となる．

## 環境構築

VSCode の Dev Container を利用する．

> [!WARNING]
> アプリケーションのみを実行する場合，実行環境に基本的なライブラリ (streamlit, boto3, Pillow など) が install されている場合，Dev Container は不要である．SAM2 を利用する場合，pytorch，nvidia driver，cuda などの環境構築が必要となるため，Dev Container の利用を推奨する．

## Amazon Titan Image Generator v2 のアプリケーション実行方法

```bash
cd src/app
python run_app.py
```

## SAM2 の実行方法

- Dev Conatiner でコンテナを起動しログインする．
  - ctrl + shift + p でコマンドパレットを開き，`Dev-Containers: Rebuild Container` を選択する．
- [`./notebook/automatic_mask_generator_example.ipynb`](https://github.com/ren8k/aws-bedrock-titan-image-generator-app/blob/main/notebook/automatic_mask_generator_example.ipynb)を実行する．
