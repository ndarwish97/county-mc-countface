# pipeline.py
import cv2
import numpy as np
from image_processing import (load_image, correct_illumination, apply_filters,
                              adjust_contrast, count_dots)
import matplotlib.pyplot as plt

class ProcessingPipeline:
    def __init__(self):
        self.images = {
            'original': None,
            'corrected': None,
            'filtered': None,
            'contrast': None,
            'dots_counted': None,
            'original_with_dots': None
        }
        self.dot_count = None
        self.centroids = None

    def clear_pipeline(self):
        self.images = {
            'original': None,
            'corrected': None,
            'filtered': None,
            'contrast': None,
            'dots_counted': None,
            'original_with_dots': None
        }
        self.dot_count = None
        self.centroids = None

    def load_image_image(self, image):
        self.images['original'] = image

    def load_image_filepath(self, file_path):
        self.images['original'] = load_image(file_path)

    def correct_illumination(self, blur_kernel_size, brightness_offset=30):
        self.images['corrected'] = correct_illumination(self.images['original'], blur_kernel_size, brightness_offset)

    def apply_filters(self, gaussian_blur, threshold, morph_open):
        filter_params = {
            'gaussian_blur': gaussian_blur,
            'threshold': threshold,
            'morph_open': morph_open
        }
        self.images['filtered'] = apply_filters(self.images['corrected'], filter_params)

    def adjust_contrast(self, alpha):
        self.images['contrast'] = adjust_contrast(self.images['filtered'], alpha)

    def count_dots(self, size_threshold, connectivity):
        self.dot_count, self.images['dots_counted'], self.images['original_with_dots'], self.centroids = count_dots(
            self.images['original'], self.images['contrast'], size_threshold, connectivity
        )

    def get_stage_output(self, stage):
        return self.images.get(stage, None)

    def run_pipeline(self, file_path, blur_kernel_size, brightness_offset, gaussian_blur, threshold, morph_open, alpha, size_threshold, connectivity):
        self.load_image_filepath(file_path)
        self.correct_illumination(blur_kernel_size, brightness_offset)
        self.apply_filters(gaussian_blur, threshold, morph_open)
        self.adjust_contrast(alpha)
        self.count_dots(size_threshold, connectivity)


if __name__ == "__main__":
    # Example usage of the ProcessingPipeline class

    # Define the parameters for each stage
    file_path = '../images/sample_images/D8-1.tif'
    blur_kernel_size = 101
    brightness_offset = 30
    gaussian_blur = 5
    threshold = 127
    morph_open = 3
    alpha = 1.5
    size_threshold = 25
    connectivity = 4

    # Create an instance of the ProcessingPipeline
    pipeline = ProcessingPipeline()

    # Run the pipeline
    pipeline.run_pipeline(file_path, blur_kernel_size, brightness_offset, gaussian_blur, threshold, morph_open, alpha, size_threshold, connectivity)

    # Access and display the results
    print(f"Dot count: {pipeline.dot_count}")
    # You would normally use a plotting library or an image display function here
    # For example:
    plt.imshow(pipeline.get_stage_output('contrast'), cmap='gray')
    plt.show()
