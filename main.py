import tkinter as tk

class MovieTicketApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Ticket Booking")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight())) # Full screen

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Movie Posters
        self.movie_posters_frame = tk.Frame(self.main_frame)
        self.movie_posters_frame.pack(expand=True, fill=tk.BOTH)

        # Movie Posters
        self.poster1 = tk.Label(self.movie_posters_frame, text="Movie Poster 1")
        self.poster1.pack(side=tk.LEFT, padx=20, pady=20)
        self.poster2 = tk.Label(self.movie_posters_frame, text="Movie Poster 2")
        self.poster2.pack(side=tk.LEFT, padx=20, pady=20)
        self.poster3 = tk.Label(self.movie_posters_frame, text="Movie Poster 3")
        self.poster3.pack(side=tk.LEFT, padx=20, pady=20)
        self.poster4 = tk.Label(self.movie_posters_frame, text="Movie Poster 4")
        self.poster4.pack(side=tk.LEFT, padx=20, pady=20)

        # Buttons to Get Tickets
        self.ticket_button = tk.Button(self.main_frame, text="Get Tickets", command=self.show_ticket_screen)
        self.ticket_button.pack()

        # Bottom Tab for Concessions
        self.concession_button = tk.Button(self, text="Concessions", command=self.show_concession_screen)
        self.concession_button.pack(side=tk.BOTTOM)

        # Receipt in Bottom Right Corner
        self.receipt_label = tk.Label(self, text="Receipt")
        self.receipt_label.pack(side=tk.RIGHT, anchor=tk.SE)

    def show_ticket_screen(self):
        # Code to open a new screen to enter customer information
        pass

    def show_concession_screen(self):
        # Code to change the screen to concessions
        pass

if __name__ == "__main__":
    app = MovieTicketApp()
    app.mainloop()
