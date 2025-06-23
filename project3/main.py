import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from PIL import Image

def load_model():
    model = MobileNetV2(weights = "imagenet")
    return model
def preproccess_image(image):
    image = np.array(image)
    image = cv2.resize(image, (224, 224))
    image = preprocess_input(image)
    image = np.expand_dims(image, axis = 0)
    return image
def classify_image(model, image):
    try:
        proccessed_image = preproccess_image(image)
        predictions = model.predict(proccessed_image)
        decoded_predictions = decode_predictions(predictions, top = 3)[0]
        return decoded_predictions
    except Exception as e:
        st.error(f"Error occured: {str(e)}")
        return None
def main():
    st.set_page_config(page_title = "Image Classifier", page_icon = None, layout = "centered")
    st.title("Image Classifier")
    st.write("Upload an image and let the classifer work")
    file = st.file_uploader("Choose a file to upload", type = ["png", "jpg"])
    @st.cache_resource
    def load_cached_model():
        return load_model()
    model = load_cached_model()
    if file:
        st.image(file, caption = "Here is the image")
        button = st.button("Classify image")
        if button:
            with st.spinner("Providing analysis"):
                image = Image.open(file)
                predictions = classify_image(model, image) ## change from tutorial
                if predictions:
                    st.subheader("Predictions")
                    for _, label, score in predictions:
                        st.write(f"**{label}**: {score:.2%}")



if __name__ == "__main__":
    main()

