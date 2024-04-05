import tkinter as tk


import tkinter as tk
import mysql.connector
from tkinter import messagebox

# Function to fetch data from the database and display it
# main.py
import tkinter as tk
from tkinter import messagebox
from database import get_connection, close_connection

def fetch_and_display_data():
    # Fetch data from the database
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Movies")
        data = cursor.fetchall()
        # Format the records into a string to display
        output = "\n".join([f"Item ID: {row[0]}, Item Name: {row[1]}, Cost: {row[2]:.2f}" for row in data])
        # Display the formatted string in a messagebox
        messagebox.showinfo("Concessions Data", output)
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            close_connection(conn)

# Set up the main application window
root = tk.Tk()
root.title("Concessions Data Display")
root.geometry("300x200")

# Add a button to the window, which will call the data-fetching function
button = tk.Button(root, text="Show Concessions Data", command=fetch_and_display_data)
button.pack(pady=20)

# Start the application
root.mainloop()




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
