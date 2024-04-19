import tkinter as tk

from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import font as tkFont
from pymongo import MongoClient


#link our individual sql databases
client = MongoClient('localhost', 27017)
db = client['mongo_movies']
#main window
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.configure(bg='black')  # Set the background color to matte black
root.state('zoomed')
app_font = tkFont.Font(family='Helvetica', size=14, weight='bold')

#formatting for buttons
style = ttk.Style()
style.configure('TButton', background='white', foreground='black')

#fix tabs
tabControl = ttk.Notebook(root)

#get movies information from database
def fetch_movies():
    movies_collection = db['movies']
    movies = list(movies_collection.find())
    print(movies)
    return movies

#same with showings database
def fetch_showings(movie_id):
    try:
        showings_collection = db['showings']

        #get showings of the given movie_id from mongo
        showings = list(showings_collection.find({'movie_id': movie_id}, {'_id': 0, 'time': 1}))

        #return time field as list
        showings = [showing['time'] for showing in showings]
        return showings
    except Exception as e:
        print(f"An error occurred: {e}")

#now get food data
def fetch_foods():
    try:
        concessions_collection = db['concessions']
        foods = list(concessions_collection.find())
        return foods

    except Exception as e:
        print(f"An error occurred: {e}")

def add_movie_to_cart(movie_index):
    movie_id = movie_index + 1

    try:
        # Connect to MongoDB
        movies_collection = db['movies']

        # Query MongoDB for movie details
        movie_details = movies_collection.find_one({'_id': movie_id})

        if movie_details:
            movie_name = movie_details['Name']
            adult_price = movie_details['ACost']
            kid_price = movie_details['KCost']
            showings = fetch_showings(movie_id)

            popup = tk.Toplevel(root)
            popup.title("Select Time and Enter Age")

            #time selection dropdown
            time_label = tk.Label(popup, text="Select time:", font=app_font)
            time_label.pack()
            times = [showing['time'] for showing in showings]
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
                popup.destroy()  #close the popup window

                #choose ticket type
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


def add_food_to_cart(food_index):
    try:
        concessions_collection = db['concessions']
        food_details = concessions_collection.find_one({'_id': food_index + 1})

        if food_details:
            ItemName = food_details['ItemName']
            Cost = food_details['Cost']

            #if the item is already in the receipt
            item_found = False
            for line in receipt_text.get("1.0", tk.END).split("\n"):
                if f"{ItemName} - ${Cost}" in line:
                    item_found = True
                    break

            if item_found:
                #if item is in receipt, increment quantity
                lines = receipt_text.get("1.0", tk.END).split("\n")
                for i, line in enumerate(lines):
                    if f"{ItemName} - ${Cost}" in line:
                        quantity = int(line.split("x")[0].strip()) + 1
                        lines[i] = f"{quantity}x {ItemName} - ${Cost}"
                        break

                receipt_text.delete("1.0", tk.END)
                for line in lines:
                    receipt_text.insert(tk.END, line + "\n")
            else:
                #add new item
                if receipt_text.get("1.0", tk.END).strip():
                    receipt_text.insert(tk.END, "\n")
                receipt_text.insert(tk.END, f"1x {ItemName} - ${Cost}")

            update_total(Cost)
        else:
            print("Food not found.")


    except Exception as e:
        print(f"An error occurred: {e}")


def create_movies_tab_content(tab):
    movies = fetch_movies()
    for i, movie in enumerate(movies):
        movie_id, movie_name = movie['movieID'], movie['Name']
        banner_path = f"{movie_id}.jpeg"
        banner_image = Image.open(banner_path)
        banner_photo = ImageTk.PhotoImage(banner_image)
        banner_label = tk.Label(tab, image=banner_photo, width=200, height=300)
        banner_label.image = banner_photo
        banner_label.grid(column=i, row=0, padx=10, pady=10)

        # Add to cart button
        button_width = 20
        button_height = 2

        add_button = tk.Button(tab, text="Add to Cart", width=button_width, height=button_height,
                               font=app_font, command=lambda i=i: add_movie_to_cart(movie_id))
        add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)


def create_tab_content(tab, item_type, add_to_cart_callback):
    foods = fetch_foods()
    for i, food in enumerate(foods):
        food_id, food_name, food_price = food['ItemID'], food['ItemName'], food['Cost']
        banner_path = f"{food_name}.jpeg"
        banner_image = Image.open(banner_path)
        banner_photo = ImageTk.PhotoImage(banner_image)
        banner_label = tk.Label(tab, image=banner_photo, width=200, height=200)
        banner_label.image = banner_photo
        banner_label.grid(column=i, row=0, padx=10, pady=10)

        button_width = 20
        button_height = 2

        label = tk.Label(tab, text=f"{food_name} - ${food_price}", fg="black", bg="white")
        label.grid(column=i, row=1, padx=10, pady=5, sticky="ew")

        add_button = tk.Button(tab, text="Add to Cart", width=button_width, height=button_height,
                               font=app_font, command=lambda i=i: add_to_cart_callback(food_id))
        add_button.grid(column=i, row=2, pady=5, sticky='ew', padx=10)

#create the movies/concession tabs on GUI
movies_tab = ttk.Frame(tabControl)
create_movies_tab_content(movies_tab)
foods_tab = ttk.Frame(tabControl)
create_tab_content(foods_tab, 'Concessions', add_food_to_cart)


#grid columns to have the same weight
number_of_columns = 5
for i in range(number_of_columns):
    movies_tab.grid_columnconfigure(i, weight=1, uniform="group1")
    foods_tab.grid_columnconfigure(i, weight=1, uniform="group1")





#add the tabs to the tab control
tabControl.add(movies_tab, text='Movies')
tabControl.add(foods_tab, text='Foods')

#pack the tab control into the main window
tabControl.pack(expand=1, fill="both")

# Place the new buttons in the GUI for movie ratings
ratings_frame = tk.Frame(root)
ratings_frame.pack(fill='x', padx=5, pady=5)

# Define the button for PG movies and its placement

def list_pg_movies():
    try:
        movies_collection = db['movies']
        pg_movies = movies_collection.find({'rating': 'PG'}, {'Name': 1})
        #get movies from query
        pg_movie_names = [movie['Name'] for movie in pg_movies]
        messagebox.showinfo("PG Movies", "\n".join(pg_movie_names))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
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
    from pymongo import MongoClient

    def checkout():
        try:
            orders_collection = db['orders']
            #get max existing order number
            max_order_num = orders_collection.find_one(
                sort=[("OrderNum", -1)])  #sort desc
            if max_order_num:
                order_num = max_order_num['OrderNum'] + 1
            else:
                order_num = 1

            #get items from receipt
            order_items = receipt_text.get("1.0", tk.END).strip()
            order_cost = total_value.cget("text")

            #insert items into orders
            order_data = {
                "OrderNum": order_num,
                "OrderItems": order_items,
                "OrderCost": order_cost
            }
            orders_collection.insert_one(order_data)

            tk.messagebox.showinfo("Checkout", "Order placed successfully!")

            #clear receipt/tot cost
            receipt_text.delete("1.0", tk.END)
            total_value.config(text="0.00")

        except Exception as e:
            print(f"An error occurred: {e}")


checkout_button = tk.Button(root, text="Checkout", command=checkout)
checkout_button.pack(side="bottom", padx=10, pady=10)

root.mainloop()

client.close()