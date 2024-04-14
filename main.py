import tkinter as tk

from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import font as tkFont


# database functions
from database import get_connection, close_connection

# the main window
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.configure(bg='black')  # Set the background color to matte black

# full-screen
root.state('zoomed')
app_font = tkFont.Font(family='Helvetica', size=14, weight='bold')

# style for the buttons
style = ttk.Style()
style.configure('TButton', background='white', foreground='black')
#  tab control
tabControl = ttk.Notebook(root)

#fetch movie data from the database
def fetch_movies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    close_connection(conn)
    return movies

#fetch showings data from the database
def fetch_showings(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM showings WHERE movieID = %s", (movie_id,))
    showings = cursor.fetchall()
    close_connection(conn)
    return showings

def fetch_foods():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Concessions")
    foods = cursor.fetchall()
    close_connection(conn)
    return foods

# add_movie_to_cart function
def add_movie_to_cart(movie_index):
    movie_id = movie_index + 1  # Assuming movie IDs start from 1
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Name, ACost, KCost FROM movies WHERE movieID = %s", (movie_id,))
    movie_details = cursor.fetchone()
    close_connection(conn)

    if movie_details:
        movie_name, adult_price, kid_price = movie_details
        showings = fetch_showings(movie_id)

        #a popup window to prompt for time and age
        popup = tk.Toplevel(root)
        popup.title("Select Time and Enter Age")

        # dropdown for selecting time
        time_label = tk.Label(popup, text="Select time:", font=app_font)
        time_label.pack()
        times = [showing[0] for showing in showings]  # Assuming each showing is a tuple with the time as the first element
        time_var = tk.StringVar(popup)
        time_dropdown = ttk.Combobox(popup, textvariable=time_var, values=times, state="readonly")
        time_dropdown.pack()

        age_label = tk.Label(popup, text="Enter your age:", font=app_font)
        age_label.pack()

        age_entry = tk.Entry(popup)
        age_entry.pack()

        def add_to_cart_after_age():
            selected_time = time_var.get()
            if not selected_time:
                messagebox.showerror("Error", "Please select a time before adding to cart.")
                return

            age = int(age_entry.get())
            popup.destroy()  # close the popup window after collecting data

            # determine ticket price and type
            ticket_price = adult_price if age >= 12 else kid_price
            ticket_type = "Adult Ticket" if age >= 12 else "Child Ticket"

            # logic to add item to receipt
            receipt_update(movie_name, ticket_type, ticket_price)

        add_button = tk.Button(popup, text="Add to Cart", command=add_to_cart_after_age)
        add_button.pack()

    else:
        print("Movie not found.")

def receipt_update(movie_name, ticket_type, ticket_price):
    item_index = None
    for i, line in enumerate(receipt_text.get("1.0", tk.END).split("\n")):
        if f"{movie_name} ({ticket_type}) - ${ticket_price}" in line:
            item_index = i
            break

    if item_index is not None:
        current_line = receipt_text.get(f"{item_index + 1}.0", f"{item_index + 1}.end")
        quantity = int(current_line.split("x")[0].strip()) + 1
        receipt_text.delete(f"{item_index + 1}.0", f"{item_index + 1}.end")
        receipt_text.insert(f"{item_index + 1}.0", f"{quantity}x {movie_name} ({ticket_type}) - (${ticket_price})")
    else:
        if receipt_text.get("1.0", tk.END).strip():
            receipt_text.insert(tk.END, "\n")  # Add newline if it's not the first item
        receipt_text.insert(tk.END, f"1x {movie_name} ({ticket_type}) - ${ticket_price}")

    receipt_text.configure(bg='gray', fg='white')
    update_total(ticket_price)

# add_food_to_cart function
def add_food_to_cart(food_index):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Concessions WHERE ItemID = %s", (food_index + 1,))
    food_details = cursor.fetchone()
    close_connection(conn)

    if food_details:
        ItemID, ItemName, Cost = food_details

        # if the item is already in the receipt
        item_index = None
        for i, line in enumerate(receipt_text.get("1.0", tk.END).split("\n")):
            if f"{ItemName} - ${Cost}" in line:
                item_index = i
                break

        if item_index is not None:
            # item already in receipt, increment its quantity
            current_line = receipt_text.get(f"{item_index + 1}.0", f"{item_index + 1}.end")
            quantity = int(current_line.split("x")[0].strip()) + 1
            receipt_text.delete(f"{item_index + 1}.0", f"{item_index + 1}.end")
            receipt_text.insert(f"{item_index + 1}.0", f"{quantity}x {ItemName} - ${Cost}")
        else:
            # Item not in receipt, add it
            if receipt_text.get("1.0", tk.END).strip():
                receipt_text.insert(tk.END, "\n")  # Add newline if it's not the first item
            receipt_text.insert(tk.END, f"1x {ItemName} - ${Cost}")
        # update total cost
        update_total(Cost)

    else:
        print("Food not found.")


# create the tab content for Movies
def create_movies_tab_content(tab):
    movies = fetch_movies()
    for i, movie in enumerate(movies):
        movie_id, movie_name = movie[0], movie[1]
        # Banner
        banner_path = f"{movie_id}.jpeg"
        banner_image = Image.open(banner_path)
        banner_photo = ImageTk.PhotoImage(banner_image)
        banner_label = tk.Label(tab, image=banner_photo, width=200, height=300)
        banner_label.image = banner_photo
        banner_label.grid(column=i, row=0, padx=10, pady=10)

        # add to cart button
        button_width = 20  # Width in characters
        button_height = 2  # Height in text lines

        # create the add to to cart
        add_button = tk.Button(tab, text="Add to Cart", width=button_width, height=button_height,
                               font=app_font, command=lambda i=i: add_movie_to_cart(i))

        add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)

