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


def count_dots(image, size_threshold, connectivity=4):
    """
    Count the number of dots in the image based on a size threshold and mark them with a red dot.

    :param image: numpy.ndarray, the image to process.
    :param size_threshold: int, size threshold for considering a white area a dot.
    :param connectivity: int, connectivity criteria (4 or 8) for the blobs.
    :return: int, the number of dots counted, and the image with red dots marked.
    """
    # Ensure the image is binary
    _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Find connected components (blobs)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity, cv2.CV_32S)

    # Create an output image to draw red dots on
    output_image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2BGR)

    # Count dots and draw red dots on the output image
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
            # Draw a red dot (3x3 pixels)
            cv2.rectangle(output_image, (center_x - 1, center_y - 1), (center_x + 1, center_y + 1), (0, 0, 255), -1)

    return num_dots, output_image



if __name__ == "__main__":
    # Example calls for debugging
    img_path = '../images/sample_images/D8-1.tif'
    img = load_image(img_path)

    # label the plot with the image name
    plt.title(img_path)
    plt.imshow(img, cmap='gray')
    plt.show()
    plt.clf()

    filter_parameters = {
        'gaussian_blur': 5,  # Kernel size for Gaussian Blur
        'threshold': 127,  # Threshold value for binary threshold
        'morph_open': 3  # Kernel size for Morphological Opening
    }

    filtered_img = apply_filters(img, filter_parameters)

    # label the plot with the image name and filter parameters
    plt.title(f"{img_path} - Filtered")
    plt.imshow(filtered_img, cmap='gray')
    plt.show()
    plt.clf()

    # Contrast adjustment parameters
    alpha = 1.5  # Example value to increase contrast
    contrast_img = adjust_contrast(filtered_img, alpha)

    # label the plot with the image name and contrast level
    plt.title(f"{img_path} - Contrast Adjusted")
    plt.imshow(contrast_img, cmap='gray')
    plt.show()
    plt.clf()

    # Dot counting parameters
    size_threshold = 10  # Example value to determine minimum dot size
    dot_count, marked_image = count_dots(contrast_img, size_threshold)

    # label the plot with the image name and dot count
    plt.title(f"{img_path} - Dot Count: {dot_count}")
    plt.imshow(marked_image)
    plt.show()
    plt.clf()


    print(f"Dot count: {dot_count}")
