import tkinter as tk
from tkinter import messagebox
import json

def create_table():
        # show success message
    messagebox.showinfo("Success", f"Snippet has been created and added to database!")

    title = title_entry.get()
    subtitle = subtitle_entry.get()

    dlines = description_text.get("1.0", tk.END).split("\n")
    slines = source_text.get("1.0", tk.END).split("\n")

    dline_dict = {}
    sline_dict = {}

    # loop through all the description lines and add to the dictionary
    for i in range(len(dlines)):
        if dlines[i] != "":
            dline_dict[str(i+1)] = dlines[i]

    # loop through all the source lines and add to the dictionary
    for i in range(len(slines)):
        if slines[i] != "":
            sline_dict[str(i+1)] = slines[i]

    table = {"Title": title, "subTitle": subtitle, "dLine": dline_dict, "SLine": sline_dict}

    # read the existing database file, if any
    try:
        with open("database.json", "r") as f:
            database = json.load(f)
    except FileNotFoundError:
        database = {"tables": []}

    # add the new table to the existing tables
    database["tables"].append(table)

    # write the updated database file
    with open("database.json", "w") as f:
        json.dump(database, f, indent=4)

    # clear the input fields
    title_entry.delete(0, tk.END)
    subtitle_entry.delete(0, tk.END)
    description_text.delete("1.0", tk.END)
    source_text.delete("1.0", tk.END)


root = tk.Tk()
root.title("Snippet Creator")

title_label = tk.Label(root, text="Title:")
title_label.grid(row=0, column=0, padx=5, pady=5)

title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1, padx=5, pady=5)

subtitle_label = tk.Label(root, text="Subtitle:")
subtitle_label.grid(row=1, column=0, padx=5, pady=5)

subtitle_entry = tk.Entry(root)
subtitle_entry.grid(row=1, column=1, padx=5, pady=5)

description_label = tk.Label(root, text="Description:")
description_label.grid(row=2, column=0, padx=10, pady=10)

description_text = tk.Text(root, height=10)
description_text.grid(row=2, column=1, padx=5, pady=5)

source_label = tk.Label(root, text="Source Code:")
source_label.grid(row=3, column=0, padx=5, pady=5)

source_text = tk.Text(root, height=10)
source_text.grid(row=3, column=1, padx=150, pady=5)

create_table_button = tk.Button(root, text="Create Snippet", command=create_table)
create_table_button.grid(row=4, column=1, padx=5, pady=5)

# set the width and height of the window
width = 1000
height = 700
# get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# calculate the x and y coordinates to center the window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

# set the position of the window
root.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))

root.mainloop()
