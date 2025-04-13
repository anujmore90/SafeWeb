import tkinter as tk
import webbrowser

def open_browser_ui():
    window = tk.Tk()
    window.title("SafeWeb - Browser")

    tk.Label(window, text="Enter .onion URL:").pack()
    url_entry = tk.Entry(window)
    url_entry.pack()

    def open_url():
        url = url_entry.get()
        if url.endswith(".onion"):
            webbrowser.open(url)
        else:
            tk.messagebox.showerror("Error", "Please enter a valid .onion URL.")

    tk.Button(window, text="Open URL", command=open_url).pack()
    
    window.mainloop()
