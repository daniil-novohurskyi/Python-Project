from tkinter import ttk


class TableFrame(ttk.Frame):
    """
    A Tkinter frame for displaying and sorting a pandas DataFrame in a treeview widget.

    Attributes:
        dataframe (DataFrame): The pandas DataFrame to be displayed.
        sort_column (str): The currently selected column for sorting.
        sort_reverse (bool): The sorting order (True for descending, False for ascending).

    Methods:
        create_widgets():
            Creates and arranges the widgets in the frame.
        update_treeview(dataframe):
            Updates the treeview with the data from the given DataFrame.
        sort_by_column(column):
            Sorts the DataFrame by the specified column and updates the treeview.
    """

    def __init__(self, parent, dataframe):
        """
        Initializes the TableFrame instance.

        Args:
            parent (tk.Widget): The parent widget to which this frame belongs.
            dataframe (DataFrame): The pandas DataFrame to be displayed.
        """
        super().__init__(parent)
        # Initialize attributes for widgets and data
        self.scrollbar = None
        self.treeview_data = None
        self.tree = None
        self.tree_frame = None
        self.frame = None
        self.dataframe = dataframe
        self.sort_column = None
        self.sort_reverse = False

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the widgets in the frame.
        """
        # Create a main frame for layout
        self.frame = ttk.Frame(self)
        self.frame.pack(fill="both", expand=True)

        # Drop the 'Year' column from the dataframe (if present)
        self.dataframe = self.dataframe.drop("Year", axis=1, errors='ignore')

        # Create a frame for the treeview widget
        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.grid(row=0, column=0, sticky="nsew")

        # Create the treeview widget with headings from dataframe columns
        self.tree = ttk.Treeview(self.tree_frame, columns=list(self.dataframe.columns), show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Configure column headings and sorting behavior
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column, command=lambda col=column: self.sort_by_column(col))
            self.tree.column(column, width=100, anchor="center")

        # Configure row colors (alternating colors)
        self.tree.tag_configure('oddrow', background='lightgray')
        self.tree.tag_configure('evenrow', background='white')

        # Initialize treeview data list and update it with dataframe rows
        self.treeview_data = []
        self.update_treeview(self.dataframe)

        # Add a vertical scrollbar to the treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Configure grid layout to expand the frame with the window
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

    def update_treeview(self, dataframe):
        """
        Updates the treeview with the data from the given DataFrame.

        Args:
            dataframe (DataFrame): The pandas DataFrame containing the data to be displayed.
        """
        # Clear existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add new data to the treeview
        self.treeview_data = []
        for index, row in dataframe.iterrows():
            tag = 'evenrow' if len(self.treeview_data) % 2 == 0 else 'oddrow'
            # Insert row values into the treeview with alternating row colors
            self.treeview_data.append(self.tree.insert("", "end", values=list(row), tags=(tag,)))

    def sort_by_column(self, column):
        """
        Sorts the DataFrame by the specified column and updates the treeview.

        Args:
            column (str): The column name to sort by.
        """
        # Toggle the sort order if the same column is selected again
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        self.sort_column = column

        # Sort the DataFrame based on selected column and order
        self.dataframe = self.dataframe.sort_values(by=column, ascending=not self.sort_reverse).reset_index(drop=True)

        # Update the treeview with sorted data
        self.update_treeview(self.dataframe)
