import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="منصة الدفاع المدني الذكية", layout="wide")

st.title("منصة ذكية متكاملة لرصد السيول والزلازل")
st.caption("نموذج متكامل يجمع المراقبة، التنبيهات، التوقعات، والمحاكاة – قابل للتطوير وربطه بـ NASA و Google Earth Engine.")

WADIS = [
    {"name": "وادي بيشة", "risk_sensitivity": "عالي"},
    {"name": "وادي تربة", "risk_sensitivity": "متوسط"},
    {"name": "وادي رقم 3", "risk_sensitivity": "منخفض"},
]

def assess_risk(rain: float) -> str:
    if rain < 10:
        return "منخفض"
    elif 10 <= rain < 30:
        return "متوسط"
    elif 30 <= rain < 50:
        return "مرتفع"
    else:
        return "حرج"

def mock_rain_data():
    data = []
    for w in WADIS:
        rain = round(random.uniform(0, 80), 1)
        data.append({
            "wadi": w["name"],
            "rain_rate_mm_h": rain,
            "risk_level": assess_risk(rain)
        })
    return pd.DataFrame(data)

def mock_quake_data():
    quakes = []
    for i in range(5):
        quakes.append({
            "location": f"منطقة زلزال {i+1}",
            "magnitude": round(random.uniform(2.5, 6.5), 1),
            "depth_km": round(random.uniform(5, 30), 1),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    return pd.DataFrame(quakes)

def mock_forecast_data(days=7):
    rows = []
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        rain = round(random.uniform(0, 50), 1)
        rows.append({"date": date, "expected_rain_mm": rain})
    return pd.DataFrame(rows)

role = st.sidebar.selectbox(
    "اختر نوع المستخدم",
    ["مستخدم عادي", "مراقب ميداني", "غرفة العمليات", "مدير النظام"]
)
st.sidebar.markdown(f"**الدور الحالي:** {role}")

tabs = st.tabs([
    "لوحة المراقبة", 
    "الأودية", 
    "التنبيهات", 
    "توقعات الأمطار", 
    "محاكاة السيول", 
    "الإعدادات المتقدمة"
])

rain_df = mock_rain_data()
quake_df = mock_quake_data()

with tabs[0]:
    st.subheader("لوحة مراقبة لحظية")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("عدد الأودية", len(WADIS))
        st.metric("أودية في خطر مرتفع/حرج", len(rain_df[rain_df["risk_level"].isin(["مرتفع", "حرج"])]))
    with col2:
        st.metric("عدد الزلازل المسجلة", len(quake_df))
        st.metric("زلازل قوية (≥ 4.5)", len(quake_df[quake_df["magnitude"] >= 4.5]))
    with col3:
        avg_rain = round(rain_df["rain_rate_mm_h"].mean(), 1)
        st.metric("متوسط شدة الأمطار", f"{avg_rain} مم/ساعة")
    st.markdown("### حالة الأودية الآن")
    st.dataframe(rain_df, use_container_width=True)
    st.markdown("### الزلازل المسجلة")
    st.dataframe(quake_df, use_container_width=True)

with tabs[1]:
    st.subheader("ملفات الأودية")
    selected_wadi = st.selectbox("اختر واديًا", [w["name"] for w in WADIS])
    wadi_rain = rain_df[rain_df["wadi"] == selected_wadi].iloc[0]
    st.markdown(f"### {selected_wadi}")
    st.write(f"شدة الأمطار الحالية: {wadi_rain['rain_rate_mm_h']} مم/ساعة")
    st.write(f"مستوى الخطر الحالي: {wadi_rain['risk_level']}")
    history = pd.DataFrame({
        "date": ["2022-04-10", "2023-08-21", "2024-03-05"],
        "event": ["سيل متوسط", "سيل قوي", "سيل خفيف"],
        "impact": ["إغلاق طريق فرعي", "أضرار في بعض المنازل", "لا أضرار كبيرة"]
    })
    st.markdown("#### تاريخ سيول (افتراضي)")
    st.table(history)

with tabs[2]:
    st.subheader("نظام التنبيهات")
    critical = rain_df[rain_df["risk_level"].isin(["مرتفع", "حرج"])]
    if critical.empty:
        st.success("لا توجد تنبيهات حرجة حاليًا.")
    else:
        st.error("🚨 تنبيهات حرجة للأودية التالية:")
        for _, row in critical.iterrows():
            st.error(
                f"⚠️ {row['wadi']} | الأمطار: {row['rain_rate_mm_h']} مم/ساعة | الخطر: {row['risk_level']}"
            )
    alerts_log = pd.DataFrame({
        "time": [datetime.now().strftime("%Y-%m-%d %H:%M")] * 3,
        "type": ["سيول", "زلازل", "سيول"],
        "level": ["حرج", "متوسط", "مرتفع"],
        "details": ["وادي بيشة", "منطقة زلزال 2", "وادي تربة"]
    })
    st.markdown("#### سجل تنبيهات (افتراضي)")
    st.table(alerts_log)

with tabs[3]:
    st.subheader("توقعات الأمطار")
    forecast_df = mock_forecast_data(days=7)
    st.line_chart(forecast_df.set_index("date")["expected_rain_mm"])
    st.table(forecast_df)
    st.info("يمكن لاحقًا ربط هذه التوقعات بنماذج طقس عالمية وبيانات NASA الفعلية.")

with tabs[4]:
    st.subheader("محاكاة السيول")
    sim_wadi = st.selectbox("اختر واديًا للمحاكاة", [w["name"] for w in WADIS])
    sim_rain = st.slider("كمية الأمطار المتوقعة (مم)", 0, 200, 50)
    st.write(f"الوادي: {sim_wadi}")
    st.write(f"كمية الأمطار في المحاكاة: {sim_rain} مم")
    if sim_rain < 50:
        st.success("المحاكاة: خطر منخفض، لا يتوقع سيل كبير.")
    elif 50 <= sim_rain < 120:
        st.warning("المحاكاة: خطر متوسط إلى مرتفع، احتمال سيول في بعض المناطق.")
    else:
        st.error("المحاكاة: خطر حرج، سيول قوية متوقعة في الوادي.")
    st.info("يمكن لاحقًا ربط هذه المحاكاة بنماذج هيدرولوجية حقيقية وتحليل تدفق باستخدام Google Earth Engine.")

with tabs[5]:
    st.subheader("الإعدادات المتقدمة")
    st.markdown("### ربط مع NASA APIs / Earthdata")
    st.markdown("""
    - إعداد مفاتيح الوصول (API Keys).
    - اختيار منتجات الأمطار (مثل GPM IMERG).
    - ضبط فترة التحديث (كل 30 دقيقة / كل ساعة).
    """)
    st.markdown("### ربط مع Google Earth Engine")
    st.markdown("""
    - تحميل بيانات DEM للتضاريس.
    - حساب الانحدار (Slope) وتحديد الأودية.
    - دمج الأمطار مع التضاريس لتقدير خطر السيول.
    """)
    st.markdown("### نظام صلاحيات المستخدمين")
    st.markdown("""
    - مدير النظام: إدارة الإعدادات والتقارير.
    - غرفة العمليات: مراقبة وتنبيهات.
    - مراقب ميداني: إدخال ملاحظات من الميدان.
    - مستخدم عادي: عرض المعلومات العامة فقط.
    """)
    st.info("هذا القسم تصميمي الآن، ويمكن تحويله لاحقًا إلى إعدادات فعلية مع قاعدة بيانات وتسجيل دخول.")
