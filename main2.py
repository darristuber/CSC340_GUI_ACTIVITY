import tkinter as tk

from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import font as tkFont
from pymongo import MongoClient

# link our individual sql databases
client = MongoClient('localhost', 27017)
db = client['mongo_movies']
# main window
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.configure(bg='black')  # Set the background color to matte black
root.state('zoomed')
app_font = tkFont.Font(family='Helvetica', size=14, weight='bold')

# formatting for buttons
style = ttk.Style()
style.configure('TButton', background='white', foreground='black')

# fix tabs
tabControl = ttk.Notebook(root)


# get movies information from database
def fetch_movies():
    try:
        movies_collection = db['movies']
        movies = list(movies_collection.find())
        return movies
    except Exception as e:
        print(f"An error occurred: {e}")


# same with showings database
def fetch_showings(movie_id):
    try:
        showings_collection = db['showings']
        showings = list(showings_collection.find())
        times = []
        for row in showings:
            if row['movieID'] == movie_id:
                times.append(str(row['time']))
        return times
    except Exception as e:
        print(f"An error occurred: {e}")


# now get food data
def fetch_foods():
    try:
        concessions_collection = db['concessions']
        foods = list(concessions_collection.find())
        return foods

    except Exception as e:
        print(f"An error occurred: {e}")


def add_movie_to_cart(movie_index):
    movie_id = movie_index
    try:
        # Fetch movies
        movies = fetch_movies()

        # Find the movie with the given movie_id
        selected_movie = None
        for movie in movies:
            if movie['movieID'] == movie_id:
                selected_movie = movie
                break

        if selected_movie:
            movie_name = selected_movie['Name']
            adult_price = selected_movie['ACost']
            kid_price = selected_movie['KCost']
            showings = fetch_showings(movie_id)

            popup = tk.Toplevel(root)
            popup.title("Select Time and Enter Age")

            # time selection dropdown
            time_label = tk.Label(popup, text="Select time:", font=app_font)
            time_label.pack()
            times = showings
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
                popup.destroy()  # close the popup window

                # choose ticket type
                ticket_price = adult_price if age >= 12 else kid_price
                ticket_type = "Adult Ticket" if age >= 12 else "Child Ticket"

                receipt_update(movie_name, ticket_type, ticket_price)

            add_button = tk.Button(popup, text="Add to Cart", command=add_to_cart_after_age)
            add_button.pack()

        else:
            print("Movie not found.")


    except Exception as e:
        print(f"An error occurred: {e}")


def receipt_update(movie_name, ticket_type, ticket_price):
    item_index = None
    for i, line in enumerate(receipt_text.get("1.0", tk.END).split("\n")):
        if f"{movie_name} {ticket_type} " in line:
            item_index = i
            break

    if item_index is not None:
        current_line = receipt_text.get(f"{item_index + 1}.0", f"{item_index + 1}.end")
        quantity = int(current_line.split("x")[0].strip()) + 1
        receipt_text.delete(f"{item_index + 1}.0", f"{item_index + 1}.end")
        new_cost = int(quantity*float(ticket_price))
        receipt_text.insert(f"{item_index + 1}.0", f"{quantity}x {movie_name} {ticket_type} - ${new_cost}")
    else:
        if receipt_text.get("1.0", tk.END).strip():
            receipt_text.insert(tk.END, "\n")  # Add newline if it's not the first item
        receipt_text.insert(tk.END, f"1x {movie_name} {ticket_type} - ${ticket_price}")

    receipt_text.configure(bg='gray', fg='white')
    update_total(ticket_price)


