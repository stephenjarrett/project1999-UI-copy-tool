# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import filedialog
import shutil
import glob

# Function to save the last selected directory to a file
def save_last_directory(directory_path):
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "last_directory.txt")
    with open(file_path, "w") as file:
        file.write(directory_path)

# Function to load the last selected directory from the file
def load_last_directory():
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "last_directory.txt")
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return ""

def update_file_dropdown():
    # Clear the file dropdown
    file_dropdown['menu'].delete(0, 'end')

    # Get the directory path
    directory_path = directory_entry.get()

    # Get the files with the pattern UI_***_P1999Green.ini
    files = glob.glob(os.path.join(directory_path, "UI_*_P1999*.ini"))

    # Add the files to the file dropdown
    for file in files:
        file_path =  os.path.basename(file)
        file_dropdown['menu'].add_command(label=file_path, command=lambda file=file_path: select_file(file))

    # Set the default value for the file dropdown
    selected_file.set("Select file")

def update_destination_dropdown():
    # Clear the destination dropdown ####
    destination_dropdown['menu'].delete(0, 'end')

    # Get the directory path
    directory_path_destination = directory_entry.get()

    # Get the files with the pattern UI_***_P1999Green.ini
    files_destination = glob.glob(os.path.join(directory_path_destination, "UI_*_P1999*.ini"))

    # Add the files to the file dropdown
    for file in files_destination:
        file_path =  os.path.basename(file)
        destination_dropdown['menu'].add_command(label=file_path, command=lambda file=file_path: select_destination(file))

    # Set the default value for the destination dropdown ####
    selected_destination.set("Select file")

def copy_and_rename():
    source_file = os.path.join(directory_entry.get(), selected_file.get())
    source_file_2 = os.path.join(directory_entry.get(), selected_file.get().replace("UI_", ""))
    destination_file = os.path.join(directory_entry.get(), selected_destination.get())
    destination_file_2 = os.path.join(directory_entry.get(), selected_destination.get().replace("UI_", ""))

    if source_file == destination_file:
        success_label.config(text="Please select a different destination character", fg="red")
    else:       
        try:
            shutil.copyfile(source_file, destination_file)
            shutil.copyfile(source_file_2, destination_file_2)
            success_label.config(text="Success!", fg="green")
        except Exception as e:
            success_label.config(text="Error!", fg="red")

def select_directory():
    directory_path = filedialog.askdirectory(initialdir=load_last_directory())
    if directory_path:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(tk.END, directory_path)
        save_last_directory(directory_path)

        # Update the file dropdown
        update_file_dropdown()

        # If a file is already selected, update the destination dropdown
        update_destination_dropdown()

        clear_success()

def select_file(selection):
    selected_file.set(selection)
    clear_success()

def select_destination(selection):
    selected_destination.set(selection)
    clear_success()

def clear_success():
    # Clear the success indicator
    success_label.config(text="")

def close_window():
    window.destroy()

# Create the main window
window = tk.Tk()
window.title("Project 1999 - UI Copy Tool")

# Create the UI elements
directory_label = tk.Label(window, text="Project 1999 directory:")
directory_label.grid(row=0, column=0, sticky="w")
directory_entry = tk.Entry(window)
directory_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button = tk.Button(window, text="Browse", command=select_directory)
browse_button.grid(row=0, column=2, padx=5, pady=5)

file_label = tk.Label(window, text="Character file:")
file_label.grid(row=1, column=0, sticky="w")
selected_file = tk.StringVar(window)
file_dropdown = tk.OptionMenu(window, selected_file, "Select Project 1999 directory")
file_dropdown.grid(row=1, column=1, padx=5, pady=5)

destination_label = tk.Label(window, text="Destination Character File:")
destination_label.grid(row=2, column=0, sticky="w")
selected_destination = tk.StringVar(window)
destination_dropdown = tk.OptionMenu(window, selected_destination, "Select Project 1999 directory")
destination_dropdown.grid(row=2, column=1, padx=5, pady=5)

copy_button = tk.Button(window, text="Copy UI", command=copy_and_rename, font=("TkDefaultFont", 10, "bold"), relief=tk.RAISED)
copy_button.grid(row=3, column=0, columnspan=3, padx=(40,40), ipadx=75, pady=(20, 0), sticky="we")

success_label = tk.Label(window, text="")
success_label.grid(row=4, column=0, columnspan=2, pady=5)

# Load the last selected directory
last_directory = load_last_directory()
if last_directory:
    directory_entry.insert(tk.END, last_directory)
    update_file_dropdown()
    update_destination_dropdown()

window.protocol("WM_DELETE_WINDOW", close_window)

try:
    # Start the main event loop
    window.mainloop()
except KeyboardInterrupt:
    close_window()

