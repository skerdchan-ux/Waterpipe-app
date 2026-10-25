import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Water Pipe Design", page_icon="🚰", layout="wide")

st.markdown("""
    <style>
    .card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚰 โปรแกรมช่วยออกแบบระบบท่อส่งน้ำ")
st.markdown("**สำหรับอุตสาหกรรมน้ำดื่มและระบบสูบจ่ายน้ำ** — รองรับท่อเหล็กขนาด 2 ถึง 16 นิ้ว")
st.markdown("---")

# ส่วนข้อมูลตั้งต้น
st.subheader("1. ⚙️ ข้อมูลตั้งต้นระบบ (Inputs)")
col_in1, col_in2 = st.columns(2)

with col_in1:
    pipe_materials = {
        "ท่อเหล็ก (Steel Pipe - C=120)": 120,
        "สแตนเลส (SS304 - C=150)": 150,
        "PVC (C=140)": 140,
        "HDPE (C=130)": 130
    }
    selected_material = st.sidebar.selectbox if False else st.selectbox("ชนิดและวัสดุของท่อ", list(pipe_materials.keys()))
    c_factor = pipe_materials[selected_material]
    
    # รายการขนาดท่อ 2 ถึง 16 นิ้ว (อ้างอิงเส้นผ่านศูนย์กลางภายใน ID โดยประมาณสำหรับท่อเหล็กมาตรฐาน / ชสล.)
    steel_pipe_sizes = {
        "2 นิ้ว (ID: 52.5 มม.)": 52.5,
        "2.5 นิ้ว (ID: 62.7 มม.)": 62.7,
        "3 นิ้ว (ID: 77.9 มม.)": 77.9,
        "4 นิ้ว (ID: 102.3 มม.)": 102.3,
        "6 นิ้ว (ID: 154.1 มม.)": 154.1,
        "8 นิ้ว (ID: 202.7 มม.)": 202.7,
        "10 นิ้ว (ID: 254.5 มม.)": 254.5,
        "12 นิ้ว (ID: 303.2 มม.)": 303.2,
        "14 นิ้ว (ID: 333.3 มม.)": 333.3,
        "16 นิ้ว (ID: 381.0 มม.)": 381.0
    }
    
    selected_pipe_name = st.selectbox("ขนาดเส้นผ่านศูนย์กลางท่อ (2 - 16 นิ้ว)", list(steel_pipe_sizes.keys()), index=2)
    d_mm = steel_pipe_sizes[selected_pipe_name]
    
    q_m3h = st.number_input("อัตราการไหลของน้ำ (Q) [m³/h]", value=100.0)

with col_in2:
    pipe_length = st.number_input("ความยาวท่อรวม (L) [เมตร]", value=200.0)
    delta_z = st.number_input("ความต่างระดับ (ΔZ) [เมตร]", value=10.0)
    h_press = st.number_input("ความดันปลายทาง [เมตรน้ำ]", value=20.0)

st.markdown("##### อุปกรณ์ประกอบท่อ (Fittings)")
f1, f2, f3 = st.columns(3)
with f1:
    elbow_90 = st.number_input("ข้องอ 90°", value=4, min_value=0)
with f2:
    valve = st.number_input("วาล์ว", value=2, min_value=0)
with f3:
    tee = st.number_input("สามทาง", value=1, min_value=0)

st.markdown("---")

# คำนวณทางวิศวกรรม
d_m = d_mm / 1000.0
area = np.pi * (d_m ** 2) / 4.0
velocity = (q_m3h / 3600.0) / area
major_loss = 10.67 * (q_m3h ** 1.852) * (d_mm ** -4.87) * (c_factor ** -1.852) * pipe_length
k_total = (elbow_90 * 0.9) + (valve * 0.2) + (tee * 1.0)
minor_loss = k_total * (velocity ** 2) / (2 * 9.81)
total_loss = major_loss + minor_loss
tdh = delta_z + h_press + total_loss

rho, g = 1000.0, 9.81
hydraulic_power = (rho * g * (q_m3h / 3600.0) * tdh) / 1000.0
shaft_power = hydraulic_power / 0.75
motor_power_rec = shaft_power * 1.2

# แสดงผลลัพธ์
st.subheader("3. 📊 ผลการคำนวณและสรุปข้อมูลปั๊ม")
res1, res2 = st.columns(2)

with res1:
    st.markdown("### ข้อมูลท่อและการสูญเสีย")
    
    # เช็คเกณฑ์ความเร็ว
    if 1.0 <= velocity <= 2.0:
        v_status = "✅ อยู่ในช่วงแนะนำ (1.0 - 2.0 m/s)"
    elif velocity < 1.0:
        v_status = "⚠️ ต่ำกว่าเกณฑ์แนะนำ"
    else:
        v_status = "⚠️ สูงกว่าเกณฑ์แนะนำ"
        
    st.info(f"**ท่อที่เลือก:** {selected_pipe_name}\n\n**ความเร็วในท่อ:** {velocity:.2f} m/s\n\n{v_status}")
    st.markdown(f"- **Major Loss (แรงเสียดทาน):** {major_loss:.2f} ม.")
    st.markdown(f"- **Minor Loss (อุปกรณ์):** {minor_loss:.2f} ม.")
    st.markdown(f"- **รวมสูญเสียทั้งหมด:** **{total_loss:.2f} ม.**")

with res2:
    st.markdown("### สรุปพลังงานปั๊ม")
    st.success(f"**เฮดรวม (TDH):** {tdh:.2f} เมตร")
    st.markdown(f"- **กำลังไฮดรอลิก:** {hydraulic_power:.2f} kW")
    st.markdown(f"- **กำลังเพลาปั๊ม (Eff 75%):** {shaft_power:.2f} kW")
    st.markdown(f"- **ขนาดมอเตอร์แนะนำ:** **{motor_power_rec:.2f} kW**")

# กราฟ
st.markdown("---")
st.subheader("4. 📈 กราฟจุดทำงานของปั๊ม (Pump & System Curve)")
fig, ax = plt.subplots(figsize=(8, 4))
flows = np.linspace(1, max(q_m3h * 1.6, 120), 50)
pump_head_curve = (tdh * 1.4) - 0.003 * (flows ** 2)
system_head_curve = delta_z + h_press + (total_loss / (q_m3h ** 2)) * (flows ** 2)

ax.plot(flows, pump_head_curve, label="Pump Curve", color="blue", linewidth=2)
ax.plot(flows, system_head_curve, label="System Curve", color="red", linewidth=2)
ax.plot(q_m3h, tdh, marker="o", markersize=8, color="green", label=f"Duty Point ({q_m3h} m³/h, {tdh:.1f} m)")
ax.set_xlabel("Flow Rate (m³/h)")
ax.set_ylabel("Head (m)")
ax.grid(True, linestyle="--", alpha=0.6)
ax.legend()
st.pyplot(fig)

# หลักการ
st.markdown("---")
st.subheader("6. 📚 หลักการคำนวณมาตรฐาน")
st.markdown("""
- **ความเร็วในท่อ:** V = 4Q / (pi * D²)
- **Hazen-Williams (รองรับท่อเหล็ก C=120):** hf = 10.67 * Q^1.852 * D^-4.87 * C^-1.852 * L
- **Minor Loss:** hm = K * V^2 / (2g)
- **TDH:** ΔZ + H_pressure + hf + hm
""")
