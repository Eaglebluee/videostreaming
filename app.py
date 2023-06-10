import cv2
import streamlit as st
import numpy as np
from PIL import Image
import io


class VideoTransformer:
    def __init__(self):
        self.selected_filter = "None"
        self.blur_rate = 0.5
        self.brightness_amount = 0
        self.apply_enhancement_filter = False

    def brighten_image(self, frame, amount):
        img_bright = cv2.convertScaleAbs(frame, beta=amount)
        return img_bright

    def blur_image(self, frame, amount):
        blur_img = cv2.GaussianBlur(frame, (11, 11), amount)
        return blur_img

    def enhance_details(self, frame):
        hdr = cv2.detailEnhance(frame, sigma_s=12, sigma_r=0.15)
        return hdr

    def cartoon_effect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)
        color = cv2.bilateralFilter(frame, 9, 250, 250)
        cartoon_img = cv2.bitwise_and(color, color, mask=edges)
        return cartoon_img

    def greyscale(self, frame):
        greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return greyscale

    def sepia(self, frame):
        frame_sepia = np.array(frame, dtype=np.float64)  # converting to float to prevent loss
        frame_sepia = cv2.transform(frame_sepia, np.matrix([[0.272, 0.534, 0.131],
                                                            [0.349, 0.686, 0.168],
                                                            [0.393, 0.769, 0.189]]))  # multiplying image with sepia matrix
        frame_sepia[np.where(frame_sepia > 255)] = 255  # normalizing values greater than 255 to 255
        frame_sepia = np.array(frame_sepia, dtype=np.uint8)
        return frame_sepia

    def pencil_sketch_grey(self, frame):
        sk_gray, sk_color = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
        return sk_gray

    def invert(self, frame):
        inv = cv2.bitwise_not(frame)
        return inv

    def summer(self, frame):
        summer_frame = frame.copy()
        summer_frame[..., 0] = np.clip(frame[..., 0] * 1.2, 0, 255)
        summer_frame[..., 2] = np.clip(frame[..., 2] * 0.8, 0, 255)
        return summer_frame

    def winter(self, frame):
        winter_frame = frame.copy()
        winter_frame[..., 0] = np.clip(frame[..., 0] * 0.8, 0, 255)
        winter_frame[..., 2] = np.clip(frame[..., 2] * 1.2, 0, 255)
        return winter_frame

    def transform(self, frame):
        if self.selected_filter == "Cartoon Effect":
            processed_frame = self.cartoon_effect(frame)
        elif self.selected_filter == "Gray Effect":
            processed_frame = self.greyscale(frame)
        elif self.selected_filter == "Sepia Effect":
            processed_frame = self.sepia(frame)
        elif self.selected_filter == "Pencil Sketch":
            processed_frame = self.pencil_sketch_grey(frame)
        elif self.selected_filter == "Invert Effect":
            processed_frame = self.invert(frame)
        elif self.selected_filter == "Summer":
            processed_frame = self.summer(frame)
        elif self.selected_filter == "Winter":
            processed_frame = self.winter(frame)
        else:
            processed_frame = np.copy(frame)

        processed_frame = self.blur_image(processed_frame, self.blur_rate)
        processed_frame = self.brighten_image(processed_frame, self.brightness_amount)

        if self.apply_enhancement_filter:
            processed_frame = self.enhance_details(processed_frame)

        # Convert the processed frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))

        # Create a BytesIO object to hold the image data
        image_stream = io.BytesIO()
        pil_image.save(image_stream, format="JPEG")

        # Rewind the stream to the beginning
        image_stream.seek(0)

        # Return the image stream
        return image_stream


def main():
    st.title("Video Editor")
    st.subheader("You can edit and apply filters to your videos!")

    filters = {
        "None": "No filter applied",
        "Cartoon Effect": "Apply a cartoon effect to the video",
        "Gray Effect": "Convert the video to grayscale",
        "Sepia Effect": "Apply a sepia tone effect to the video",
        "Pencil Sketch": "Create a pencil sketch effect",
        "Invert Effect": "Invert the colors of the video",
        "Summer": "Apply a summer color effect",
        "Winter": "Apply a winter color effect"
    }

    selected_filter = st.sidebar.selectbox("Filters", list(filters.keys()))
    filter_tooltip = filters[selected_filter]
    st.sidebar.text(filter_tooltip)

    blur_rate = st.sidebar.slider("Blurring", min_value=0.5, max_value=3.5)
    brightness_amount = st.sidebar.slider("Brightness", min_value=-50, max_value=50, value=0)
    apply_enhancement_filter = st.sidebar.checkbox('Enhance Details')

    uploaded_file = st.file_uploader("Upload a video", type=["mp4"])

    if uploaded_file is not None:
        # Read the video file using OpenCV
        video_bytes = uploaded_file.read()
        video_np = np.asarray(bytearray(video_bytes), dtype=np.uint8)
        video_cv = cv2.imdecode(video_np, cv2.IMREAD_UNCHANGED)

        # Create a VideoTransformer instance
        video_transformer = VideoTransformer()
        video_transformer.selected_filter = selected_filter
        video_transformer.blur_rate = blur_rate
        video_transformer.brightness_amount = brightness_amount
        video_transformer.apply_enhancement_filter = apply_enhancement_filter

        # Process the video frames
        processed_frames = []
        for frame in video_transformer.transform_video(video_cv):
            processed_frames.append(frame)

        # Create an output video path
        output_video_path = "output.mp4"

        # Save the processed frames as a new video
        video_transformer.save_video(processed_frames, output_video_path)

        # Display the output video
        st.subheader("Processed Video")
        video_file = open(output_video_path, "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)

        # Display a success message
        st.success("Video processing complete!")


if __name__ == '__main__':
    main()
