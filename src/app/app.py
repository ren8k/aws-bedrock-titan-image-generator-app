import config
import streamlit as st
import ui_components as ui
import utils
from image_generator import ImageGenerator


def main() -> None:
    st.title("Amazon Titan Image Generator v2 App")
    img_generator = ImageGenerator(region=config.AWS_REGION)
    mode = ui.get_generation_mode()
    st.header(f"生成モード: {mode}")

    # get inference parameters
    no_of_images = ui.get_no_of_images()
    seed = ui.get_seed()
    cfg_scale: float = ui.get_cfg_scale()
    payload_params = ui.render_ui_components(mode)

    if st.button("Generate Image"):
        payload = img_generator.make_payload(mode=mode, **payload_params)
        with st.spinner("Drawing..."):
            try:
                response = img_generator.generate_image(
                    payload=payload,
                    model_id=config.MODEL_ID,
                    num_image=no_of_images,
                    cfg_scale=cfg_scale,
                    seed=seed,
                )
                images = img_generator.extract_images_from(response)
                ui.show_results(images)
                utils.save_images(config.SAVE_DIR, images, seed=seed, mode=mode)
                st.success(f"生成画像を `{config.SAVE_DIR}` に保存しました")
            except Exception as e:
                st.error(f"画像生成時にエラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