# create the tab content for Foods
def create_tab_content(tab, item_type, add_to_cart_callback):
    foods = fetch_foods()
    for i, food in enumerate(foods):
        food_id, food_name, food_price = food[0], food[1], food[2]
        # Banner
        banner_path = f"{food_name}.jpeg"
        banner_image = Image.open(banner_path)
        banner_photo = ImageTk.PhotoImage(banner_image)
        banner_label = tk.Label(tab, image=banner_photo, width=200, height=200)
        banner_label.image = banner_photo
        banner_label.grid(column=i, row=0, padx=10, pady=10)

        button_width = 20  # Width in characters
        button_height = 2  # Height in text lines

        label = tk.Label(tab, text=f"{food_name} - ${food_price}", fg="black", bg="white")
        label.grid(column=i, row=1, padx=10, pady=5, sticky="ew")

        add_button = tk.Button(tab, text="Add to Cart", width=button_width, height=button_height,
                               font=app_font, command=lambda i=i: add_movie_to_cart(i))
        add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)


# create the Movies, Foods tabs
movies_tab = ttk.Frame(tabControl)
create_movies_tab_content(movies_tab)
foods_tab = ttk.Frame(tabControl)
create_tab_content(foods_tab, 'Concessions', add_food_to_cart)


# grid columns to have the same weight
number_of_columns = 5  # Adjust this to the actual number of columns you have
for i in range(number_of_columns):
    movies_tab.grid_columnconfigure(i, weight=1, uniform="group1")
    foods_tab.grid_columnconfigure(i, weight=1, uniform="group1")





# Add the tabs to the tab control
tabControl.add(movies_tab, text='Movies')
tabControl.add(foods_tab, text='Foods')

# Pack the tab control into the main window
tabControl.pack(expand=1, fill="both")

# Place the new buttons in the GUI for movie ratings
ratings_frame = tk.Frame(root)
ratings_frame.pack(fill='x', padx=5, pady=5)

# Define the button for PG movies and its placement

def list_pg_movies():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Make sure to replace 'your_database_name' with the actual name of your database
        cursor.execute("CREATE OR REPLACE VIEW pg_movies AS SELECT Name FROM MOVIE_THEATRE.Movies WHERE rating = 'PG'")
        conn.commit()
        cursor.execute("SELECT Name FROM pg_movies")
        pg_movie_names = cursor.fetchall()
        close_connection(conn)
        # Display the movie names in a messagebox or in a designated area of your GUI
        messagebox.showinfo("PG Movies", "\n".join(name for (name,) in pg_movie_names))
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
        close_connection(conn)
#####

pg_button = tk.Button(ratings_frame, text="List PG", command=list_pg_movies)
pg_button.pack(side='left', padx=2, pady=2)

# Create the Receipt section
receipt_label = tk.Label(root, text="Receipt:")
receipt_label.pack()
receipt_text = tk.Text(root, height=10, width=70, font=app_font)

receipt_text.pack()

total_frame = tk.Frame(root, bg="black")
total_frame.pack(fill="x", padx=10, pady=5)

total_label = tk.Label(total_frame, text="Total: $", fg="white", bg="black")
total_label.grid(row=0, column=0, sticky="e")

total_value = tk.Label(total_frame, text="0.00", fg="white", bg="black")
total_value.grid(row=0, column=1, sticky="w")

# Configure total frame to center horizontally
total_frame.pack_configure()



# Function to update the total cost
def update_total(cost):
    current_total = float(total_value.cget("text"))
    updated_total = current_total + float(cost)
    total_value.config(text=f"{updated_total:.2f}")
def checkout():
    # Query the database to get the highest existing OrderNum
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(OrderNum) FROM Orders")
    max_order_num = cursor.fetchone()[0]
    conn.commit()
    close_connection(conn)

    # If there are existing orders, increment the highest OrderNum by 1
    if max_order_num is not None:
        order_num = max_order_num + 1
    else:
        order_num = 1  # If no existing orders, start from 1

    # Retrieve OrderItems from the receipt box
    order_items = receipt_text.get("1.0", tk.END).strip()

    # Retrieve OrderCost from the total cost label
    order_cost = total_value.cget("text")

    # Print the items that will be added to Orders
    print("Order Items:")
    print(order_items)
    print("Order Cost:", order_cost)

    # Insert data into the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Orders (OrderNum, OrderItems, OrderCost) VALUES (%s, %s, %s)",
                   (order_num, order_items, order_cost))
    conn.commit()
    close_connection(conn)

    # Display success message
    tk.messagebox.showinfo("Checkout", "Order placed successfully!")

    # Clear receipt and total cost values
    receipt_text.delete("1.0", tk.END)
    total_value.config(text="0.00")

# Create checkout button
checkout_button = tk.Button(root, text="Checkout", command=checkout)
checkout_button.pack(side="bottom", padx=10, pady=10)

# Run the main window's event loop
root.mainloop()