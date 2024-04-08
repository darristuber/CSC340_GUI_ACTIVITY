import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from database import get_connection, close_connection

class MovieTicketApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Ticket Booking")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))  # Full screen

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Movie Posters Frame
        self.movie_posters_frame = tk.Frame(self.main_frame)
        self.movie_posters_frame.pack(expand=True, fill=tk.BOTH)

        # Load movie poster images
        self.load_movie_posters()

        # Button to Get Tickets
        self.ticket_button = tk.Button(self.main_frame, text="Get Tickets", command=self.show_ticket_screen)
        self.ticket_button.pack()

        # Button to Show Concessions Data
        self.concessions_button = tk.Button(self.main_frame, text="Show Concessions Data", command=self.fetch_and_display_data)
        self.concessions_button.pack()

        # Bottom Tab for Concessions
        self.concession_button = tk.Button(self, text="Concessions", command=self.show_concession_screen)
        self.concession_button.pack(side=tk.BOTTOM)

        # Receipt in Bottom Right Corner
        self.receipt_label = tk.Label(self, text="Receipt")
        self.receipt_label.pack(side=tk.RIGHT, anchor=tk.SE)

    def load_movie_posters(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT PosterImage FROM Movies")
            rows = cursor.fetchall()
            for row in rows:
                url = row[0]
                response = requests.get(url)
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(self.movie_posters_frame, image=photo)
                label.image = photo  # keep a reference!
                label.pack(side=tk.LEFT, padx=20, pady=20)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def fetch_and_display_data(self):
        """Fetch and display data from the database."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Movies")
            data = cursor.fetchall()
            output = "\n".join([f"Item ID: {row[0]}, Item Name: {row[1]}, Cost: {row[2]:.2f}" for row in data])
            messagebox.showinfo("Movies Data", output)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def show_ticket_screen(self):
        # Code to open a new screen to enter customer information
        pass

    def show_concession_screen(self):
        # Code to change the screen to concessions
        pass

if __name__ == "__main__":
    app = MovieTicketApp()
    app.mainloop()
