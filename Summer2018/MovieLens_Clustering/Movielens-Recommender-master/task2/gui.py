from Tkinter import *
import tkMessageBox

import numpy as np
import pandas as pd
import CF as ur
import random


#
# Configurations
#
# Name of the CSV file containing user's ratings data
RATINGS_DATA = "Rating Zeros.csv"
# Name of the CSV file containinng movies data
MOVIES_DATA = "Items.csv"
# Total number of movies
# (the dataset contains 1682 movies, that takes long time to compute
# the similarity, choose smaller number of movies for faster computation)
TOTAL_MOVIES = 100
# ID of the user to be tested
USER_ID = 1
# Number of movies for ratings
NUM_MOVIES = 5


class GUI:
    """
    Implement a user interface for the movie recommender system.
    The GUI allows user to input a user id to find the top 5 recommended
    movies based on user's rating data.
    """

    def __init__(self):
        """Create and start the GUI"""

        # member variables used in the GUI
        self.rating_vars = []
        self.result_list = None     # list box to display result
        self.ratings = None         # ratings data
        self.movie_names = None     # movies data
        self.chosen_movies = None   # list of pickup movies for rating
        self.sim_mat = None         # similarity matrix

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

        # Top panel that includes an entry for input ratings
        top_panel = Frame(frame)
        top_panel.pack(side=TOP, fill=X)

        Label(top_panel, text="Please rate below movies (value 1-5):").pack(side=TOP)

        # randomly choose five movies
        self.chosen_movies = [random.randrange(len(self.movie_names))
                              for _ in range(NUM_MOVIES)]

        for idx in self.chosen_movies:
            row = Frame(top_panel)
            row.pack(side=TOP, fill=X, expand=True)

            var = IntVar()
            var.set(5)

            Label(row, text=self.movie_names[idx]).pack(side=LEFT)
            Entry(row, textvariable=var, width=10).pack(side=RIGHT)

            self.rating_vars.append(var)

        # Button - Click to find the recommended movies
        Button(top_panel, text="Submit",
               command=self.find_movies).pack(side=BOTTOM)

        # Result panel that shows recommended movies based on user rating
        result_panel = Frame(frame)
        result_panel.pack(side=TOP, fill=BOTH, expand=True)

        Label(result_panel, text="Movies you may like:").pack(side=TOP)

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
        ratings = np.array(pd.read_csv(RATINGS_DATA, index_col=0))
        # use subset of movies
        self.ratings = ratings[:,:TOTAL_MOVIES]

        # movies information
        items = pd.read_csv(MOVIES_DATA, index_col=0)
        self.movie_names = items.Name[:TOTAL_MOVIES]

        # pre-compute the similarity matrix
        print "Computing ratings similarity matrix..."
        self.sim_mat = ur.getsim(self.ratings)

    def find_movies(self):
        # Get user input rating, make sure it is a valid number
        try:
            for var in self.rating_vars:
                r = var.get()
                if r < 1 or r > 5:
                    raise ValueError

        except ValueError:
            tkMessageBox.showerror("Input Error", "Please enter a number 1-5 for ratings")
            return

        # clear the previous result
        self.result_list.delete(0, END)

        try:
            # call the function provided by the recommender system to get
            # the top recommended movies

            for idx, var in zip(self.chosen_movies, self.rating_vars):
                self.ratings[USER_ID][idx] = var.get()

            movies = ur.recommend(self.ratings, USER_ID, self.sim_mat, NUM_MOVIES)

            # display the returned movies in the listbox
            for idx, rating in movies:
               self.result_list.insert(END, self.movie_names[idx + 1])

        except Exception as e:
            # Handle any unexpected error thrown by the recommender system
            tkMessageBox.showerror("Unexpected Error", e)


if __name__ == '__main__':
    GUI()