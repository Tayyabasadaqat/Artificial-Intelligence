import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk


class QRGenerator:

    def __init__(self, root):

        self.root = root
        self.root.title("QR Code Generator")
        logo = tk.PhotoImage(file="logo.PNG")
        self.root.iconphoto(True, logo)
        self.root.geometry("650x550")
        self.root.configure(bg="#f4f6f8")
        self.root.resizable(False, False)

        self.qr_image = None

        title = tk.Label(
            root,
            text="QR Code Generator",
            font=("Segoe UI", 22, "bold"),
            bg="#f4f6f8",
            fg="#2c3e50"
        )
        title.pack(pady=15)

        self.entry = ttk.Entry(
            root,
            width=55,
            font=("Segoe UI", 12)
        )
        self.entry.pack(ipady=6)

        self.entry.focus()

        button_frame = tk.Frame(root, bg="#f4f6f8")
        button_frame.pack(pady=20)

        self.generate_btn = tk.Button(
            button_frame,
            text="Generate",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=12,
            command=self.generate_qr
        )
        self.generate_btn.grid(row=0, column=0, padx=10)

        self.save_btn = tk.Button(
            button_frame,
            text="Save",
            bg="#2980b9",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=12,
            state=tk.DISABLED,
            command=self.save_qr
        )
        self.save_btn.grid(row=0, column=1, padx=10)

        self.clear_btn = tk.Button(
            button_frame,
            text="Clear",
            bg="#e74c3c",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=12,
            command=self.clear
        )
        self.clear_btn.grid(row=0, column=2, padx=10)

        self.preview = tk.Label(
            root,
            bg="white",
            width=300,
            height=300,
            relief="solid",
            bd=1
        )
        self.preview.pack(pady=20)

        self.info = tk.Label(
            root,
            text="Enter text or URL above and click Generate",
            bg="#f4f6f8",
            fg="gray",
            font=("Segoe UI", 10)
        )
        self.info.pack()

    def generate_qr(self):

        data = self.entry.get().strip()

        if data == "":
            messagebox.showerror(
                "Error",
                "Please enter some text or URL."
            )
            return

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        self.qr_image = img

        preview = img.resize((280, 280))
        photo = ImageTk.PhotoImage(preview)

        self.preview.configure(image=photo)
        self.preview.image = photo

        self.save_btn.config(state=tk.NORMAL)

        self.info.config(
            text="QR Code generated successfully!"
        )

    def save_qr(self):

        if self.qr_image is None:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ],
            title="Save QR Code"
        )

        if filename:

            self.qr_image.save(filename)

            messagebox.showinfo(
                "Saved",
                "QR Code saved successfully!"
            )

    def clear(self):

        self.entry.delete(0, tk.END)

        self.preview.configure(image="")

        self.preview.image = None

        self.qr_image = None

        self.save_btn.config(state=tk.DISABLED)

        self.info.config(
            text="Enter text or URL above and click Generate"
        )


root = tk.Tk()

app = QRGenerator(root)

root.mainloop()