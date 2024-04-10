import tkinter as tk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.configure(bg='black')  # Set the background color to matte black

# To make the window full-screen
root.state('zoomed')  # For Windows

# Configure the style for the buttons
style = ttk.Style()
style.configure('TButton', background='white', foreground='black')
# root.attributes('-zoomed', True)  # For Linux
# root.wm_attributes('-fullscreen', 'true')  # For macOS

# Define a function to add items to the receipt
def add_to_receipt(item, quantity, item_type):
    receipt_text.insert(tk.END, f"{quantity} x {item} ({item_type}) added\n")
    receipt_text.configure(bg='black', fg='white')  # Set the text color to white



# Create the tab control
tabControl = ttk.Notebook(root)


# Define the creation of the tab content for Movies, Foods, and Drinks
def create_tab_content(tab, item_type, add_to_cart_callback):

    for i in range(4):  # Assuming you have 4 items per tab
        tab.columnconfigure(i, weight=1)
        # Banner
        banner = tk.Label(tab, text=f"{item_type} Banner {i + 1}", bg="grey", width=20, height=10)
        banner.grid(column=i, row=0, padx=10, pady=10, sticky='ew')

        # Dropdown to select times for movies, quantity for food and drinks
        if item_type == 'Movie':
            times_var = tk.StringVar()
            times_dropdown = ttk.Combobox(tab, textvariable=times_var, width=15)
            times_dropdown['values'] = ('Time 1', 'Time 2', 'Time 3')  # Add actual times here
            times_dropdown.grid(column=i, row=1, sticky='ew', padx=10)
        else:
            quantity_var = tk.IntVar(value=1)
            quantity_entry = ttk.Entry(tab, textvariable=quantity_var, width=5)
            quantity_entry.grid(column=i, row=1, sticky='ew', padx=10)

        # Add to cart button
        add_button = tk.Button(tab, text="Add to Cart", command=lambda i=i: add_to_cart_callback(i))
        add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)

def create_tab_content(tab, item_type, add_to_cart_callback):

    for i in range(4):  # Assuming you have 4 items per tab
        tab.columnconfigure(i, weight=1)
        # Banner
        banner = tk.Label(tab, text=f"{item_type} Banner {i + 1}", bg="grey", width=20, height=10)
        banner.grid(column=i, row=0, padx=10, pady=10, sticky='ew')

        # Dropdown to select times for movies, quantity for food and drinks
        if item_type == 'Movie':
            times_var = tk.StringVar()
            times_dropdown = ttk.Combobox(tab, textvariable=times_var, width=15)
            times_dropdown['values'] = ('Time 1', 'Time 2', 'Time 3')  # Add actual times here
            times_dropdown.grid(column=i, row=1, sticky='ew', padx=10)
        else:
            quantity_var = tk.IntVar(value=1)
            quantity_entry = ttk.Entry(tab, textvariable=quantity_var, width=5)
            quantity_entry.grid(column=i, row=1, sticky='ew', padx=10)

        # Add to cart button
        add_button = tk.Button(tab, text="Add to Cart", command=lambda i=i: add_to_cart_callback(i))
        add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)


# Add to cart callbacks
def add_movie_to_cart(movie_index):
    # Replace 'Movie Name' with your movie names
    add_to_receipt(f"Movie Name {movie_index + 1}", 1, "Movie")


def add_food_to_cart(food_index):
    # Replace 'Food Name' with your food names
    add_to_receipt(f"Food Name {food_index + 1}", 1, "Food")


def add_drink_to_cart(drink_index):
    # Replace 'Drink Name' with your drink names
    add_to_receipt(f"Drink Name {drink_index + 1}", 1, "Drink")


# Create the Movies, Foods, and Drinks tabs
movies_tab = ttk.Frame(tabControl)
create_tab_content(movies_tab, 'Movie', add_movie_to_cart)
foods_tab = ttk.Frame(tabControl)
create_tab_content(foods_tab, 'Food', add_food_to_cart)
drinks_tab = ttk.Frame(tabControl)
create_tab_content(drinks_tab, 'Drink', add_drink_to_cart)

# Add the tabs to the tab control
tabControl.add(movies_tab, text='Movies')
tabControl.add(foods_tab, text='Foods')
tabControl.add(drinks_tab, text='Drinks')

# Pack the tab control into the main window
tabControl.pack(expand=1, fill="both")

# Create the Receipt section
receipt_label = tk.Label(root, text="Receipt:")
receipt_label.pack()
receipt_text = tk.Text(root, height=10, width=50)
receipt_text.pack()

# Run the main window's event loop
root.mainloop()
