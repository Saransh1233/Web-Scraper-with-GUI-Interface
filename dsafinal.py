import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import io
import time
import os
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

class WebScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper GUI")

        # URL Entry Section
        self.url_label = tk.Label(master, text="Enter the URL:", font=("Helvetica", 12))
        self.url_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        self.url_entry = tk.Entry(master, width=50, font=("Helvetica", 12))
        self.url_entry.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        # Save Button
        self.save_button = tk.Button(master, text="Save Information", command=self.save_information, state=tk.DISABLED, font=("Helvetica", 12))
        self.save_button.grid(row=0, column=2, pady=10, padx=10, sticky='w')

        # Show Complexity Button
        self.show_complexity_button = tk.Button(master, text="Show Complexity Graph", command=self.display_complexity_graph, state=tk.DISABLED, font=("Helvetica", 12))
        self.show_complexity_button.grid(row=0, column=3, pady=10, padx=10, sticky='w')

        # Buttons Section on the Left Side
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=1, column=0, rowspan=3, pady=10, padx=10, sticky='w')

        self.fetch_buttons = {}
        options = ["Get Text", "Get URL", "Get Title", "Get Meta Tags", "Get All URLs", "Get Images", "Exit"]
        for i, option in enumerate(options, start=1):
            self.fetch_buttons[i] = tk.Button(self.button_frame, text=option, command=lambda i=i: self.fetch_information(i), font=("Helvetica", 12))
            self.fetch_buttons[i].grid(row=i, column=0, pady=5, sticky='w')

        # Result Text Section
        self.result_text = scrolledtext.ScrolledText(master, width=50, height=10, font=("Helvetica", 12))
        self.result_text.grid(row=1, column=1, rowspan=3, pady=10, padx=10, sticky='w')

        # Image Display Section
        self.image_label = tk.Label(master, font=("Helvetica", 12))
        self.image_label.grid(row=1, column=2, rowspan=3, pady=10, padx=10, sticky='w')

        self.image_data = None  # Variable to store image data
        self.base_url = ""
        self.time_complexities = {}  # Dictionary to store time complexities for each option

    def fetch_information(self, choice=None):
        url = self.url_entry.get()

        if not url:
            self.result_text.insert(tk.END, "Please enter a valid URL.\n")
            return

        if choice is None:
            choice = tk.simpledialog.askinteger("Choose an option", "Enter your choice (1-6):\n1. Get Text\n2. Get URL\n3. Get Title\n4. Get Meta Tags\n5. Get All URLs on the Page\n6. Get Images\n7. Exit")

        # Calculate and display time complexity for the chosen option
        if choice:
            start_time = time.time()

        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, "html.parser")

        if choice == 1:
            text = soup.get_text()
            self.result_text.insert(tk.END, f"Text:\n{text}\n\n")
        elif choice == 2:
            self.result_text.insert(tk.END, f"URL:\n{url}\n\n")
        elif choice == 3:
            title = soup.title.text
            self.result_text.insert(tk.END, f"Title:\n{title}\n\n")
        elif choice == 4:
            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                self.result_text.insert(tk.END, f"Meta Tag: {tag.get('name', '')}: {tag.get('content', '')}\n")
        elif choice == 5:
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    self.result_text.insert(tk.END, f"Link: {href}\n")
        elif choice == 6:
            self.image_data = self.fetch_images_async(soup, url)
            self.base_url = url
            self.display_images_progressive()  # Display images using progressive loading
        elif choice == 7:
            self.master.destroy()
        else:
            self.result_text.insert(tk.END, "Invalid choice. Please enter a number between 1 and 7.\n")

        if choice:
            end_time = time.time()
            execution_time = end_time - start_time

            self.time_complexities[choice] = execution_time

        # Enable the save button, show graph button, and the fetch buttons
        self.master.after(500, self.enable_buttons)

    def fetch_images_async(self, soup, base_url):
        image_tags = soup.find_all('img')
        images = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            # Fetching images asynchronously using ThreadPoolExecutor
            futures = [executor.submit(self.fetch_single_image, base_url, img_tag) for img_tag in image_tags]

            # Retrieving the results
            for future in futures:
                image_data = future.result()
                if image_data:
                    images.append(image_data)

        return images

    def fetch_single_image(self, base_url, img_tag):
        src = img_tag.get('src')
        if src:
            image_url = requests.compat.urljoin(base_url, src)
            image_data = requests.get(image_url).content
            return image_data

    def display_images_progressive(self):
        if self.image_data:
            try:
                for i, image_data in enumerate(self.image_data):
                    tk_image = self.create_tk_image(image_data)

                    self.image_label.configure(image=tk_image)
                    self.image_label.image = tk_image

                    # Inserting a newline character to separate images
                    self.result_text.insert(tk.END, '\n')

                    # the GUI updation
                    self.master.update()
                    self.master.after(500)  # the delay time between images

            except Exception as e:
                self.result_text.insert(tk.END, f"Error displaying image: {str(e)}\n")

    def create_tk_image(self, image_data):
        image = Image.open(io.BytesIO(image_data))
        resized_image = image.resize((300, 200), Image.BILINEAR)
        tk_image = ImageTk.PhotoImage(resized_image)
        return tk_image

    def enable_buttons(self):
        self.save_button["state"] = tk.NORMAL  # Enable the save button
        self.show_complexity_button["state"] = tk.NORMAL  # Enable the show complexity graph button
        for i in range(1, 8):
            self.fetch_buttons[i]["state"] = tk.NORMAL  # Enable the fetch buttons

    def save_information(self):
        result_to_save = self.result_text.get("1.0", tk.END)
        self.result_text.insert(tk.END, "Saving information and images...\n")

        # Ask the user to choose a directory to save the file
        save_dir = filedialog.askdirectory()

        if not save_dir:
            self.result_text.insert(tk.END, "Saving canceled.\n")
            return

        # Save the text information in DOCX format
        doc = Document()
        doc.add_paragraph(result_to_save)
        doc_path = os.path.join(save_dir, "information.docx")
        doc.save(doc_path)

        # Save the images in PDF format
        pdf_path = os.path.join(save_dir, "images.pdf")
        self.save_images_to_pdf(pdf_path)

        self.result_text.insert(tk.END, f"Information and images saved in {save_dir}.\n")

    def save_images_to_pdf(self, pdf_path):
        if self.image_data:
            with open(pdf_path, "wb") as pdf_file:
                pdf = canvas.Canvas(pdf_file, pagesize=letter)

                for i, image_data in enumerate(self.image_data):
                    image = Image.open(io.BytesIO(image_data))
                    width, height = image.size

                    # Assuming letter size page, adjust scale based on your requirements
                    scale = min(letter[0] / width, letter[1] / height)

                    # Convert image_data to ImageReader
                    image_reader = ImageReader(io.BytesIO(image_data))

                    # Draw the image on the PDF page
                    pdf.drawImage(image_reader, 0, 0, width*scale, height*scale)
                    pdf.showPage()

                pdf.save()

    def display_complexity_graph(self):
        options = list(range(1, 7))
        time_complexities = [self.time_complexities.get(opt, 0) for opt in options]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(options, time_complexities, label='Time Complexity', color='blue')
        ax.set_xlabel('Options')
        ax.set_ylabel('Time Complexity')
        ax.set_title('Time Complexity for Each Option')
        ax.legend()

        # Embed the graph in the GUI
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().grid(row=4, column=1, columnspan=3, pady=10, padx=10, sticky='w')  # Update the grid parameters

        plt.show()

# Create and run the GUI
root = tk.Tk()
app = WebScraperGUI(root)
root.mainloop()
