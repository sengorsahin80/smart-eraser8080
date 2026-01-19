# simple_eraser.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
import os
import sys

# Try to import rembg, if not available use simple method
try:
    from rembg import remove
    REMBG_AVAILABLE = True
    print("✅ rembg available - using AI model")
except ImportError:
    REMBG_AVAILABLE = False
    print("⚠️ rembg not available - using simple method")
    import cv2
    import numpy as np

class SmartEraser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🤖 Smart Eraser - SynMindLabs.com")
        self.window.geometry("900x700")
        self.window.configure(bg="#f8f9fa")
        
        # Set icon (optional)
        try:
            self.window.iconbitmap("icon.ico")
        except:
            pass
        
        self.setup_ui()
        self.current_image = None
        self.original_image = None
        
    def setup_ui(self):
        # HEADER
        header_frame = tk.Frame(self.window, bg="#667eea", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="🤖 SMART ERASER",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#667eea"
        )
        title.pack(pady=15)
        
        subtitle = tk.Label(
            header_frame,
            text="by SynMindLabs.com - AI Background Remover",
            font=("Arial", 12),
            fg="white",
            bg="#667eea"
        )
        subtitle.pack()
        
        # MAIN CONTENT
        main_frame = tk.Frame(self.window, bg="#f8f9fa", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # LEFT PANEL - UPLOAD
        left_panel = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            left_panel,
            text="📤 UPLOAD IMAGE",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333"
        ).pack(pady=20)
        
        self.original_canvas = tk.Canvas(left_panel, width=350, height=350, bg="#f0f0f0", highlightthickness=0)
        self.original_canvas.pack(pady=10)
        self.original_canvas.create_text(175, 175, text="Drag & drop or click upload", fill="#999", font=("Arial", 12))
        
        upload_btn = tk.Button(
            left_panel,
            text="📁 CHOOSE IMAGE",
            command=self.upload_image,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        upload_btn.pack(pady=20)
        
        # RIGHT PANEL - RESULT
        right_panel = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(
            right_panel,
            text="✨ RESULT",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333"
        ).pack(pady=20)
        
        self.result_canvas = tk.Canvas(right_panel, width=350, height=350, bg="#f0f0f0", highlightthickness=0)
        self.result_canvas.pack(pady=10)
        self.result_canvas.create_text(175, 175, text="Processed image will appear here", fill="#999", font=("Arial", 12))
        
        process_btn = tk.Button(
            right_panel,
            text="🚀 REMOVE BACKGROUND",
            command=self.process_image,
            bg="#667eea",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        process_btn.pack(pady=10)
        
        download_btn = tk.Button(
            right_panel,
            text="💾 SAVE RESULT",
            command=self.save_result,
            bg="#764ba2",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        download_btn.pack(pady=5)
        
        # STATUS BAR
        status_frame = tk.Frame(self.window, bg="#333", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready • SynMindLabs Smart Eraser v1.0",
            fg="white",
            bg="#333",
            font=("Arial", 10)
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # FOOTER
        footer = tk.Label(
            self.window,
            text="© 2024 SynMindLabs.com - AI Tools for Everyone | Smart Eraser • PDF Tools • Video Tools",
            font=("Arial", 9),
            fg="#666",
            bg="#f8f9fa"
        )
        footer.pack(side=tk.BOTTOM, pady=10)
        
    def upload_image(self):
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=file_types)
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                
                # Display image
                self.display_image(self.original_image, self.original_canvas)
                
                self.status_label.config(text=f"✓ Loaded: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Cannot load image:\n{str(e)}")
                self.status_label.config(text="✗ Error loading image")
    
    def display_image(self, image, canvas):
        # Resize to fit canvas
        width, height = image.size
        max_size = 340
        
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(resized)
        
        # Clear canvas and display
        canvas.delete("all")
        canvas.create_image(175, 175, image=photo, anchor=tk.CENTER)
        canvas.image = photo  # Keep reference
    
    def simple_remove_background(self, image):
        """Simple background removal without AI"""
        try:
            # Convert PIL to OpenCV
            img_np = np.array(image)
            
            if len(img_np.shape) == 2:  # Grayscale
                img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
            elif img_np.shape[2] == 4:  # RGBA
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
            
            # Invert mask
            mask = cv2.bitwise_not(thresh)
            
            # Apply morphological operations
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Create transparent image
            rgba = cv2.cvtColor(img_np, cv2.COLOR_RGB2RGBA)
            rgba[:, :, 3] = mask
            
            return Image.fromarray(rgba)
            
        except Exception as e:
            print(f"Simple removal error: {e}")
            return image
    
    def process_image(self):
        if self.current_image is None:
            messagebox.showwarning("No Image", "Please upload an image first!")
            return
        
        self.status_label.config(text="🔄 Processing...")
        self.window.update()
        
        try:
            if REMBG_AVAILABLE:
                # Use rembg AI
                img_byte_arr = io.BytesIO()
                self.current_image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                
                output_bytes = remove(img_bytes)
                result_image = Image.open(io.BytesIO(output_bytes))
            else:
                # Use simple method
                result_image = self.simple_remove_background(self.current_image)
            
            self.current_image = result_image
            self.display_image(result_image, self.result_canvas)
            
            self.status_label.config(text="✅ Background removed successfully!")
            
        except Exception as e:
            messagebox.showerror("Processing Error", f"Failed to process image:\n{str(e)}")
            self.status_label.config(text="✗ Processing failed")
    
    def save_result(self):
        if self.current_image is None or self.current_image == self.original_image:
            messagebox.showwarning("No Result", "Please process an image first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="background_removed.png"
        )
        
        if file_path:
            try:
                self.current_image.save(file_path, 'PNG')
                self.status_label.config(text=f"💾 Saved to: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Image saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Cannot save image:\n{str(e)}")
                self.status_label.config(text="✗ Save failed")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 SMART ERASER - SynMindLabs.com")
    print("="*60)
    print("Version: 1.0")
    print("Domain: synmindlabs.com")
    print("Status: AI Background Remover")
    print("="*60)
    
    # Check dependencies
    try:
        from PIL import Image
        print("✅ PIL/Pillow: OK")
    except:
        print("❌ PIL/Pillow: Missing - run: pip install pillow")
        sys.exit(1)
    
    print(f"✅ AI Engine: {'rembg available' if REMBG_AVAILABLE else 'simple mode'}")
    print("="*60)
    print("Starting application...\n")
    
    app = SmartEraser()
    app.run()