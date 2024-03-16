import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pipeline import ProcessingPipeline

class ImageProcessingApp(tk.Tk):
    def __init__(self, pipeline):
        super().__init__()
        self.title('Image Processing Application')

        # Create an instance of the ProcessingPipeline class
        self.pipeline = pipeline

        self.title('County-mc-Countface')

        # Setup frames
        self.setup_frames()

        # Setup components
        self.setup_components()

    def setup_frames(self):
        self.image_frame = tk.Frame(self)
        self.image_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=0, column=2, sticky='ns')

        self.filename_frame = tk.Frame(self)
        self.filename_frame.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

    def setup_components(self):
        # Image display slots
        self.setup_image_slot(self.image_frame, 'Pipeline Image 1', row=0, column=0)
        self.setup_image_slot(self.image_frame, 'Pipeline Image 2', row=0, column=1)

        # Control buttons and variables
        self.open_file_button = tk.Button(self.control_frame, text='Open File', command=self.open_file)
        self.open_file_button.pack()

        # Variable grid setup for processing parameters
        self.variable_entries = {}

        # Dictionary of parameter names and their default values
        self.parameters = {
            'blur_kernel_size': '101',
            'brightness_offset': '100',
            'gaussian_blur': '5',
            'threshold': '127',
            'morph_open': '3',
            'alpha': '1.5',
            'size_threshold': '25',
            'connectivity': '4'
            # Add more parameters as needed
        }

        for i, (param_name, default_value) in enumerate(self.parameters.items()):
            var_label = tk.Label(self.control_frame, text=param_name.replace('_', ' ').capitalize())
            var_label.pack()
            var_entry = tk.Entry(self.control_frame)
            var_entry.insert(0, default_value)  # Set default value
            var_entry.pack()
            self.variable_entries[param_name] = var_entry

        self.process_button = tk.Button(self.control_frame, text='Process', command=self.process)
        self.process_button.pack()

        self.open_matplotlib_button = tk.Button(self.control_frame, text='Open in Matplotlib', command=self.open_in_matplotlib)
        self.open_matplotlib_button.pack()

        self.save_button = tk.Button(self.control_frame, text='Save', command=self.save)
        self.save_button.pack()

        self.log_button = tk.Button(self.control_frame, text='Log', command=self.log)
        self.log_button.pack()

        # Filename entries
        self.working_filename_var = tk.StringVar()
        self.working_filename_entry = tk.Entry(self.filename_frame, textvariable=self.working_filename_var)
        self.working_filename_entry.grid(row=0, column=0, sticky='ew')
        self.output_filename_var = tk.StringVar()
        self.output_filename_entry = tk.Entry(self.filename_frame, textvariable=self.output_filename_var)
        self.output_filename_entry.grid(row=0, column=1, sticky='ew')
        self.filename_frame.grid_columnconfigure(0, weight=1)
        self.filename_frame.grid_columnconfigure(1, weight=1)

        # Additional control buttons and statistics display
        self.histogram_button = tk.Button(self.control_frame, text='Distance Histogram', command=self.open_histogram)
        self.histogram_button.pack()

        # Output statistics labels and text
        self.stats_frame = tk.LabelFrame(self.control_frame, text='Output Statistics')
        self.stats_frame.pack(fill=tk.X, expand=True)

        self.bad_data_label = tk.Label(self.stats_frame, text='% Image Bad Data:')
        self.bad_data_label.pack()
        self.bad_data_text = tk.StringVar()
        self.bad_data_entry = tk.Entry(self.stats_frame, textvariable=self.bad_data_text, state='readonly')
        self.bad_data_entry.pack()

        self.count_label = tk.Label(self.stats_frame, text='Count:')
        self.count_label.pack()
        self.count_text = tk.StringVar()
        self.count_entry = tk.Entry(self.stats_frame, textvariable=self.count_text, state='readonly')
        self.count_entry.pack()

        self.polymer_count_label = tk.Label(self.stats_frame, text='Count Polymers:')
        self.polymer_count_label.pack()
        self.polymer_count_text = tk.StringVar()
        self.polymer_count_entry = tk.Entry(self.stats_frame, textvariable=self.polymer_count_text, state='readonly')
        self.polymer_count_entry.pack()

        self.avg_polymer_length_label = tk.Label(self.stats_frame, text='Average Polymer Length:')
        self.avg_polymer_length_label.pack()
        self.avg_polymer_length_text = tk.StringVar()
        self.avg_polymer_length_entry = tk.Entry(self.stats_frame, textvariable=self.avg_polymer_length_text,
                                                 state='readonly')
        self.avg_polymer_length_entry.pack()

    def setup_image_slot(self, parent, title, row, column):
        # Create a LabelFrame widget as a container for the plot and radiobuttons
        frame = tk.LabelFrame(parent, text=title)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)
        parent.grid_rowconfigure(0, weight=1)  # Assuming all image slots are in row 0

        # Create a matplotlib figure
        figure = plt.Figure(figsize=(5, 4))  # Adjust the size as needed
        # Create a canvas widget to embed the matplotlib figure
        canvas = FigureCanvasTkAgg(figure, frame)
        # Pack the canvas widget and fill the space in the GUI
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create a frame for the radiobuttons
        pips_frame = tk.Frame(frame)
        pips_frame.pack(fill=tk.X, expand=True)

        # Variable to store the selected stage for this slot
        selected_stage = tk.StringVar()
        selected_stage.set('original')  # Default to the original stage

        stages = ['original', 'corrected', 'filtered', 'contrast', 'dots_counted', 'original_with_dots']

        # Create radiobuttons for the processing stages
        for stage in stages:
            pip = tk.Radiobutton(
                pips_frame,
                text=stage.capitalize(),
                variable=selected_stage,
                value=stage,
                command=lambda s=stage, c=column: self.update_displayed_image(s, c)  # Command to execute on selection
            )
            pip.pack(side=tk.LEFT)

        # Save references to the figure, canvas, and selected_stage variable for later use
        if column == 0:
            self.left_figure = figure
            self.left_canvas = canvas
            self.left_selected_stage = selected_stage
        else:
            self.right_figure = figure
            self.right_canvas = canvas
            self.right_selected_stage = selected_stage

    def open_file(self):
        # Logic for opening a file and updating the working filename
        pass

    def process(self):
        # Logic for processing the image
        pass

    def open_in_matplotlib(self):
        # Logic for opening the image in an external Matplotlib window
        pass

    def save(self):
        # Logic for saving the current state
        pass

    def log(self):
        # Logic for logging actions or results
        pass

    def open_histogram(self):
        # Logic for opening the histogram in a Matplotlib window
        pass

    def update_displayed_image(self, stage, column):
        # Get the image for the selected stage from the pipeline
        image = self.pipeline.get_stage_output(stage)

        # Determine which canvas to update based on the column
        canvas_to_update = self.left_canvas if column == 0 else self.right_canvas

        # Call the method to update the image display
        self.update_image_display(canvas_to_update, image)

if __name__ == '__main__':
    # create an instance of the processing pipeline
    pipeline = ProcessingPipeline()

    app = ImageProcessingApp(pipeline)
    app.mainloop()
