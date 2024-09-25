import config
import streamlit as st
import utils
from image_generator import ImageGenerator
from ui_components import (
    get_cfg_scale,
    get_generation_mode,
    get_no_of_images,
    get_seed,
    render_ui_components,
    show_results,
)


def main() -> None:
    st.title("Amazon Titan Image Generator v2 App")
    img_generator = ImageGenerator(region=config.AWS_REGION)
    mode = get_generation_mode()
    st.header(f"生成モード: {mode}")

    # get inference parameters
    no_of_images = get_no_of_images()
    seed = get_seed()
    cfg_scale: float = get_cfg_scale()
    payload_params = render_ui_components(mode)

    if st.button("Generate Image"):
        payload = img_generator.make_payload(mode=mode, **payload_params)
        with st.spinner("Generating image..."):
            try:
                response = img_generator.generate_image(
                    payload=payload,
                    model_id=config.MODEL_ID,
                    num_image=no_of_images,
                    cfg_scale=cfg_scale,
                    seed=seed,
                )
                images = img_generator.extract_images_from(response)
                show_results(images)
                utils.save_images(config.SAVE_DIR, images, seed=seed, mode=mode)
                st.success(f"生成された画像が {config.SAVE_DIR} に保存されました")
            except Exception as e:
                st.error(f"画像生成中にエラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
