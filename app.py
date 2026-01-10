import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io

# 1. Cấu hình trang web
st.set_page_config(page_title="Document Layout Analysis", page_icon="📄")

st.title("📄 Document Layout Detection App")
st.write("Upload một ảnh tài liệu để hệ thống tự động nhận diện Header, Footer, Table...")

# 2. Load Model (Load 1 lần thôi dùng cache cho nhanh)
@st.cache_resource
def load_model():
    # Thay 'best.pt' bằng đường dẫn file model của bạn
    return YOLO("best.pt")

try:
    model = load_model()
    # Hiển thị thông báo load thành công (nhỏ xíu ở góc)
    st.toast("Model Loaded Successfully!", icon="✅")
except Exception as e:
    st.error(f"Không tìm thấy file model. Lỗi: {e}")

# 3. Widget Upload ảnh
uploaded_file = st.file_uploader("Chọn ảnh...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Chia cột: Bên trái ảnh gốc - Bên phải ảnh kết quả
    col1, col2 = st.columns(2)
    
    # Đọc ảnh
    image = Image.open(uploaded_file)
    
    with col1:
        st.header("Ảnh gốc")
        st.image(image, caption="Original Image", use_container_width=True)

    # Nút bấm để bắt đầu chạy
    if st.button("🚀 Phân tích ngay", type="primary"):
        with st.spinner('Đang phân tích... chờ xíu...'):
            # Chạy model YOLO
            results = model(image, conf=0.25) # conf=0.25 là độ tin cậy tối thiểu
            
            # Hàm plot() của YOLO tự động vẽ bounding box lên ảnh rất đẹp
            # Nó trả về numpy array (BGR), cần đổi lại màu xíu
            res_plotted = results[0].plot()[:, :, ::-1] 

        with col2:
            st.header("Kết quả")
            st.image(res_plotted, caption="Detected Layout", use_container_width=True)
            
            # (Tùy chọn) Hiện danh sách các vật thể tìm thấy bên dưới
            st.success("Đã tìm thấy các thành phần sau:")
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                st.write(f"- **{model.names[cls_id]}** (Độ tin cậy: {float(box.conf[0]):.2f})")