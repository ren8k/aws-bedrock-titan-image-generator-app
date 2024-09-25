from typing import Any, Dict, List, Optional

import streamlit as st
import utils
from streamlit.runtime.uploaded_file_manager import UploadedFile


def get_generation_mode() -> str:
    return st.sidebar.selectbox(
        "生成モードを選択してください:",
        [
            "TEXT_IMAGE",
            "IMAGE_CONDITIONING",
            "INPAINTING",
            "REMOVAL",
            "OUTPAINTING",
            "IMAGE_VARIATION",
            "COLOR_GUIDED_GENERATION",
            "BACKGROUND_REMOVAL",
        ],
    )


def get_no_of_images() -> int:
    return st.sidebar.number_input(
        "生成する画像の数を入力してください:", min_value=1, max_value=5, value=1
    )


def get_seed() -> int:
    return st.sidebar.number_input(
        "シード値を入力してください:", min_value=0, max_value=2147483646
    )


def get_cfg_scale() -> float:
    return st.sidebar.slider(
        "スケールを入力してください:", min_value=1.1, max_value=10.0, value=8.0
    )


def get_prompt() -> str:
    return st.text_input("プロンプトを入力してください:")


def get_negative_prompt() -> str:
    return st.text_input(
        "ネガティブプロンプトを入力してください:",
        value="bad quality, low res, noise",
    )


def upload_image(
    label: str = "入力画像をアップロードしてください",
) -> Optional[UploadedFile]:
    return st.file_uploader(label, type=["png", "jpg", "jpeg"])


def display_uploaded_image(uploaded_file: UploadedFile) -> None:
    if uploaded_file is not None:
        st.image(uploaded_file, caption="アップロードした画像", use_column_width=True)


def get_control_mode() -> str:
    return st.selectbox("制御モードを選択してください:", ["CANNY_EDGE", "SEGMENTATION"])


def get_control_strength() -> float:
    return st.slider("制御強度:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)


def get_mask_prompt() -> str:
    return st.text_input("マスクプロンプトを入力してください:")


def get_outpainting_mode() -> str:
    return st.selectbox("アウトペインティングモード:", ["PRECISE", "DEFAULT"])


def get_similarity_strength() -> float:
    return st.slider("類似度の強さ:", min_value=0.2, max_value=1.0, value=0.7, step=0.1)


# def get_colors() -> List[str]:
#     color_input = st.text_input("カラーを入力してください (カンマ区切り):")
#     return [color.strip() for color in color_input.split(",") if color.strip()]


def get_no_of_colors() -> int:
    return st.number_input(
        "色の数を入力してください:", min_value=1, max_value=5, value=2
    )


def select_color_palette(no_of_colors: int = 5) -> List[str]:
    st.write("カラーパレットを選択")
    colors = []
    cols = st.columns(no_of_colors)

    for i in range(no_of_colors):
        with cols[i]:
            color = st.color_picker(f"色 {i+1}", f"#{i*30:02x}{i*30:02x}{i*30:02x}")
            colors.append(color)

    return colors


def render_ui_components(mode: str) -> Dict[str, Any]:
    payload_params: Dict[str, Any] = {}

    if mode == "TEXT_IMAGE":
        payload_params["prompt"] = get_prompt()
        payload_params["negative_prompt"] = get_negative_prompt()

    elif mode == "IMAGE_CONDITIONING":
        payload_params["prompt"] = get_prompt()
        payload_params["negative_prompt"] = get_negative_prompt()
        input_image = upload_image()
        if input_image:
            display_uploaded_image(input_image)
            image_bytes = input_image.getvalue()
            payload_params["input_image"] = utils.bytes_to_base64(image_bytes)
        payload_params["control_mode"] = get_control_mode()
        payload_params["control_strength"] = get_control_strength()

    elif mode in ["INPAINTING", "OUTPAINTING", "REMOVAL"]:
        if mode in ["INPAINTING", "OUTPAINTING"]:
            payload_params["prompt"] = get_prompt()
        payload_params["negative_prompt"] = get_negative_prompt()
        input_image = upload_image()
        if input_image:
            display_uploaded_image(input_image)
            image_bytes = input_image.getvalue()
            payload_params["input_image"] = utils.bytes_to_base64(image_bytes)
        mask_image = upload_image("マスク画像をアップロードしてください")
        if mask_image:
            display_uploaded_image(mask_image)
            mask_bytes = mask_image.getvalue()
            payload_params["mask_image"] = utils.bytes_to_base64(mask_bytes)
        mask_prompt = get_mask_prompt()
        if mask_prompt:
            payload_params["mask_prompt"] = mask_prompt
        if mode == "OUTPAINTING":
            payload_params["outpainting_mode"] = get_outpainting_mode()

    elif mode == "IMAGE_VARIATION":
        payload_params["prompt"] = get_prompt()
        payload_params["negative_prompt"] = get_negative_prompt()
        input_image = upload_image()
        if input_image:
            display_uploaded_image(input_image)
            image_bytes = input_image.getvalue()
            payload_params["input_images"] = [utils.bytes_to_base64(image_bytes)]
        payload_params["similarity_strength"] = get_similarity_strength()

    elif mode == "COLOR_GUIDED_GENERATION":
        payload_params["prompt"] = get_prompt()
        payload_params["negative_prompt"] = get_negative_prompt()
        # payload_params["colors"] = get_colors()
        no_of_colors = get_no_of_colors()
        payload_params["colors"] = select_color_palette(no_of_colors)
        reference_image = upload_image(
            "参照画像をアップロードしてください (オプション)"
        )
        if reference_image:
            display_uploaded_image(reference_image)
            image_bytes = reference_image.getvalue()
            payload_params["reference_image"] = utils.bytes_to_base64(image_bytes)

    elif mode == "BACKGROUND_REMOVAL":
        input_image = upload_image()
        if input_image:
            display_uploaded_image(input_image)
            image_bytes = input_image.getvalue()
            payload_params["input_image"] = utils.bytes_to_base64(image_bytes)

    else:
        st.error("不明な生成モードです。")

    return payload_params


def show_results(images: list) -> None:
    st.header("生成結果")
    if len(images) == 1:
        st.image(images[0], caption="生成された画像", use_column_width=True)
    else:
        cols = st.columns(len(images))
        for idx, col in enumerate(cols):
            with col:
                st.image(
                    images[idx],
                    caption=f"生成された画像 {idx+1}",
                    use_column_width=True,
                )
