import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Water Pipe Design", page_icon="🚰", layout="centered")

st.title("🚰 โปรแกรมออกแบบท่อส่งน้ำ")
st.markdown("สำหรับอุตสาหกรรมน้ำดื่ม (เวอร์ชันมือถือ)")

# เพิ่มตัวเลือกขนาดท่อ (เส้นผ่านศูนย์กลางภายใน มม.)
pipe_sizes = {
    "2 นิ้ว (ID: 54.8 มม.)": 54.8,
    "2.5 นิ้ว (ID: 62.7 มม.)": 62.7,
    "3 นิ้ว (ID: 77.9 มม.)": 77.9,
    "4 นิ้ว (ID: 102.2 มม.)": 102.2
}

selected_pipe_name = st.selectbox("เลือกขนาดเส้นผ่านศูนย์กลางท่อ", list(pipe_sizes.keys()), index=1)
d_mm = pipe_sizes[selected_pipe_name]

q_m3h = st.number_input("อัตราการไหลของน้ำ (m³/h)", value=40.0)
pipe_length = st.number_input("ความยาวท่อรวม (เมตร)", value=120.0)
delta_z = st.number_input("ความต่างระดับ Elevation Head (เมตร)", value=6.0)
h_press = st.number_input("ความดันปลายทาง (เมตรน้ำ)", value=20.0)

d_m = d_mm / 1000.0
area = np.pi * (d_m ** 2) / 4.0
velocity = (q_m3h / 3600.0) / area

major_loss = 10.67 * (q_m3h ** 1.852) * (d_mm ** -4.87) * (150 ** -1.852) * pipe_length
minor_loss = 0.5 * (velocity ** 2) / (2 * 9.81)
total_loss = major_loss + minor_loss
tdh = delta_z + h_press + total_loss
power = (1000 * 9.81 * (q_m3h / 3600.0) * tdh) / 1000.0 / 0.75 * 1.2

if st.button("คำนวณผลลัพธ์", type="primary"):
    st.success("คำนวณสำเร็จ!")
    st.metric("ความเร็วในท่อ", f"{velocity:.2f} m/s", "เกณฑ์แนะนำ: 1.0 - 2.0 m/s")
    st.metric("เฮดรวมที่ปั๊มต้องสร้าง (TDH)", f"{tdh:.2f} เมตร")
    st.metric("กำลังมอเตอร์ที่แนะนำ", f"{power:.2f} kW")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    flows = np.linspace(1, max(q_m3h*1.5, 50), 30)
    ax.plot(flows, 70 - 0.005*(flows**2), label="Pump Curve", color="blue")
    ax.plot(flows, delta_z + h_press + (total_loss/(q_m3h**2))*(flows**2), label="System Curve", color="red")
    ax.set_xlabel("Flow Rate (m³/h)")
    ax.set_ylabel("Head (m)")
    ax.legend()
    st.pyplot(fig)