def add_food_to_cart(food_index):
    try:
        foods = fetch_foods()
        for i, food in enumerate(foods):
            item_name = food['ItemName']
            Cost = food['Cost']
            item_id = food['ItemID']
            if item_id == food_index:
                item_found = False
                for line in receipt_text.get("1.0", tk.END).split("\n"):
                    if f"{item_name} " in line:
                        item_found = True
                        #increment quantity if already in receipt
                        lines = receipt_text.get("1.0", tk.END).split("\n")
                        for j, line in enumerate(lines):
                            if f"{item_name} " in line:
                                quantity = int(line.split("x")[0].strip()) + 1
                                new_cost = int(quantity*float(Cost))
                                lines[j] = f"{quantity}x {item_name} - ${new_cost}"
                                break

                        receipt_text.delete("1.0", tk.END)
                        for line in lines:
                            receipt_text.insert(tk.END, line + "\n")
                        break  #exit once updated
                else:
                    #no item, add new line
                    if receipt_text.get("1.0", tk.END).strip():
                        receipt_text.insert(tk.END, "\n")
                    receipt_text.insert(tk.END, f"1x {item_name} - ${Cost}")
                update_total(Cost)
                break  #exit
        else:
            print("Food not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_movies_tab_content(tab):
    movies = fetch_movies()
    for i, movie in enumerate(movies):
        movie_id = movie.get('movieID')  # Get movieID field
        movie_name = movie.get('Name')  # Get Name field
        movie_rating = movie.get('rating')  # Get Rating field

        # Load the banner image
        banner_path = f"{movie_id}.jpeg"
        banner_image = Image.open(banner_path)
        banner_photo = ImageTk.PhotoImage(banner_image)
        banner_label = tk.Label(tab, image=banner_photo, width=350, height=350)
        banner_label.image = banner_photo  # keep a reference!
        banner_label.grid(column=i, row=0, padx=10, pady=10)

        # Create and place the movie name label below the banner image
        movie_name_label = tk.Label(tab, text=movie_name, font=app_font, bg='white')
        movie_name_label.grid(column=i, row=1, padx=10, pady=2)

        # Create and place the movie rating label below the movie name
        movie_rating_label = tk.Label(tab, text=f"Rating: {movie_rating}", font=app_font, bg='white')
        movie_rating_label.grid(column=i, row=2, padx=10, pady=2)

        button_width = 20
        button_height = 3  # Height is typically set in text lines, not pixels.

        # Wrap the function call to include the movie ID
        def add_movie_to_cart_wrapper(movie_id=movie_id):
            add_movie_to_cart(movie_id)

        # Create and place the add to cart button below the movie rating label
        add_button = tk.Button(tab, text="Add to Cart", width=button_width, height=button_height,
                               font=app_font, command=add_movie_to_cart_wrapper)
        add_button.grid(column=i, row=3, pady=5, sticky='ew', padx=10)

def create_tab_content(tab, item_type, add_to_cart_callback):
    foods = fetch_foods()
    for i, food in enumerate(foods):
        food_id, food_name, food_price = food['ItemID'], food['ItemName'], food['Cost']
        banner_path = f"{food_name}.jpeg"
        banner_image = Image.open(banner_path)
        banner_photo = ImageTk.PhotoImage(banner_image)
        banner_label = tk.Label(tab, image=banner_photo, width=200, height=350)
        banner_label.image = banner_photo
        banner_label.grid(column=i, row=0, padx=10, pady=10)

        label = tk.Label(tab, text=f"{food_name} - ${food_price}", fg="black", bg="white")
        label.grid(column=i, row=1, padx=10, pady=5, sticky="ew")

        add_button = create_add_to_cart_button(tab, food_id, food_name, food_price, add_to_cart_callback)
        add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)


def create_add_to_cart_button(tab, food_id, food_name, food_price, add_to_cart_callback):
    button_width = 20
    button_height = 4

    def add_to_cart_wrapper():
        add_to_cart_callback(food_id)

    add_button = tk.Button(tab, text="Add to Cart", width=button_width, height=button_height,
                           font=app_font, command=add_to_cart_wrapper)
    return add_button

# create the movies/concession tabs on GUI
movies_tab = ttk.Frame(tabControl)
create_movies_tab_content(movies_tab)
foods_tab = ttk.Frame(tabControl)
create_tab_content(foods_tab, 'Concessions', add_food_to_cart)

# grid columns to have the same weight
number_of_columns = 5
for i in range(number_of_columns):
    movies_tab.grid_columnconfigure(i, weight=1, uniform="group1")
    foods_tab.grid_columnconfigure(i, weight=1, uniform="group1")

##add the tabs to the tab control
tabControl.add(movies_tab, text='Movies')
tabControl.add(foods_tab, text='Foods')

#pack the tab control into the main window
tabControl.pack(expand=1, fill="both")

# Place the new buttons in the GUI for movie ratings
ratings_frame = tk.Frame(root)
ratings_frame.pack(fill='x', padx=5, pady=5)


# Make sure the column configuration allows for the widget to stretch or shrink as needed
ratings_frame.grid_columnconfigure(0, weight=1)



#the button for PG movies and its placement

def list_pg_movies():
    try:
        movies_collection = db['movies']
        pg_movies = movies_collection.find({'rating': 'PG'}, {'Name': 1})
        # get movies from query
        pg_movie_names = [movie['Name'] for movie in pg_movies]
        messagebox.showinfo("PG Movies", "\n".join(pg_movie_names))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


#####


pg_button = tk.Button(ratings_frame, text="List PG", command=list_pg_movies, width=20)
pg_button.pack(side='top', pady=5)



#add_button = create_add_to_cart_button(tab, food_id, food_name, food_price, add_to_cart_callback)
#add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)

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
    try:
        orders_collection = db['orders']
        # get max existing order number
        max_order_num = orders_collection.find_one(
            sort=[("OrderNum", -1)])  # sort desc
        if max_order_num:
            order_num = max_order_num['OrderNum'] + 1
        else:
            order_num = 1

        # get items from receipt
        order_items = receipt_text.get("1.0", tk.END).strip()
        order_cost = total_value.cget("text")

        # insert items into orders
        order_data = {
            "OrderNum": order_num,
            "OrderItems": order_items,
            "OrderCost": order_cost
        }
        orders_collection.insert_one(order_data)

        tk.messagebox.showinfo("Checkout", "Order placed successfully!")

        # clear receipt/tot cost
        receipt_text.delete("1.0", tk.END)
        total_value.config(text="0.00")

    except Exception as e:
        print(f"An error occurred: {e}")


# Place the checkout button in the top right of the total_frame
checkout_button = tk.Button(total_frame, text="Checkout", command=checkout, font=app_font)
checkout_button.grid(row=0, column=2, sticky='ne', padx=10, pady=10)

# Configure the grid layout to push everything to the left
total_frame.grid_columnconfigure(0, weight=1)
# This will make the column 0 take up all the extra space, pushing column 2 to the right

root.mainloop()

client.close()
