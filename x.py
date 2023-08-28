import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import json

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Copy Pastes VxwxV")
        self.root.state("zoomed")
        self.bg_color = "#2E2E2E"
        self.text_color = "#FFFFFF"
        self.button_bg_color = "#444444"
        self.custom_style = ttk.Style()
        self.custom_style.configure("Custom.TFrame", background=self.bg_color)
        self.root.configure(bg=self.bg_color)
        self.text_list = []
        self.canvas_frame = tk.Frame(root, bg=self.bg_color)
        self.canvas_frame.pack(fill="both", expand=True)     
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.bg_color)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.text_frame = tk.Frame(self.canvas, bg=self.bg_color)
        self.canvas.create_window((0, 0), window=self.text_frame, anchor="nw")
        def onmousewheel(widget, command):
                    widget.bind("<Enter>", lambda _: widget.bind_all("<MouseWheel>", command))
                    widget.bind("<Leave>", lambda _: widget.unbind_all("<MouseWheel>"))

        onmousewheel(self.canvas, lambda e: self.canvas.yview_scroll(int(-0.01 * e.delta), "units"))


        for row in range(9):
            for col in range(6):
                frame = tk.Frame(self.text_frame, bg=self.bg_color)
                frame.grid(row=row, column=col, padx=5, pady=30)

               
                text_font = ("Courier New", 11)  

                text_box = tk.Text(frame, width=26, height=13, wrap=tk.WORD, state="disabled",
                                bg=self.bg_color, fg=self.text_color, font=text_font)
                text_box.pack()

                button_frame = tk.Frame(frame, bg=self.bg_color)
                button_frame.pack(side="bottom", fill="both", expand=True, padx=100, pady=10)

                copy_button = tk.Button(button_frame, text="Copiar", command=lambda tb=text_box: self.copy_text(tb), bg="#8AE29D")
                copy_button.pack(side="right", padx=5)

                edit_button = tk.Button(button_frame, text="Editar", command=lambda tb=text_box: self.edit_text(tb), bg="#A4D6E2")
                edit_button.pack(side="left", padx=5)

                self.text_list.append((text_box, copy_button, edit_button))

        self.text_frame.update_idletasks()  
        self.canvas.config(scrollregion=self.canvas.bbox("all"))



    def copy_text(self, text_box):
        selected_text = text_box.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
        self.root.update()

    def edit_text(self, text_box):
        if text_box.cget("state") == "normal":
            text_box.configure(state="disabled")
        else:
            self.open_edit_popup(text_box.get("1.0", "end-1c"), text_box)

    def open_edit_popup(self, current_text, text_box):
        popup = tk.Toplevel(self.root)
        popup.title("Editar Texto")

        popup_width = 500
        popup_height = 400
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2
        
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        popup.configure(bg=self.bg_color)  
        
        edited_text = tk.Text(popup, width=26, height=13, wrap=tk.WORD, bg="white", fg="black")  
        edited_text.pack(padx=20, pady=20)

        edited_text.insert("1.0", current_text)

        continue_button = tk.Button(popup, text="Continuar", command=lambda: self.continue_edit(text_box, edited_text.get("1.0", "end-1c"), popup), bg="#8AE29D")
        continue_button.pack(pady=10)

        cancel_button = tk.Button(popup, text="Cancelar", command=popup.destroy, bg="#E28A8A")
        cancel_button.pack()

    def continue_edit(self, text_box, edited_text, popup):
        updated_text = self._update_text_in_list(text_box, edited_text)
        if updated_text is not None:
            text_box.configure(state="normal")
            text_box.delete("1.0", "end")
            text_box.insert("1.0", updated_text)
            text_box.configure(state="disabled")
            self.save_data_to_json("data.json") 
        popup.destroy()

    def _update_text_in_list(self, text_box, edited_text):
        for tb, _, _ in self.text_list:
            if tb is text_box:
                if edited_text != tb.get("1.0", "end-1c"):
                    return edited_text
        return None

    def save_data_to_json(self, filename):
        data_to_save = []
        for text_box, _, _ in self.text_list:
            text = text_box.get("1.0", "end-1c")
            data_to_save.append(text)
        
        with open(filename, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)

    def load_data_from_json(self, filename):
        try:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
                for idx, (text_box, _, _) in enumerate(self.text_list):
                    if idx < len(data):
                        text_box.configure(state="normal")
                        text_box.delete("1.0", "end")
                        text_content = data[idx].replace("\n", "")
                        text_box.insert("1.0", text_content)
                        text_box.configure(state="disabled")
        except FileNotFoundError:
            pass

    def run(self):
        self.load_data_from_json("data.json")
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    app.run()