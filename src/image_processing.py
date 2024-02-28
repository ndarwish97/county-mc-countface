import cv2
import numpy as np
from matplotlib import pyplot as plt


def load_image(file_path):
    """
    Load an image from the specified file path.

    :param file_path: str, the path to the image file.
    :return: image as a numpy array.
    """
    with open(file_path, 'rb') as f:
        img = cv2.imread(file_path, 0)

    return img


def correct_illumination(image, blur_kernel_size, brightness_offset=30):
    """
    Correct uneven illumination in an image and increase brightness.

    :param image: numpy.ndarray, the image to process.
    :param blur_kernel_size: int, size of the kernel used for background estimation.
    :param brightness_offset: int, value to add to each pixel to increase brightness.
    :return: Illumination corrected and brightness adjusted image as a numpy array.
    """
    # Estimate the background by blurring the image
    background = cv2.GaussianBlur(image, (blur_kernel_size, blur_kernel_size), 0)

    # Subtract the background from the original image
    corrected_image = cv2.subtract(image, background)

    # Normalize the image to the range [0, 255]
    corrected_image = cv2.normalize(corrected_image, None, 0, 255, cv2.NORM_MINMAX)

    # Increase the brightness by adding an offset value to each pixel
    corrected_image = cv2.convertScaleAbs(corrected_image, alpha=1, beta=brightness_offset)

    return corrected_image



def apply_filters(image, filter_params):
    """
    Apply filters to the image based on the given parameters.

    :param image: numpy.ndarray, the image to filter.
    :param filter_params: dict, parameters for the filters.
    :return: filtered image as a numpy array.
    """
    # Gaussian Blur
    if 'gaussian_blur' in filter_params:
        kernel_size = filter_params['gaussian_blur']
        image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    # Thresholding
    if 'threshold' in filter_params:
        _, image = cv2.threshold(image, filter_params['threshold'], 255, cv2.THRESH_BINARY)

    # Morphological Opening
    if 'morph_open' in filter_params:
        kernel_size = filter_params['morph_open']
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    return image


def adjust_contrast(image, alpha):
    """
    Adjust the contrast of the image by multiplying by alpha value and then adding a beta value to increase brightness if necessary.

    :param image: numpy.ndarray, the image to adjust.
    :param alpha: float, the factor by which to scale the contrast (1.0 means no change).
    :return: contrast adjusted image as a numpy array.
    """
    # New image = alpha * original image + beta
    # Here, we'll set beta to 0 because we only want to adjust contrast, not brightness
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
    return adjusted


def count_dots(original_image, processed_image, size_threshold, connectivity=4):
    """
    Count the number of dots in the processed image based on a size threshold and mark them on both
    the processed image and the original image.

    :param original_image: numpy.ndarray, the original image to overlay dots on.
    :param processed_image: numpy.ndarray, the processed image used to count dots.
    :param size_threshold: int, size threshold for considering a white area a dot.
    :param connectivity: int, connectivity criteria (4 or 8) for the blobs.
    :return: tuple(int, numpy.ndarray, numpy.ndarray), the number of dots counted,
             the processed image with red dots marked, and the original image with red dots marked.
    """
    # Ensure the processed image is binary
    _, binary = cv2.threshold(processed_image, 127, 255, cv2.THRESH_BINARY)

    # Find connected components (blobs)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity, cv2.CV_32S)

    # Create an output image to draw red dots on (processed image)
    count_image = cv2.cvtColor(processed_image.copy(), cv2.COLOR_GRAY2BGR)

    # Create a copy of the original image to draw red dots on
    if len(original_image.shape) == 2:
        # If the original image is grayscale, convert it to BGR
        original_colored = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    else:
        # Otherwise, make a copy of the original
        original_colored = original_image.copy()

    # Count dots and draw red dots on both output images
    num_dots = 0
    for i, stat in enumerate(stats):
        # Skip the first component, which is the background
        if i == 0:
            continue

        area = stat[cv2.CC_STAT_AREA]
        if area >= size_threshold:
            num_dots += 1
            # Get the centroid for the component
            center_x = int(centroids[i][0])
            center_y = int(centroids[i][1])
            # Draw a red dot (3x3 pixels) on both images
            cv2.rectangle(count_image, (center_x - 1, center_y - 1), (center_x + 1, center_y + 1), (255, 0, 0), -1)
            cv2.rectangle(original_colored, (center_x - 1, center_y - 1), (center_x + 1, center_y + 1), (255, 0, 0), -1)

    return num_dots, count_image, original_colored


if __name__ == "__main__":
    # Example calls for debugging
    img_path = '../images/sample_images/D8-1.tif'
    img = load_image(img_path)

    # Retrieve image dimensions
    height, width = img.shape[:2]

    # Create a figure with a size that has the same aspect ratio as the image
    # and a DPI that makes the figure large enough to encompass the full resolution of the image.
    # You may adjust the scale factor as needed.
    scale_factor = 1  # Adjust this factor to scale the figure size
    fig_size = (width / float(100 * scale_factor),
                height / float(100 * scale_factor))  # Dividing by 100 because the default DPI is 100
    plt.figure(figsize=fig_size, dpi=100 * scale_factor)  # Adjusting the DPI based on the scale factor

    # label the plot with the image name
    plt.title(img_path)
    plt.imshow(img, cmap='gray')
    plt.show()
    plt.clf()

    # Image correction parameters
    blur_kernel_size = 101  # Example value, adjust as needed
    brightness_offset = 100  # Example value, adjust as needed
    corrected_img = correct_illumination(img, blur_kernel_size, brightness_offset)

    # label the plot with the image name and correction method
    plt.figure(figsize=fig_size, dpi=100 * scale_factor)
    plt.title(f"{img_path} - Corrected")
    plt.imshow(corrected_img, cmap='gray')
    plt.show()
    plt.clf()

    filter_parameters = {
        'gaussian_blur': 5,  # Kernel size for Gaussian Blur
        'threshold': 127,  # Threshold value for binary threshold
        'morph_open': 3  # Kernel size for Morphological Opening
    }

    filtered_img = apply_filters(corrected_img, filter_parameters)

    # label the plot with the image name and filter parameters
    plt.figure(figsize=fig_size, dpi=100 * scale_factor)
    plt.title(f"{img_path} - Filtered")
    plt.imshow(filtered_img, cmap='gray')
    plt.show()
    plt.clf()

    # Contrast adjustment parameters
    alpha = 1.5  # Example value to increase contrast
    contrast_img = adjust_contrast(filtered_img, alpha)

    # label the plot with the image name and contrast level
    plt.figure(figsize=fig_size, dpi=100 * scale_factor)
    plt.title(f"{img_path} - Contrast Adjusted")
    plt.imshow(contrast_img, cmap='gray')
    plt.show()
    plt.clf()

    # Dot counting parameters
    size_threshold = 25  # Example value to determine minimum dot size
    dot_count, count_img, original_with_dots = count_dots(img, contrast_img, size_threshold)

    # label the plot with the image name and dot count
    plt.figure(figsize=fig_size, dpi=100 * scale_factor)
    plt.title(f"{img_path} - Dot Count: {dot_count}")
    plt.imshow(count_img)
    plt.show()
    plt.clf()

    # label the plot with the image name and dot count
    plt.figure(figsize=fig_size, dpi=100 * scale_factor)
    plt.title(f"{img_path} - Dot Count: {dot_count}")
    plt.imshow(original_with_dots)
    plt.show()
    plt.clf()


    print(f"Dot count: {dot_count}")
