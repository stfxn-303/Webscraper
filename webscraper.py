import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class WebScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Beautiful WebScraper")
        self.geometry("600x500")

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter website URL", width=400)
        self.url_entry.pack(pady=10)

        self.tag_entry = ctk.CTkEntry(self, placeholder_text="Enter HTML tag (e.g., p, h1)", width=200)
        self.tag_entry.pack(pady=10)

        self.scrape_button = ctk.CTkButton(self, text="Scrape", command=self.scrape_website)
        self.scrape_button.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=500, height=250, wrap="word")
        self.textbox.pack(pady=10)

        self.export_button = ctk.CTkButton(self, text="Export to File", command=self.export_to_file)
        self.export_button.pack(pady=10)

    def scrape_website(self):
        url = self.url_entry.get()
        tag = self.tag_entry.get()

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all(tag)

            self.textbox.delete("1.0", "end")
            for i, item in enumerate(results, 1):
                text = item.get_text(strip=True)
                if text:
                    self.textbox.insert("end", f"{i}. {text}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def export_to_file(self):
        text_data = self.textbox.get("1.0", "end").strip()
        if not text_data:
            messagebox.showwarning("No Data", "There is no scraped data to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_data)
            messagebox.showinfo("Success", f"Data exported to:\n{file_path}")

if __name__ == "__main__":
    app = WebScraperApp()
    app.mainloop()
