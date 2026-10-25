import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Water Pipe Design", page_icon="🚰", layout="centered")

st.title("🚰 โปรแกรมออกแบบท่อส่งน้ำ")
st.markdown("สำหรับอุตสาหกรรมน้ำดื่ม (เวอร์ชันมือถือ)")

q_m3h = st.number_input("อัตราการไหลของน้ำ (m³/h)", value=50.0)
pipe_length = st.number_input("ความยาวท่อรวม (เมตร)", value=120.0)
delta_z = st.number_input("ความต่างระดับ Elevation Head (เมตร)", value=15.0)
h_press = st.number_input("ความดันปลายทาง (เมตรน้ำ)", value=20.0)

d_mm = 62.7 
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
    st.metric("ความเร็วในท่อ", f"{velocity:.2f} m/s", "เกณฑ์: 1.0 - 2.0 m/s")
    st.metric("เฮดรวมที่ปั๊มต้องสร้าง (TDH)", f"{tdh:.2f} เมตร")
    st.metric("กำลังมอเตอร์ที่แนะนำ", f"{power:.2f} kW")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    flows = np.linspace(1, 100, 30)
    ax.plot(flows, 70 - 0.005*(flows**2), label="Pump Curve", color="blue")
    ax.plot(flows, delta_z + h_press + (total_loss/(q_m3h**2))*(flows**2), label="System Curve", color="red")
    ax.set_xlabel("Flow Rate")
    ax.set_ylabel("Head (m)")
    ax.legend()
    st.pyplot(fig)
