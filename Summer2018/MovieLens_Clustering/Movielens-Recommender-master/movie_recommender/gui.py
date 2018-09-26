from Tkinter import *
import tkMessageBox

import numpy as np
import pandas as pd
import CF as ur


#
# Configurations
#
# Name of the CSV file containing user's ratings data
RATINGS_DATA = "Rating Zeros.csv"
# Name of the CSV file containinng movies data
MOVIES_DATA = "Items.csv"


class GUI:
    """
    Implement a user interface for the movie recommender system.
    The GUI allows user to input a user id to find the top 5 recommended
    movies based on user's rating data.
    """

    def __init__(self):
        """Create and start the GUI"""

        # member variables used in the GUI
        self.user_id_var = None     # input user id
        self.result_list = None     # list box to display result
        self.ratings = None         # ratings data
        self.movie_names = None     # movies data

        # load ratings and moves data from the corresponding files
        self._load_data()
        # create and start running the GUI
        self._create_gui()

    def _create_gui(self):
        """
        Create the user interface which includes an entry for user input
        a user id, a button to click to find recommended movies, and
        a list box to display the result
        """

        # The TK's root that manages the GUI
        root = Tk()
        root.title("Movie Recommender System")

        # Create the frame for the main window
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Top panel that includes an entry for input user id
        top_panel = Frame(frame)
        top_panel.pack(side=TOP, fill=X)

        Label(top_panel, text="User ID:").pack(side=LEFT)

        # Entry for input user id which is stored in 'user_id_var'
        self.user_id_var = IntVar()
        self.user_id_var.set(1)
        Entry(top_panel, textvariable=self.user_id_var,
              width=10).pack(side=LEFT)

        # Button - Click to find the recommended movies
        Button(top_panel, text="Find Movies",
               command=self.find_movies).pack(side=RIGHT)

        # The panel to shows the result
        result_panel = Frame(frame)
        result_panel.pack(side=TOP, fill=BOTH, expand=True)

        Label(result_panel, text="Top 5 Recommended Movies").pack(side=TOP)

        # The list box that shows the result
        self.result_list = Listbox(result_panel, height=8)
        self.result_list.pack(side=LEFT, fill=BOTH, expand=True)

        # run the GUI
        root.mainloop()

    def _load_data(self):
        """
        Load ratings and movies data in the files whose names are set in
        variables RATINGS_DATA and MOVIES_DATA
        """
        # row: users  col: movies
        self.ratings = np.array(pd.read_csv(RATINGS_DATA, index_col=0))

        # movies information
        items = pd.read_csv(MOVIES_DATA, index_col=0)
        self.movie_names = items.Name

    def find_movies(self):
        """
        Callback for "Find" button.
        Call the functions provided by the CF module to find recommended
        movies for a user. The returned result is shown in the list box
        """

        # Get user input User ID, make sure it is a valid number
        try:
            user_id = self.user_id_var.get()
        except ValueError:
            tkMessageBox.showerror("Input Error", "Please enter a number as User ID")
            return

        # clear the previous result
        self.result_list.delete(0, END)

        try:
            # call the function provided by the recommender system to get
            # the top recommended movies
            movies = ur.getmemovies(self.ratings, user_id, self.movie_names)

            # display the returned movies in the listbox
            for item in movies:
                self.result_list.insert(END, item)

        except IndexError:
            # Invalid user id that runs out of index of the data
            tkMessageBox.showerror("Input Error", "Invalid User ID")
        except Exception as e:
            # Handle any unexpected error thrown by the recommender system
            tkMessageBox.showerror("Unexpected Error", e)


if __name__ == '__main__':
    GUI()