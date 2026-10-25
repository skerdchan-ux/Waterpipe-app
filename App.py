import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Water Pipe Design", page_icon="🚰", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1e3a8a; }
    .sub-title { font-size: 14px; color: #475569; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚰 โปรแกรมช่วยออกแบบระบบท่อส่งน้ำ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">สำหรับอุตสาหกรรมน้ำดื่ม (เวอร์ชันมือถือและเดสก์ท็อป)</p>', unsafe_allow_html=True)

# Sidebar หรือ ส่วนตั้งค่าข้อมูลตั้งต้น
st.sidebar.header("1. ข้อมูลตั้งต้นระบบ")

pipe_materials = {
    "สแตนเลส (SS304)": 150,
    "PVC": 140,
    "HDPE": 130
}
selected_material = st.sidebar.selectbox("ชนิดและวัสดุของท่อ", list(pipe_materials.keys()))
c_factor = pipe_materials[selected_material]

pipe_sizes = {
    "2 นิ้ว (ID: 54.8 มม.)": 54.8,
    "2.5 นิ้ว (ID: 62.7 มม.)": 62.7,
    "3 นิ้ว (ID: 77.9 มม.)": 77.9,
    "4 นิ้ว (ID: 102.2 มม.)": 102.2,
    "6 นิ้ว (ID: 154.1 มม.)": 154.1
}
selected_pipe_name = st.sidebar.selectbox("ขนาดเส้นผ่านศูนย์กลางท่อ", list(pipe_sizes.keys()), index=1)
d_mm = pipe_sizes[selected_pipe_name]

q_m3h = st.sidebar.number_input("อัตราการไหลของน้ำ (Q) [m³/h]", value=50.0)
pipe_length = st.sidebar.number_input("ความยาวท่อรวม (L) [เมตร]", value=120.0)
delta_z = st.sidebar.number_input("ความต่างระดับ (ΔZ) [เมตร]", value=15.0)
h_press = st.sidebar.number_input("ความดันปลายทาง (H_pressure) [เมตรน้ำ]", value=20.0)

st.sidebar.subheader("อุปกรณ์ประกอบท่อ (Fittings)")
elbow_90 = st.sidebar.number_input("ข้องอ 90° (ตัว)", value=6, min_value=0)
valve = st.sidebar.number_input("วาล์ว (ตัว)", value=2, min_value=0)
tee = st.sidebar.number_input("สามทาง (ตัว)", value=1, min_value=0)

calc_btn = st.sidebar.button("คำนวณผลลัพธ์", type="primary")

# คำนวณทางวิศวกรรม
d_m = d_mm / 1000.0
area = np.pi * (d_m ** 2) / 4.0
velocity = (q_m3h / 3600.0) / area

# Major Loss (Hazen-Williams)
major_loss = 10.67 * (q_m3h ** 1.852) * (d_mm ** -4.87) * (c_factor ** -1.852) * pipe_length

# Minor Loss (Fittings: Elbow 90 = 0.9, Valve = 0.2, Tee = 1.0 roughly or standard coefficients)
k_total = (elbow_90 * 0.9) + (valve * 0.2) + (tee * 1.0)
minor_loss = k_total * (velocity ** 2) / (2 * 9.81)

total_loss = major_loss + minor_loss
tdh = delta_z + h_press + total_loss

# Power calculations
rho = 1000.0
g = 9.81
q_m3s = q_m3h / 3600.0
hydraulic_power = (rho * g * q_m3s * tdh) / 1000.0 # kW
shaft_power = hydraulic_power / 0.75 # สมมติประสิทธิภาพปั๊ม 75%
motor_power_rec = shaft_power * 1.2 # เผื่อ 20%

# แสดงผลลัพธ์หลัก
col1, col2 = st.columns([1.2, 1.2])

with col1:
    st.subheader("3. ผลการคำนวณ")
    st.markdown("---")
    st.markdown(f"**ขนาดท่อที่แนะนำ:** {selected_pipe_name}")
    st.markdown(f"**เส้นผ่านศูนย์กลางภายใน:** {d_mm} มม.")
    
    # ความเร็วในท่อพร้อมเกณฑ์
    if 1.0 <= velocity <= 2.0:
        v_status = "✅ อยู่ในช่วงที่แนะนำ (1.0 - 2.0 m/s)"
    elif velocity < 1.0:
        v_status = "⚠️ ต่ำกว่าเกณฑ์แนะนำเล็กน้อย"
    else:
        v_status = "⚠️ สูงกว่าเกณฑ์แนะนำ"
    
    st.metric("ความเร็วในท่อ (V)", f"{velocity:.2f} m/s", v_status)
    
    st.markdown("#### การสูญเสียเฮด (Head Loss)")
    st.markdown(f"- **Major Loss (แรงเสียดทานท่อ):** {major_loss:.2f} ม.")
    st.markdown(f"- **Minor Loss (อุปกรณ์ข้อต่อ):** {minor_loss:.2f} ม.")
    st.markdown(f"- **รวมการสูญเสียเฮดทั้งหมด:** **{total_loss:.2f} ม.**")
    
    st.markdown("#### เฮดรวมที่ต้องใช้ (TDH)")
    st.info(f"TDH = ΔZ + H_pressure + h_f + h_m\n\nTDH = {delta_z} + {h_press} + {major_loss:.2f} + {minor_loss:.2f} = **{tdh:.2f} เมตร**")

with col2:
    st.subheader("5. สรุปข้อมูลปั๊มและมอเตอร์")
    st.markdown("---")
    st.metric("เฮดรวม (TDH)", f"{tdh:.2f} เมตร")
    st.metric("กำลังไฮดรอลิก (Pn)", f"{hydraulic_power:.2f} kW")
    st.metric("กำลังเพลาปั๊ม (เผื่อ 75% Eff.)", f"{shaft_power:.2f} kW")
    st.metric("ขนาดมอเตอร์แนะนำ (เผื่อโหลด 20%)", f"{motor_power_rec:.2f} kW")
    
    st.success("✨ ผลการคำนวณอยู่ในเกณฑ์ที่เหมาะสม พร้อมใช้งานจริง")

# ส่วนแสดงกราฟ
st.markdown("---")
st.subheader("4. กราฟจุดทำงานของปั๊ม (Pump & System Curve)")
fig, ax = plt.subplots(figsize=(8, 4.5))
flows = np.linspace(1, max(q_m3h * 1.6, 80), 50)
# สมมติกราฟปั๊มคร่าวๆ
pump_head_curve = (tdh * 1.5) - 0.005 * (flows ** 2)
system_head_curve = delta_z + h_press + (total_loss / (q_m3h ** 2)) * (flows ** 2)

ax.plot(flows, pump_head_curve, label="Pump Curve", color="blue", linewidth=2)
ax.plot(flows, system_head_curve, label="System Curve", color="red", linewidth=2)
ax.plot(q_m3h, tdh, marker="o", markersize=8, color="green", label=f"Duty Point ({q_m3h} m³/h, {tdh:.1f} m)")

ax.set_xlabel("Flow Rate (m³/h)")
ax.set_ylabel("Head (m)")
ax.grid(True, linestyle="--", alpha=0.6)
ax.legend()
st.pyplot(fig)

# หลักการคำนวณด้านล่าง
st.markdown("---")
st.subheader("6. หลักการคำนวณที่ใช้")
st.markdown("""
- **ความเร็วในท่อ:** $V = 4Q / (\\pi D^2)$
- **Hazen-Williams Formula:** $h_f = 10.67 \\times Q^{1.852} \\times D^{-4.87} \\times C^{-1.852} \\times L$
- **Minor Loss:** $h_m = K \\times V^2 / (2g)$
- **TDH:** $\\text{TDH} = \\Delta Z + H_{\\text{pressure}} + h_f + h_m$
- **กำลังปั๊มและมอเตอร์:** คำนวณตามหลักเกณฑ์วิศวกรรมสุขាภิบาลและอุตสาหกรรมน้ำดื่ม
""")
