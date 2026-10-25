import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Water Pipe Design VSD", page_icon="🚰", layout="wide")

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

st.title("🚰 โปรแกรมช่วยออกแบบระบบท่อส่งน้ำ (รองรับ VSD)")
st.markdown("**สำหรับอุตสาหกรรมน้ำดื่มและระบบสูบจ่ายน้ำ** — กราฟเส้นประ VSD ตรงกับค่าความดันเป้าหมายที่ตั้งไว้")
st.markdown("---")

# ส่วนข้อมูลตั้งต้น
st.subheader("1. ⚙️ ข้อมูลตั้งต้นระบบ (Inputs)")
col_in1, col_in2 = st.columns(2)

with col_in1:
    pipe_type = st.selectbox(
        "เลือกประเภทท่อ / วัสดุ", 
        [
            "ท่อเหล็กทั่วไป (Steel Pipe - C=120)", 
            "ท่อ Sanitary (Stainless SMS/DIN - C=150)",
            "สแตนเลสงานระบบทั่วไป (SS304 - C=150)",
            "PVC (C=140)", 
            "HDPE (C=130)"
        ]
    )
    
    if "ท่อเหล็กทั่วไป" in pipe_type:
        c_factor = 120
        pipe_sizes = {
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
    elif "Sanitary" in pipe_type:
        c_factor = 150
        pipe_sizes = {
            "1.5 นิ้ว Sanitary (ID: 35.6 มม.)": 35.6,
            "2 นิ้ว Sanitary (ID: 47.6 มม.)": 47.6,
            "2.5 นิ้ว Sanitary (ID: 60.2 มม.)": 60.2,
            "3 นิ้ว Sanitary (ID: 72.3 มม.)": 72.3,
            "4 นิ้ว Sanitary (ID: 97.4 มม.)": 97.4,
            "6 นิ้ว Sanitary (ID: 146.8 มม.)": 146.8,
            "8 นิ้ว Sanitary (ID: 194.7 มม.)": 194.7,
            "10 นิ้ว Sanitary (ID: 243.8 มม.)": 243.8,
            "12 นิ้ว Sanitary (ID: 292.1 มม.)": 292.1
        }
    else:
        c_factor = 150 if "สแตนเลส" in pipe_type else (140 if "PVC" in pipe_type else 130)
        pipe_sizes = {
            "2 นิ้ว (ID: 54.8 มม.)": 54.8,
            "2.5 นิ้ว (ID: 62.7 มม.)": 62.7,
            "3 นิ้ว (ID: 77.9 มม.)": 77.9,
            "4 นิ้ว (ID: 102.2 มม.)": 102.2,
            "6 นิ้ว (ID: 154.1 มม.)": 154.1,
            "8 นิ้ว (ID: 202.7 มม.)": 202.7,
            "10 นิ้ว (ID: 254.5 มม.)": 254.5,
            "12 นิ้ว (ID: 303.2 มม.)": 303.2
        }

    selected_pipe_name = st.selectbox("ขนาดเส้นผ่านศูนย์กลางท่อ", list(pipe_sizes.keys()), index=min(1, len(pipe_sizes)-1))
    d_mm = pipe_sizes[selected_pipe_name]
    
    q_m3h = st.number_input("อัตราการไหลออกแบบ (Q_design) [m³/h]", value=35.0, min_value=1.0)

with col_in2:
    pipe_length = st.number_input("ความยาวท่อรวม (L) [เมตร]", value=100.0, min_value=0.1)
    delta_z = st.number_input("ความต่างระดับ (ΔZ) [เมตร]", value=10.0)
    
    control_mode = st.selectbox(
        "โหมดการควบคุมปั๊ม (Control Mode)",
        [
            "VSD Constant Pressure Control (ควบคุมแรงดันคงที่)",
            "Fixed Speed / Throttle Valve Control (รอบคงที่)"
        ]
    )
    
    if "VSD" in control_mode:
        h_press = st.number_input("🎯 ค่าความดันเป้าหมายที่ต้องการควบคุม (VSD Target Pressure) [เมตรน้ำ]", value=22.0, min_value=0.0)
    else:
        h_press = st.number_input("ความดันปลายทางเป้าหมาย [เมตรน้ำ]", value=20.0, min_value=0.0)

st.markdown("##### อุปกรณ์ประกอบท่อ (Fittings)")
f1, f2, f3 = st.columns(3)
with f1:
    elbow_90 = st.number_input("ข้องอ 90°", value=4, min_value=0)
with f2:
    valve = st.number_input("วาล์ว", value=2, min_value=0)
with f3:
    tee = st.number_input("สามทาง", value=1, min_value=0)

st.markdown("---")

# คำนวณทางวิศวกรรมที่ Duty Point
d_m = d_mm / 1000.0
area = np.pi * (d_m ** 2) / 4.0
velocity = (q_m3h / 3600.0) / area
major_loss = 10.67 * (q_m3h ** 1.852) * (d_mm ** -4.87) * (c_factor ** -1.852) * pipe_length
k_total = (elbow_90 * 0.9) + (valve * 0.2) + (tee * 1.0)
minor_loss = k_total * (velocity ** 2) / (2 * 9.81)
total_loss = major_loss + minor_loss

if "VSD" in control_mode:
    # ในระบบ VSD Constant Pressure ที่ปลายทาง หัวปั๊มต้องจ่าย Head เท่ากับ ΔZ + H_target + Head Loss ในท่อ
    tdh = delta_z + h_press + total_loss
    vsd_target_head = delta_z + h_press # ระดับเส้นประสีแดงที่จะแสดง (Static + Target Pressure)
else:
    tdh = delta_z + h_press + total_loss
    vsd_target_head = tdh

rho, g = 1000.0, 9.81
hydraulic_power = (rho * g * (q_m3h / 3600.0) * tdh) / 1000.0
shaft_power = hydraulic_power / 0.75
motor_power_rec = shaft_power * 1.2

# แสดงผลลัพธ์
st.subheader("3. 📊 ผลการคำนวณและสรุปข้อมูลปั๊ม")
res1, res2 = st.columns(2)

with res1:
    st.markdown("### ข้อมูลท่อและการสูญเสีย")
    if 1.0 <= velocity <= 2.0:
        v_status = "✅ อยู่ในช่วงแนะนำ (1.0 - 2.0 m/s)"
    elif velocity < 1.0:
        v_status = "⚠️ ต่ำกว่าเกณฑ์แนะนำ"
    else:
        v_status = "⚠️ สูงกว่าเกณฑ์แนะนำ"
        
    st.info(f"**โหมดควบคุม:** {'VSD Constant Pressure' if 'VSD' in control_mode else 'Fixed Speed'}\n\n**ขนาดท่อ:** {selected_pipe_name}\n\n**ความเร็วในท่อ:** {velocity:.2f} m/s\n\n{v_status}")
    st.markdown(f"- **Major Loss ที่จุดออกแบบ:** {major_loss:.2f} ม.")
    st.markdown(f"- **Minor Loss ที่จุดออกแบบ:** {minor_loss:.2f} ม.")
    st.markdown(f"- **TDH สูงสุดที่ออกแบบ:** **{tdh:.2f} ม.**")

with res2:
    st.markdown("### สรุปพลังงานปั๊ม")
    st.success(f"**เฮดรวมสูงสุด (Max TDH):** {tdh:.2f} เมตร")
    st.markdown(f"- **กำลังไฮดรอลิก:** {hydraulic_power:.2f} kW")
    st.markdown(f"- **กำลังเพลาปั๊ม (Eff 75%):** {shaft_power:.2f} kW")
    st.markdown(f"- **ขนาดมอเตอร์แนะนำ:** **{motor_power_rec:.2f} kW**")
    if "VSD" in control_mode:
        st.caption(f"💡 ควบคุมความดันปลายทางคงที่ที่ระดับ {h_press} เมตรน้ำ ด้วยระบบ VSD")

# กราฟ Pump & System Curve (แก้ไขเส้นประ VSD ให้ตรงกับค่าที่ตั้งไว้)
st.markdown("---")
st.subheader("4. 📈 กราฟจุดทำงานของปั๊มและระบบ (System & VSD Curves)")

fig, ax = plt.subplots(figsize=(8, 4.5))
max_flow_graph = max(q_m3h * 1.4, 50)
flows = np.linspace(0, max_flow_graph, 150)

if "VSD" in control_mode:
    # เส้นประสีแดงแสดงระดับ Static Head + Target Pressure ตามที่ผู้ใช้กรอก
    system_head_curve = np.full_like(flows, vsd_target_head)
    shutoff_head = tdh * 1.35
    ax.plot(flows, system_head_curve, label=f"VSD Target Pressure ({delta_z} + {h_press} = {vsd_target_head} m)", color="red", linewidth=2.5, linestyle="--")
    
    pump_100 = shutoff_head - (shutoff_head - tdh) * ((flows / q_m3h) ** 2)
    ax.plot(flows, pump_100, label="Pump Curve (100% Speed)", color="blue", linewidth=2)
    ax.plot(flows, pump_100 * (0.85**2), label="Pump Curve (85% Speed)", color="blue", alpha=0.6, linestyle=":")
    ax.plot(flows, pump_100 * (0.70**2), label="Pump Curve (70% Speed)", color="blue", alpha=0.3, linestyle=":")
else:
    static_head = delta_z + h_press
    loss_coefficient = total_loss / (q_m3h ** 1.852) if q_m3h > 0 else 0
    system_head_curve = static_head + loss_coefficient * (flows ** 1.852)
    shutoff_head = tdh * 1.35
    pump_head_curve = shutoff_head - (shutoff_head - tdh) * ((flows / q_m3h) ** 2)
    
    ax.plot(flows, pump_head_curve, label="Pump Curve", color="blue", linewidth=2)
    ax.plot(flows, system_head_curve, label="System Curve", color="red", linewidth=2)

ax.plot(q_m3h, tdh, marker="o", markersize=8, color="green", label=f"Design Duty Point ({q_m3h:.1f} m³/h, {tdh:.1f} m)")

ax.set_xlim(left=0, right=max_flow_graph)
ax.set_ylim(bottom=0, top=max(tdh * 1.3, 30))
ax.set_xlabel("Flow Rate (m³/h)")
ax.set_ylabel("Head (m)")
ax.grid(True, linestyle="--", alpha=0.6)
ax.legend(loc="upper right", fontsize=9)
st.pyplot(fig)

# 5. ตารางข้อมูลการเปลี่ยนแปลง Pressure กับ Flow Rate
st.markdown("---")
st.subheader("5. 📋 ตารางแสดงการเปลี่ยนแปลง Pressure และ Head ตาม Flow Rate")

table_flows = np.linspace(0, q_m3h * 1.4, 8)
table_data = []

for f in table_flows:
    if f == 0:
        v_t = 0.0
        tot_loss_t = 0.0
        sys_head_t = delta_z + h_press if "VSD" in control_mode else delta_z + h_press
    else:
        v_t = (f / 3600.0) / area
        maj_t = 10.67 * (f ** 1.852) * (d_mm ** -4.87) * (c_factor ** -1.852) * pipe_length
        min_t = k_total * (v_t ** 2) / (2 * 9.81)
        tot_loss_t = maj_t + min_t
        if "VSD" in control_mode:
            sys_head_t = delta_z + h_press + tot_loss_t
        else:
            sys_head_t = delta_z + h_press + tot_loss_t
            
    pressure_bar = sys_head_t / 10.2
    
    table_data.append({
        "Flow Rate (m³/h)": round(f, 2),
        "Velocity (m/s)": round(v_t, 2),
        "Total Head Loss (m)": round(tot_loss_t, 2),
        "System Head / TDH (m)": round(sys_head_t, 2),
        "Est. Pressure (bar)": round(pressure_bar, 2)
    })

df_result = pd.DataFrame(table_data)
st.dataframe(df_result, use_container_width=True)

# หลักการ
st.markdown("---")
st.subheader("6. 📚 หลักการคำนวณมาตรฐาน")
st.markdown("""
- **ความเร็วในท่อ:** V = 4Q / (pi * D²)
- **Hazen-Williams:** hf = 10.67 * Q^1.852 * D^-4.87 * C^-1.852 * L
- **VSD Target Pressure:** เส้นประแสดงค่าความดันเป้าหมายรวมกับความต่างระดับ ($\Delta Z + H_{\text{target}}$) อย่างถูกต้องตรงตามค่าที่ตั้งไว้
""")
