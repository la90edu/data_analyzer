# import streamlit as st
# import plotly.graph_objects as go
# import io
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from PIL import Image

# # פונקציה ליצירת גרף Plotly
# def generate_plotly_figure():
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 20, 15, 25], mode="lines+markers", name="Sample Data"))

#     # ✅ הוספת ערכת צבעים כדי להבטיח שהתוצאה תהיה צבעונית
#     fig.update_layout(
#         title="Sample Plotly Graph",
#         xaxis_title="X-Axis",
#         yaxis_title="Y-Axis",
#         template="plotly",  # תבנית צבעונית
#     )
#     return fig

# # שמירת הגרף כתמונה צבעונית
# def save_plotly_figure(fig):
#     img_buffer = io.BytesIO()
#     fig.write_image(img_buffer, format="png", scale=2)  # ✅ שמירה בצבעים ובאיכות גבוהה
#     img_buffer.seek(0)
#     return img_buffer

# # יצירת PDF עם הגרף
# def generate_pdf():
#     pdf_buffer = io.BytesIO()
#     c = canvas.Canvas(pdf_buffer, pagesize=letter)

#     # כותרת הדוח
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(100, 750, "Analysis Report")

#     # תיאור קצר
#     c.setFont("Helvetica", 12)
#     c.drawString(100, 730, "This report contains an analysis of the provided data.")

#     # יצירת הגרף ושמירתו כקובץ תמונה
#     fig = generate_plotly_figure()
#     img_buffer = save_plotly_figure(fig)

#     # המרת התמונה והכנסתה ל-PDF
#     img = Image.open(img_buffer)
#     img_path = "temp_graph.png"
#     img.save(img_path)
#     c.drawImage(img_path, 100, 500, width=300, height=200)  # התאמת המיקום והגודל של הגרף

#     c.showPage()
#     c.save()

#     pdf_buffer.seek(0)
#     return pdf_buffer

# # Streamlit App
# st.title("Export Plotly Graph to PDF")

# # הצגת הגרף באתר
# fig = generate_plotly_figure()
# st.plotly_chart(fig)

# # כפתור להורדת PDF
# if st.button("Download PDF"):
#     pdf_file = generate_pdf()
#     st.download_button(label="Click to download", data=pdf_file, file_name="report.pdf", mime="application/pdf")

##############################
# import streamlit as st
# import plotly.graph_objects as go
# import io
# import plotly.io as pio
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

# # Create an interactive Plotly figure
# def generate_plotly_figure():
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 20, 15, 25], mode="lines+markers", name="Sample Data"))
#     fig.update_layout(title="Interactive Plot", xaxis_title="X-Axis", yaxis_title="Y-Axis", template="plotly")
#     return fig

# # Save Plotly as an interactive HTML file
# def save_plotly_html(fig):
#     html_path = "plot.html"
#     pio.write_html(fig, file=html_path, full_html=True)
#     return html_path

# # Generate a PDF with a link to the interactive graph
# def generate_pdf(html_url):
#     pdf_buffer = io.BytesIO()
#     c = canvas.Canvas(pdf_buffer, pagesize=letter)

#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(100, 750, "Analysis Report")

#     c.setFont("Helvetica", 12)
#     c.drawString(100, 730, "This report contains an interactive graph.")

#     # 🔗 Add a clickable link to the online graph
#     c.setFillColorRGB(0, 0, 1)  # Blue color
#     c.drawString(100, 700, "Click here to view the interactive graph:")
#     c.linkURL(html_url, (100, 680, 400, 700), relative=0)

#     c.showPage()
#     c.save()
#     pdf_buffer.seek(0)
#     return pdf_buffer

# # Streamlit App
# st.title("Export Interactive Plotly Graph to PDF")

# fig = generate_plotly_figure()
# st.plotly_chart(fig)

# # Save HTML and provide a link (you need to upload it somewhere like Google Drive, Render, or a web server)
# html_file = save_plotly_html(fig)
# html_url = "https://yourwebsite.com/plot.html"  # Replace with your uploaded link

# if st.button("Download PDF"):
#     pdf_file = generate_pdf(html_url)
#     st.download_button(label="Click to download", data=pdf_file, file_name="report.pdf", mime="application/pdf")

####################
# import streamlit as st
# import matplotlib.pyplot as plt
# from fpdf import FPDF
# import io

# def create_pdf(text, fig):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # Add text
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, text)

#     # Save plot as an image
#     img_stream = io.BytesIO()
#     fig.savefig(img_stream, format="png")
#     img_stream.seek(0)

#     # Add plot to PDF
#     pdf.image(img_stream, x=10, w=180)

#     return pdf.output(dest="S").encode("latin1")  # Return as bytes

# st.title("Save Graph & Text to PDF")

# # User input
# user_text = st.text_area("Enter text to save in PDF")

# # Create a sample plot
# fig, ax = plt.subplots()
# ax.plot([1, 2, 3, 4], [10, 20, 30, 40])
# ax.set_title("Sample Graph")

# st.pyplot(fig)

# if st.button("Download PDF"):
#     pdf_bytes = create_pdf(user_text, fig)
#     st.download_button("Download PDF", pdf_bytes, "report.pdf", "application/pdf")
from PIL import Image

def create_pdf(text, fig):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # הוספת טקסט
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)

    # שמירת הגרף כקובץ PNG בזיכרון
    img_stream = io.BytesIO()
    fig.savefig(img_stream, format="png")
    img_stream.seek(0)

    # פתיחת התמונה עם PIL ושמירה זמנית
    img = Image.open(img_stream)
    image_path = "temp_image.png"
    img.save(image_path, format="PNG")

    # הוספת תמונה ל-PDF
    pdf.image(image_path, x=10, w=180)

    return pdf.output(dest="S").encode("latin1")
