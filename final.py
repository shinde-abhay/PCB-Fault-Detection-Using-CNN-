import threading
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO
import numpy as np

# Load YOLO model (adjust path if needed)
model = YOLO(r"C:\Users\Abhay\Desktop\New folder\PCB_Defect\weights\best.pt")

# Defect information
DEFECT_INFO = {
    "spurious_copper": {
        "description": "Unwanted copper traces present on the PCB surface.",
        "remedy": "Remove using precision cutting tools or chemical etching."
    },
    "spur": {
        "description": "Small, thin copper projections extending from traces.",
        "remedy": "Scrape off carefully with a precision knife or rework station."
    },
    "short": {
        "description": "Unintended connection between two conductors.",
        "remedy": "Cut the bridging material or use desoldering tools to separate."
    },
    "open_circuit": {
        "description": "Broken trace causing disconnection in the circuit path.",
        "remedy": "Bridge the gap with solder or conductive ink/wire."
    },
    "mouse_bite": {
        "description": "Small semicircular cutouts along the edge of traces.",
        "remedy": "If severe, repair with conductive epoxy or replace the board."
    },
    "missing_hole": {
        "description": "Required drill hole absent from the PCB.",
        "remedy": "Drill manually with appropriate sized bit if possible."
    }
}


class StyledGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PCB Defect Detection — Dark Dashboard")
        self.root.geometry("1400x800")
        self.root.minsize(1100, 650)

        self._setup_style()
        self._setup_ui()

    def _setup_style(self):
        # Base theme - use clam for best custom styling support
        style = ttk.Style()
        style.theme_use("clam")

        # Colors
        self.bg = "#0f1720"           # charcoal
        self.card_bg = "#0f1727"      # slightly lighter card
        self.panel_bg = "#0b1020"     # panels
        self.neon = "#00ccff"         # neon blue
        self.text = "#dbeafe"         # light text
        self.muted = "#9aa6b2"        # muted text

        self.root.configure(bg=self.bg)

        style.configure("TFrame", background=self.bg)
        style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        style.configure("Panel.TFrame", background=self.panel_bg, relief="groove", borderwidth=1)
        style.configure("Header.TFrame", background=self.bg)
        style.configure("Title.TLabel", background=self.bg, foreground=self.neon,
                        font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background=self.bg, foreground=self.muted, font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="white",
                        background=self.neon, borderwidth=0, padding=6)
        style.map("Accent.TButton", background=[("active", "#00a6cc"), ("pressed", "#008aa3")])

        style.configure("Info.TLabel", background=self.card_bg, foreground=self.text, padding=8)
        style.configure("Small.TLabel", background=self.panel_bg, foreground=self.muted, font=("Segoe UI", 10))
        style.configure("Prediction.TFrame", background=self.panel_bg, relief="flat", borderwidth=0)

    def _setup_ui(self):
        # Header area
        header = ttk.Frame(self.root, style="Header.TFrame", padding=(20, 10))
        header.pack(side="top", fill="x")

        ttk.Label(header, text="PCB Defect Detection", style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="  •  Dark Dashboard", style="Sub.TLabel").pack(side="left")

        # Right side of header: buttons + progress
        buttons_frame = ttk.Frame(header, style="Header.TFrame")
        buttons_frame.pack(side="right")

        self.progress = ttk.Progressbar(buttons_frame, mode="indeterminate", length=160)
        self.progress.pack(side="right", padx=(8, 0))

        self.clear_btn = ttk.Button(buttons_frame, text="🧹 Clear", style="Accent.TButton", command=self.reset)
        self.clear_btn.pack(side="right", padx=8)

        self.upload_btn = ttk.Button(buttons_frame, text="📁 Upload Image", style="Accent.TButton",
                                     command=self._on_upload_click)
        self.upload_btn.pack(side="right")

        # Main content (grid) - 3 columns: left input, center output, right analysis
        content = ttk.Frame(self.root, style="TFrame", padding=(20, 12))
        content.pack(fill="both", expand=True)

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.columnconfigure(2, weight=0)  # fixed-width analysis panel

        # Left panel - input
        left_card = ttk.Frame(content, style="Card.TFrame", padding=10)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=6)
        left_card.columnconfigure(0, weight=1)
        ttk.Label(left_card, text="📷 Uploaded Image", style="Small.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.input_panel = ImagePanel(left_card, bg=self.card_bg)
        self.input_panel.frame.grid(row=1, column=0, sticky="nsew")
        left_card.rowconfigure(1, weight=1)

        self.input_status = ttk.Label(left_card, text="No image loaded.", style="Info.TLabel")
        self.input_status.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        # Center panel - output
        center_card = ttk.Frame(content, style="Card.TFrame", padding=10)
        center_card.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=6)
        center_card.columnconfigure(0, weight=1)
        ttk.Label(center_card, text="🔍 Detection Result", style="Small.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.output_panel = ImagePanel(center_card, bg=self.card_bg)
        self.output_panel.frame.grid(row=1, column=0, sticky="nsew")
        center_card.rowconfigure(1, weight=1)

        self.output_status = ttk.Label(center_card, text="Detection results will appear here.", style="Info.TLabel")
        self.output_status.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        # Right panel - analysis (fixed width)
        right_card = ttk.Frame(content, style="Panel.TFrame", padding=8, width=340)
        right_card.grid(row=0, column=2, sticky="nsew", pady=6)
        right_card.grid_propagate(False)  # keep width fixed
        right_card.rowconfigure(1, weight=1)

        ttk.Label(right_card, text="📊 Defect Analysis", style="Small.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.predictions_canvas = tk.Canvas(right_card, bg=self.panel_bg, highlightthickness=0)
        self.predictions_canvas.grid(row=1, column=0, sticky="nsew")
        self.predictions_scroll = ttk.Scrollbar(right_card, orient="vertical", command=self.predictions_canvas.yview)
        self.predictions_scroll.grid(row=1, column=1, sticky="ns")
        self.predictions_canvas.configure(yscrollcommand=self.predictions_scroll.set)

        # Frame inside canvas for predictions
        self.predictions_frame = ttk.Frame(self.predictions_canvas, style="Prediction.TFrame")
        self.predictions_frame.bind("<Configure>", lambda e: self.predictions_canvas.configure(scrollregion=self.predictions_canvas.bbox("all")))
        self.predictions_canvas.create_window((0, 0), window=self.predictions_frame, anchor="nw", width=320)

        # mousewheel support for predictions canvas
        self.predictions_canvas.bind_all("<MouseWheel>", self._on_mousewheel_predictions)

        # Initialize blank panels
        blank = Image.new("RGB", (640, 480), "#111217")
        self.input_panel.update_image(blank)
        self.output_panel.update_image(blank)

    def _on_mousewheel_predictions(self, event):
        # Windows delta is multiples of 120
        if self.predictions_canvas.winfo_ismapped():
            self.predictions_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_upload_click(self):
        # Open file dialog and start detection thread if file selected
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return
        # disable upload while processing
        self.upload_btn.state(["disabled"])
        self.clear_btn.state(["disabled"])
        self.progress.start(10)
        self.input_status.config(text="Loading image...", foreground=self.muted)

        # run detection in background
        threading.Thread(target=self._background_detect, args=(file_path,), daemon=True).start()

    def _background_detect(self, file_path):
        try:
            img = Image.open(file_path).convert("RGB")
            # show input image immediately on UI (use after to run in main thread)
            self.root.after(0, lambda: self._show_input_image(img))

            # run inference (this is the potentially slow op)
            results = model.predict(source=np.array(img), conf=0.25, verbose=False)

            # after inference finishes, hand results back to main thread for UI update
            self.root.after(0, lambda: self._on_detection_done(results, img))
        except Exception as e:
            self.root.after(0, lambda: self._on_detection_error(e))

    def _show_input_image(self, img):
        resized = self._resize_image(img, 560)
        self.input_panel.update_image(resized)
        self.input_status.config(text="Image loaded. Detecting...", foreground=self.text)

    def _on_detection_done(self, results, orig_image):
        # stop spinner and re-enable buttons
        self.progress.stop()
        self.upload_btn.state(["!disabled"])
        self.clear_btn.state(["!disabled"])

        # draw result overlay image
        try:
            output_arr = results[0].plot()
            output_img = Image.fromarray(output_arr[..., ::-1])
            resized_out = self._resize_image(output_img, 560)
            self.output_panel.update_image(resized_out)
        except Exception:
            # fallback if plot fails
            self.output_panel.update_image(self._resize_image(orig_image, 560))

        # update analysis panel
        self._populate_predictions(results)

        # update status messages
        if results[0].boxes is not None and len(results[0].boxes) > 0:
            count = len(results[0].boxes)
            self.output_status.config(text=f"{count} defect(s) detected.", foreground=self.neon)
        else:
            self.output_status.config(text="No defects detected.", foreground=self.muted)

    def _on_detection_error(self, exc):
        self.progress.stop()
        self.upload_btn.state(["!disabled"])
        self.clear_btn.state(["!disabled"])
        self.output_status.config(text=f"Error during detection: {exc}", foreground="red")

    def _populate_predictions(self, results):
        # clear previous
        for w in self.predictions_frame.winfo_children():
            w.destroy()

        if results[0].boxes is None or len(results[0].boxes) == 0:
            ttk.Label(self.predictions_frame, text="No defects found", style="Small.TLabel", foreground=self.muted).pack(pady=12)
            return

        # create cards for each detection
        for box in results[0].boxes:
            cls_index = int(box.cls)
            class_name = model.names[cls_index]
            conf = float(box.conf)

            card = ttk.Frame(self.predictions_frame, style="Panel.TFrame", padding=(8, 8))
            card.pack(fill="x", padx=8, pady=8)

            header = ttk.Frame(card, style="Panel.TFrame")
            header.pack(fill="x")
            ttk.Label(header, text=f"{class_name}", font=("Segoe UI", 11, "bold"), foreground=self.neon, background=self.panel_bg).pack(side="left")
            ttk.Label(header, text=f"{conf:.0%}", font=("Segoe UI", 10), foreground=self.muted, background=self.panel_bg).pack(side="right")

            info = DEFECT_INFO.get(class_name.lower(), {"description": "N/A", "remedy": "N/A"})
            ttk.Label(card, text=f"{info['description']}", style="Small.TLabel", background=self.panel_bg, foreground=self.text, wraplength=300).pack(anchor="w", pady=(6, 2))
            ttk.Label(card, text=f"Remedy: {info['remedy']}", style="Small.TLabel", background=self.panel_bg, foreground=self.muted, wraplength=300).pack(anchor="w")

    def reset(self):
        blank = Image.new("RGB", (640, 480), "#0b0e13")
        self.input_panel.update_image(blank)
        self.output_panel.update_image(blank)
        self.input_status.config(text="Upload a PCB image to begin detection.", foreground=self.muted)
        self.output_status.config(text="Detection results will appear here.", foreground=self.muted)
        for w in self.predictions_frame.winfo_children():
            w.destroy()

    def _resize_image(self, image, max_size):
        w, h = image.size
        ratio = min(max_size / w, max_size / h)
        return image.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)


class ImagePanel:
    def __init__(self, parent, bg="#0f1727"):
        self.frame = ttk.Frame(parent, style="Card.TFrame")
        self.frame.columnconfigure(0, weight=1)
        self.image_label = ttk.Label(self.frame, background=bg)
        self.image_label.grid(row=0, column=0, sticky="nsew")

    def update_image(self, pil_image):
        img_tk = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk


if __name__ == "__main__":
    root = tk.Tk()
    app = StyledGUI(root)
    root.mainloop()
