import tkinter as tk
from tkinter import filedialog
from ui import ImageProcessingApp  # Assuming your UI script is named ui.py
from image_processing import load_image  # Assuming your image processing script is named image_processing.py
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pipeline import ProcessingPipeline

class ExtendedImageProcessingApp(ImageProcessingApp):
    def open_file(self):
        initial_dir = os.getcwd()  # Get the current working directory
        file_path = filedialog.askopenfilename(initialdir=initial_dir,
                                               filetypes=[("Image files", "*.png *.jpg *.jpeg *.tif *.tiff")])
        if not file_path:  # If no file is selected
            return

        # Load the image using image processing function
        image = load_image(file_path)

        self.pipeline.load_image_image(image)  # Update the pipeline with the new image

        # Update both image displays
        self.update_image_display(self.left_canvas, image)
        self.update_image_display(self.right_canvas, image)

        # Update the filename entries
        self.working_filename_var.set(file_path)
        self.output_filename_var.set(file_path)

    def update_image_display(self, canvas, image):
        # Get the figure associated with the canvas
        figure = canvas.figure
        # Clear the current figure to prepare for the new image
        figure.clf()

        # Create a new axes object on the figure
        ax = figure.add_subplot(111)
        # Display the image on the axes
        ax.imshow(image, cmap='gray', aspect='auto')  # 'aspect' parameter makes the image fill the axes
        # Hide the axes
        ax.axis('off')

        # Adjust subplot parameters to minimize whitespace
        figure.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

        # Redraw the canvas with the new image
        canvas.draw()

    def process(self):
        # Get the parameters from the entry widgets
        blur_kernel_size = int(self.variable_entries['blur_kernel_size'].get())
        brightness_offset = int(self.variable_entries['brightness_offset'].get())
        gaussian_blur = int(self.variable_entries['gaussian_blur'].get())
        threshold = int(self.variable_entries['threshold'].get())
        morph_open = int(self.variable_entries['morph_open'].get())
        alpha = float(self.variable_entries['alpha'].get())
        size_threshold = int(self.variable_entries['size_threshold'].get())
        connectivity = int(self.variable_entries['connectivity'].get())

        # Run the pipeline with the given parameters
        self.pipeline.run_pipeline(self.working_filename_var.get(), blur_kernel_size, brightness_offset, gaussian_blur,
                                   threshold, morph_open, alpha, size_threshold, connectivity)

        # Update the image displays with the processed images
        self.update_image_display(self.left_canvas, self.pipeline.get_stage_output('original_with_dots'))
        self.update_image_display(self.right_canvas, self.pipeline.get_stage_output('dots_counted'))

        # Update the dot count label
        self.count_text.set(f'Dot count: {self.pipeline.dot_count}')



if __name__ == '__main__':
    # create an instance of the processing pipeline
    pipeline = ProcessingPipeline()

    app = ExtendedImageProcessingApp(pipeline)
    app.mainloop()
