import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.colorchooser import askcolor
import img2insta_process

# create the root window
root = tk.Tk()
root.title('img2insta')
root.resizable(False, False)
root.geometry('500x200')

selected_files = {}
folder_selected = "C:/Users/alexa/OneDrive/Images/Pellicule/réussi/Instagram Processed"
color = "white"


def select_files():
    global selected_files
    filetypes = (
        ('jpg files', '*.jpg'),
        ('All files', '*.*')
    )

    selected_files = fd.askopenfilenames(
        title='Open files',
        initialdir='C:/Users/alexa/OneDrive/Images/Pellicule',
        filetypes=filetypes)
    print(selected_files)

    label_img.config(text=str(selected_files[0]) + "...")


def select_directory():
    global folder_selected
    folder_selected = fd.askdirectory(initialdir=folder_selected)
    print(folder_selected)
    label_out.config(text=str(folder_selected))


def change_color():
    global color
    colors = askcolor(title="Tkinter Color Chooser")
    color_btn.configure(bg=colors[1])
    print("color:", colors[1])
    color = colors[1]


def process():
    global selected_files, folder_selected, color
    if selected_files and folder_selected:
        img2insta_process.modify_images(selected_files, folder_selected, color)
        label_precess.config(text=str(len(selected_files)) + " images processed.")
        selected_files = ()
    else:
        if not selected_files and folder_selected:
            select_files()
            process()
        else:
            showinfo(
                title='unable to process',
                message="please select files and directory."
            )


cadre1 = tk.Frame(root)  # Cadre placé dans la fenêtre
cadre1.pack(padx=5, pady=5)
cadre2 = tk.Frame(root)  # Cadre placé dans la fenêtre
cadre2.pack(padx=5, pady=5)
cadre3 = tk.Frame(root)  # Cadre placé dans la fenêtre
cadre3.pack(padx=5, pady=5)
cadre4 = tk.Frame(root)  # Cadre placé dans la fenêtre
cadre4.pack(padx=5, pady=5, expand=True)

# images
img_button = tk.Button(cadre1,
                       text='Open Images',
                       command=select_files
                       )
img_button.pack(side=tk.LEFT)
label_img = tk.Label(cadre1, text="please select images to process", anchor="w")
label_img.pack(side=tk.LEFT)

# folder
out_btn = tk.Button(cadre2,
                    text='select output folder',
                    command=select_directory
                    )
out_btn.pack(side=tk.LEFT)
label_out = tk.Label(cadre2, text=folder_selected)
label_out.pack(side=tk.LEFT)

# color selection
color_btn = tk.Button(cadre3,
                      text='Select a Color',
                      command=change_color)
color_btn.pack(padx=20, side=tk.LEFT)

# process button
process_btn = tk.Button(cadre4,
                        text='Process',
                        command=process,
                        bg="red"
                        )
process_btn.pack(side=tk.LEFT)
label_precess = tk.Label(cadre4, text="No image selected")
label_precess.pack(side=tk.LEFT)

# run
root.mainloop()
