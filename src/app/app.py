import base64
import io
import json
import os

import boto3
import streamlit as st
from PIL import Image

# モデルの定義
CLAUDE_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"

STABILITY_MODELS = {
    "Stable Image Core": "stability.stable-image-core-v1:0",
    "SD3 Large": "stability.sd3-large-v1:0",
    "Stable Image Ultra": "stability.stable-image-ultra-v1:0",
}

# AWS Bedrockクライアントの初期化
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-west-2")

st.title("新しいStability AIモデルで画像生成を試そう")

# 生成モードの選択
generation_mode = st.radio(
    "生成モードを選択してください:", ["text-to-image", "image-to-image"]
)

# 画像生成プロンプトのテキストボックス
japanese_prompt = st.text_input("画像生成のための日本語プロンプトを入力してください:")

# 画像アップロード
uploaded_file = None
if generation_mode == "image-to-image":
    uploaded_file = st.file_uploader(
        "元の画像をアップロードしてください", type=["png", "jpg", "jpeg"]
    )

# レイアウトの設定：左側にアップロード画像、右側に生成画像を表示
col1, col2 = st.columns(2)

# アップロードした画像の表示（左側）
if uploaded_file is not None:
    with col1:
        st.image(uploaded_file, caption="アップロードした画像", use_column_width=True)


# プロンプトの翻訳関数
def translate_to_english(japanese_text):
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": f"""あなたは日本語を英語に翻訳し、画像生成に適したプロンプトを作成するエキスパートです。
以下の日本語テキストを英語に翻訳し、Stable Diffusionのような画像生成AIで使用するのに適したプロンプトに変換してください。
翻訳されたプロンプトのみを出力してください。

日本語テキスト: {japanese_text}""",
                }
            ],
        }
    )

    response = bedrock_runtime.invoke_model(modelId=CLAUDE_MODEL, body=body)
    response_body = json.loads(response["body"].read())
    return response_body["completion"].strip()


# 画像のリサイズ関数
def resize_image(image, max_size=1536):
    width, height = image.size
    if width > max_size or height > max_size:
        ratio = max_size / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size, Image.LANCZOS)
    return image


# 画像生成ボタン
if st.button("画像生成"):
    if japanese_prompt:
        with st.spinner("プロンプトを翻訳中..."):
            english_prompt = translate_to_english(japanese_prompt)
            st.write("翻訳されたプロンプト:", english_prompt)

        with st.spinner("画像を生成中..."):
            try:
                body = {"prompt": english_prompt, "mode": generation_mode}

                if generation_mode == "image-to-image":
                    if uploaded_file is not None:
                        image = Image.open(uploaded_file)
                        image = resize_image(image)
                        buffered = io.BytesIO()
                        image.save(buffered, format="PNG")
                        image_bytes = buffered.getvalue()
                        base64_image = base64.b64encode(image_bytes).decode("utf-8")
                        body["image"] = base64_image
                        body["strength"] = 0.75
                    else:
                        st.error("画像をアップロードしてください。")
                        st.stop()

                response = bedrock_runtime.invoke_model(
                    modelId=STABILITY_MODELS["SD3 Large"],  # モデルを選択
                    body=json.dumps(body),
                )
                output_body = json.loads(response["body"].read().decode("utf-8"))
                base64_output_image = output_body["images"][0]
                image_data = base64.b64decode(base64_output_image)

                generated_image = Image.open(io.BytesIO(image_data))

                # 生成結果の表示（右側）
                with col2:
                    st.image(
                        generated_image, caption="生成された画像", use_column_width=True
                    )

                # 生成された画像の保存
                output_dir = "output"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                i = 1
                while os.path.exists(os.path.join(output_dir, f"img_{i}.png")):
                    i += 1

                image_path = os.path.join(output_dir, f"img_{i}.png")
                generated_image.save(image_path)

                st.success(f"生成された画像が {image_path} に保存されました")

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                if "output_body" in locals():
                    st.write("APIレスポンス全体:", output_body)
    else:
        st.warning("プロンプトを入力してください。")
