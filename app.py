import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io

# 1. Cấu hình trang web
st.set_page_config(page_title="Document Layout Analysis", page_icon="📄", layout="wide")

# 0. Sidebar chọn ngôn ngữ
LANGUAGES = {
    "English": {
        "sidebar_title": "Settings",
        "lang_select": "Language",
        "title": "📄 Document Layout Detection",
        "desc": "Upload a document image to automatically detect Header, Footer, Table, Text...",
        "upload_label": "Choose an image...",
        "btn_analyze": "🚀 Analyze Layout",
        "processing": "Analyzing... please wait...",
        "col_orig": "Original Image",
        "col_res": "Detected Result",
        "download_btn": "⬇️ Download Result Image",
        "stats_header": "📊 Detection Statistics",
        "found": "Found following elements:",
        "error_load": "Model not found. Please check 'best.pt' file.",
        "success_load": "Model Loaded Successfully!",
        "no_obj": "No objects detected.",
        "reliability": "Reliability"
    },
    "Tiếng Việt": {
        "sidebar_title": "Cài đặt",
        "lang_select": "Ngôn ngữ",
        "title": "📄 Phân tích Bố cục Tài liệu",
        "desc": "Tải lên ảnh tài liệu để hệ thống tự động nhận diện Tiêu đề, Chân trang, Bảng biểu...",
        "upload_label": "Chọn ảnh...",
        "btn_analyze": "🚀 Phân tích ngay",
        "processing": "Đang xử lý... chờ chút nhé...",
        "col_orig": "Ảnh gốc",
        "col_res": "Kết quả nhận diện",
        "download_btn": "⬇️ Tải ảnh kết quả về",
        "stats_header": "📊 Thống kê thành phần",
        "found": "Đã tìm thấy các thành phần sau:",
        "error_load": "Không tìm thấy file model. Kiểm tra lại file 'best.pt'.",
        "success_load": "Đã tải Model thành công!",
        "no_obj": "Không tìm thấy đối tượng nào.",
        "reliability": "Độ tin cậy"
    }
}

with st.sidebar:
    st.header("⚙️ Settings")
    # Mặc định index=0 là English
    selected_lang = st.selectbox("Language / Ngôn ngữ", ["English", "Tiếng Việt"], index=0)
    
    # Lấy bộ từ điển tương ứng
    text = LANGUAGES[selected_lang]
    
    st.divider()
    st.info("Model: YOLOv8 - DocLayNet\nClasses: 11 (Header, Footer, Table, Graph, Caption,...)")

st.title(text["title"])
st.write(text["desc"])

# 2. Load Model (Load 1 lần thôi dùng cache cho nhanh)
@st.cache_resource
def load_model():
    # Thay 'best.pt' bằng đường dẫn file model của bạn
    return YOLO("best.pt")

try:
    model = load_model()
    # Hiển thị thông báo load thành công (nhỏ xíu ở góc)
    st.toast(text["success_load"], icon="✅")
except Exception as e:
    st.error(f"{text['error_load']} Error: {e}")

# 3. Widget Upload ảnh
uploaded_file = st.file_uploader(text["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Chia cột: Bên trái ảnh gốc - Bên phải ảnh kết quả
    col1, col2 = st.columns(2)
    
    # Đọc ảnh
    image = Image.open(uploaded_file)
    
    with col1:
        st.header(text["col_orig"])
        st.image(image, caption="Original Image", use_container_width=True)

    # Nút bấm để bắt đầu chạy
    if st.button(text["btn_analyze"], type="primary", use_container_width=True):
        with st.spinner(text["processing"]):
            # Chạy model YOLO
            results = model(image, conf=0.25) # conf=0.25 là độ tin cậy tối thiểu
            
            # Hàm plot() của YOLO tự động vẽ bounding box lên ảnh rất đẹp
            # Nó trả về numpy array (BGR), cần đổi lại màu xíu
            res_plotted = results[0].plot()[:, :, ::-1]
            res_plotted = Image.fromarray(res_plotted)

        with col2:
            st.header(text["col_res"])
            st.image(res_plotted, caption="Detected Layout", use_container_width=True)

            # --- TÍNH NĂNG DOWNLOAD ---
            # Chuyển ảnh thành bytes để download
            buf = io.BytesIO()
            res_plotted.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label=text["download_btn"],
                data=byte_im,
                file_name="detected_result.png",
                mime="image/png",
                use_container_width=True
            )
            
            # (Tùy chọn) Hiện danh sách các vật thể tìm thấy bên dưới
            st.success(text["found"])
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                st.write(f"- **{model.names[cls_id]}** ({text['reliability']}: {float(box.conf[0]):.2f})")
