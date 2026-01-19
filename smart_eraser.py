# smart_eraser.py
import gradio as gr
from rembg import remove
from PIL import Image
import io
import tempfile
import os

def remove_background(input_image):
    """AI ile arka plan kaldır"""
    try:
        # PIL Image'ı bytes'a çevir
        img_byte_arr = io.BytesIO()
        input_image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        # AI ile arka plan kaldır
        output_bytes = remove(img_bytes)
        
        # Bytes'tan PIL Image'a çevir
        output_image = Image.open(io.BytesIO(output_bytes))
        
        return output_image
    except Exception as e:
        print(f"Hata: {e}")
        return input_image

# MARKA LOGOSU ve ARAYÜZ
with gr.Blocks(
    title="Smart Eraser - SynMindLabs", 
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {max-width: 1000px !important; margin: auto;}
    .title {text-align: center; padding: 20px;}
    .logo {font-size: 2.5em; color: #667eea; font-weight: bold;}
    """
) as demo:
    
    # HEADER
    gr.Markdown("""
    <div class="title">
        <div class="logo">🤖 Smart Eraser</div>
        <h2>by <strong style="color: #764ba2;">SynMindLabs.com</strong></h2>
        <p>AI-Powered Background Removal Tool</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📤 Upload Image")
            input_img = gr.Image(
                label="Drag & drop or click to upload", 
                type="pil",
                height=300
            )
            
            gr.Markdown("### ⚙️ Settings")
            process_btn = gr.Button(
                "✨ Remove Background", 
                variant="primary", 
                size="lg"
            )
            
            gr.Markdown("""
            **How it works:**
            1. Upload image (JPG, PNG, WebP)
            2. Click "Remove Background"
            3. Download transparent PNG
            """)
        
        with gr.Column(scale=1):
            gr.Markdown("### ✨ Result")
            output_img = gr.Image(
                label="Background Removed", 
                type="pil",
                height=300
            )
            
            gr.Markdown("### 📥 Download")
            download_btn = gr.Button("⬇️ Download PNG", size="lg")
            download_file = gr.File(label="Download")
    
    # FOOTER
    gr.Markdown("---")
    gr.Markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>🚀 SynMindLabs - AI Tools for Everyone</strong></p>
        <p>Smart Eraser • PDF Tools • Video Tools • AI Utilities</p>
        <p><em>Coming soon: Batch processing, API access, premium features</em></p>
        <p>📍 <strong>synmindlabs.com</strong> | 🐦 <strong>@synmindlabs</strong></p>
    </div>
    """)
    
    # FUNCTIONS
    def process_and_download(img):
        if img is None:
            return None, None
        
        # Process image
        result = remove_background(img)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
            result.save(f.name, 'PNG')
            return result, f.name
    
    # CONNECT BUTTONS
    process_btn.click(
        fn=process_and_download,
        inputs=[input_img],
        outputs=[output_img, download_file]
    )
    
    # Download button (separate)
    download_btn.click(
        fn=lambda img: process_and_download(img)[1] if img else None,
        inputs=[input_img],
        outputs=[download_file]
    )

# BAŞLAT
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 SMART ERASER - SynMindLabs")
    print("="*50)
    print("Domain: synmindlabs.com")
    print("Starting server...")
    print("🌐 Open in browser: http://localhost:7860")
    print("="*50)
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )