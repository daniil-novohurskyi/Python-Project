import tkinter as tk
from tkinter import ttk


class FrameManager(tk.Tk):
    """
    Manages multiple frames within a tkinter application.

    Attributes:
        frames (dict): Dictionary storing instances of frames associated with their classes.

    Methods:
        add_frame(frame_class, *args):
            Adds a frame to the application.

        show_frame(frame_class):
            Raises the selected frame to the top for display.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the FrameManager instance.

        Args:
            *args: Positional arguments passed to the tk.Tk initializer.
            **kwargs: Keyword arguments passed to the tk.Tk initializer.
        """
        super().__init__(*args, **kwargs)

        # Create a container frame that will hold all other frames
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Create a separate frame for buttons at the bottom
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x")

        # Dictionary to store instances of frames associated with their classes
        self.frames = {}

        # Configure grid weights for the container frame
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

    def add_frame(self, frame_class, *args):
        """
        Adds a frame to the application.

        Args:
            frame_class (class): The class of the frame to be added.
            *args: Positional arguments to be passed to the frame's initializer.
        """
        # Create an instance of the specified frame class
        frame = frame_class(self.container, *args)

        # Store the frame instance in the frames dictionary
        self.frames[frame_class] = frame

        # Use grid layout to place the frame in the container
        frame.grid(row=0, column=0, sticky="nsew")

        # Create a button in the button frame to show this frame
        button = ttk.Button(self.button_frame, text=frame_class.__name__,
                            command=lambda fc=frame_class: self.show_frame(fc))
        button.pack(side="left", fill="x", expand=True)

    def show_frame(self, frame_class):
        """
        Raises the selected frame to the top for display.

        Args:
            frame_class (class): The class of the frame to be shown.
        """
        # Retrieve the frame instance from the frames dictionary
        frame = self.frames[frame_class]

        # Raise the selected frame above all others for display
        frame.tkraise()
