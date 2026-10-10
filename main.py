import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import textwrap

import importlib
import database as db

db = importlib.reload(db)


st.set_page_config(
    page_title="Health Space | 我的健康空间",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="expanded",
)




st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Nunito', 'Microsoft YaHei', sans-serif;
    }

    .stApp {
        background: var(--app-bg);
        color: #27332B;
    }

    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        border-right: 1px solid #DDE8D8;
    }

    [data-testid="stSidebar"] * {
        color: #304035;
    }

    .main-title {
        font-size: 2.55rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.25rem;
    }

    .subtitle {
        font-size: 1.03rem;
        color: #708072;
        margin-bottom: 1.4rem;
    }

    .hero-card {
        background: linear-gradient(135deg, var(--hero-soft) 0%, #F5F1FB 100%);
        border: 1px solid #DCE8D7;
        border-radius: 28px;
        padding: 28px 30px;
        box-shadow: 0 10px 30px rgba(77, 98, 79, 0.07);
    }

    .hero-label {
        font-size: 0.84rem;
        color: #708072;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 700;
    }

    .hero-bmi {
        font-size: 4rem;
        line-height: 1;
        font-weight: 800;
        margin: 10px 0 6px 0;
        color: #30473A;
    }

    .status-pill {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 999px;
        font-size: 0.95rem;
        font-weight: 700;
        margin-top: 4px;
    }

    .pill-green {
        background: #DCEEDC;
        color: #3F6847;
    }

    .pill-yellow {
        background: #FFF0C9;
        color: #8A6A17;
    }

    .pill-orange {
        background: #FFE0C7;
        color: #9A5C22;
    }

    .pill-red {
        background: #FFD9D9;
        color: #994343;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5EBE2;
        border-radius: 20px;
        padding: 20px 22px;
        height: 100%;
        box-shadow: 0 8px 24px rgba(50, 66, 55, 0.05);
    }

    .metric-title {
        color: #7B887E;
        font-size: 0.85rem;
        margin-bottom: 6px;
        font-weight: 600;
    }

    .metric-value {
        color: #2F4336;
        font-size: 1.8rem;
        font-weight: 800;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 800;
        margin: 1.25rem 0 0.8rem 0;
        color: #2E4034;
    }

    .soft-card {
        background: #FFFFFF;
        border: 1px solid #E7ECE4;
        border-radius: 20px;
        padding: 20px;
        height: 100%;
    }

    .persona-card {
        background: linear-gradient(135deg, #FFFDF7 0%, #F5F1FB 100%);
        border: 1px solid #EAE1F3;
        border-radius: 22px;
        padding: 24px;
        height: 100%;
    }

    .persona-name {
        font-size: 1.45rem;
        font-weight: 800;
        color: #4F5C72;
    }

    .persona-desc {
        color: #707985;
        line-height: 1.7;
        margin-top: 8px;
    }

    .food-card {
        background: #FFFFFF;
        border: 1px solid #E5EBE2;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        min-height: 150px;
        box-shadow: 0 6px 18px rgba(50, 66, 55, 0.04);
    }

    .food-emoji {
        font-size: 2rem;
        margin-bottom: 8px;
    }

    .food-title {
        font-weight: 800;
        color: #35443A;
        margin-bottom: 5px;
    }

    .food-text {
        color: #758178;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .challenge-item {
        background: #FFFFFF;
        border: 1px solid #E6ECE4;
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    .small-muted {
        color: #7A857C;
        font-size: 0.9rem;
    }

    .report-card {
        background: #FFFFFF;
        border: 1px solid #E4EAE1;
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 10px 28px rgba(50, 66, 55, 0.05);
    }

    .footer {
        color: #8C978E;
        font-size: 0.82rem;
        text-align: center;
        margin-top: 35px;
        margin-bottom: 15px;
    }

    .stButton > button {
        border-radius: 14px;
        border: 1px solid #D7E2D3;
        font-weight: 700;
        padding: 0.55rem 1rem;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E5EBE2;
        padding: 15px;
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Session State 初始化
# =========================

if "profile" not in st.session_state:
    st.session_state.profile = None

if "onboarding_done" not in st.session_state:
    st.session_state.onboarding_done = False

if "theme" not in st.session_state:
    st.session_state.theme = {
        "name": "鼠尾草绿",
        "primary": "#7BAE8B",
        "secondary": "#9B8AC4",
        "soft": "#EEF4EA",
        "bg": "#F7F8F3",
    }

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "records" not in st.session_state:
    st.session_state.records = []

if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "喝水 至少1500 ml": False,
        "步行 6000➕ 步": False,
        "吃够  水果和蔬菜": False,
        "23:30 前睡觉": False,
    }


# =========================
# 主题颜色
# =========================

st.markdown(
    f"""
    <style>
    :root {{
        --app-bg: {st.session_state.theme["bg"]};
        --sidebar-bg: {st.session_state.theme["soft"]};
        --hero-soft: {st.session_state.theme["soft"]};
        --primary: {st.session_state.theme["primary"]};
        --secondary: {st.session_state.theme["secondary"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# BMI 相关函数
# =========================

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def bmi_status(bmi):
    if bmi < 18.5:
        return "偏瘦", "yellow"
    elif bmi < 24:
        return "正常", "green"
    elif bmi < 28:
        return "超重", "orange"
    return "肥胖", "red"


def healthy_weight_range(height_cm):
    h = height_cm / 100
    return round(18.5 * h * h, 1), round(23.9 * h * h, 1)


def bmi_bar_width(bmi):
    return max(4, min(98, (bmi / 35) * 100))


def get_persona(gender, bmi):
    if bmi < 18.5:
        if gender == "女":
            return "🌷 温和增重型", "更适合通过规律三餐、优质蛋白和适量力量训练改善体型与营养状态。"
        return "💪 肌力补给型", "更适合通过充足蛋白质、规律进食和力量训练提升体能与肌肉量。"

    if bmi < 24:
        if gender == "女":
            return "🥑 均衡生活家", "你的 BMI 处于正常区间，可以把重点放在稳定饮食、睡眠和体态管理上。"
        return "🏃 活力运动派", "你的 BMI 处于正常区间，可以把重点放在运动习惯、心肺能力和力量训练上。"

    if bmi < 28:
        if gender == "女":
            return "🌿 轻盈调整派", "更适合温和控制能量摄入，同时关注蛋白质、蔬菜和规律运动，不建议极端节食。"
        return "🔥 活力重塑派", "更适合逐步减少高热量饮食，同时增加力量训练和日常活动量。"

    if gender == "女":
        return "🌱 健康重启者", "建议从饮食结构、日常活动和睡眠三个方面同时做小幅调整，避免快速减重。"

    return "🚀 健康重启者", "建议逐步改善饮食结构和运动习惯，把目标放在长期体重与体能管理上。"


# =========================
# 饮食推荐
# =========================

def diet_plan(status, gender):
    female = {
        "偏瘦": [
            ("🥛", "早餐", "牛奶 + 鸡蛋 + 全麦吐司 + 香蕉"),
            ("🍗", "午餐", "米饭 + 鸡胸肉 + 西兰花 + 玉米"),
            ("🐟", "晚餐", "杂粮饭 + 鱼肉 + 青菜 + 豆腐"),
            ("🥜", "加餐", "酸奶 + 坚果"),
        ],
        "正常": [
            ("🥚", "早餐", "鸡蛋 + 牛奶 + 全麦吐司 + 蓝莓"),
            ("🥗", "午餐", "米饭 + 鱼肉 + 两种蔬菜"),
            ("🍲", "晚餐", "杂粮饭 + 瘦肉 + 绿叶菜"),
            ("🍎", "加餐", "水果 / 无糖酸奶"),
        ],
        "超重": [
            ("🥚", "早餐", "鸡蛋 + 无糖豆浆 + 全麦面包"),
            ("🥦", "午餐", "半碗杂粮饭 + 鸡胸肉 + 大量蔬菜"),
            ("🐟", "晚餐", "少量主食 + 鱼肉 + 青菜"),
            ("🍓", "加餐", "低糖水果"),
        ],
        "肥胖": [
            ("🥚", "早餐", "鸡蛋 + 无糖牛奶 + 全麦面包"),
            ("🥗", "午餐", "小份主食 + 鱼肉 + 大量蔬菜"),
            ("🍲", "晚餐", "少量主食 + 豆制品 + 青菜"),
            ("🍎", "加餐", "低糖水果，减少夜宵哦~"),
        ],
    }

    male = {
        "偏瘦": [
            ("🥛", "早餐", "牛奶 + 2个鸡蛋 + 全麦面包 + 香蕉"),
            ("🍗", "午餐", "米饭 + 鸡腿/牛肉 + 西兰花 + 玉米"),
            ("🐟", "晚餐", "杂粮饭 + 鱼肉 + 青菜 + 豆腐"),
            ("🥜", "加餐", "高蛋白酸奶 + 坚果"),
        ],
        "正常": [
            ("🍳", "早餐", "鸡蛋 + 牛奶 + 全麦面包 + 水果"),
            ("🥩", "午餐", "米饭 + 牛肉/鸡肉 + 两种蔬菜"),
            ("🐟", "晚餐", "杂粮饭 + 鱼肉 + 绿叶菜"),
            ("🍌", "加餐", "香蕉 / 酸奶"),
        ],
        "超重": [
            ("🥚", "早餐", "鸡蛋 + 无糖豆浆 + 全麦面包"),
            ("🥗", "午餐", "适量杂粮饭 + 瘦牛肉 + 大量蔬菜"),
            ("🐟", "晚餐", "少量主食 + 鱼肉 + 青菜"),
            ("🍎", "加餐", "水果或无糖酸奶"),
        ],
        "肥胖": [
            ("🥚", "早餐", "鸡蛋 + 无糖牛奶 + 全麦面包"),
            ("🥗", "午餐", "小份主食 + 鸡胸肉 + 大量蔬菜"),
            ("🍲", "晚餐", "少量主食 + 豆腐/鱼肉 + 青菜"),
            ("🍓", "加餐", "低糖水果，减少夜宵哦~"),
        ],
    }

    return (female if gender == "女" else male)[status]


# =========================
# 状态建议
# =========================

def status_advice(status, gender):
    advice = {
        "偏瘦": [
            "三餐规律，再忙也要好好吃饭",
            "适当增加优质蛋白，如牛奶、鸡蛋、鱼肉、豆制品，蛋白质可以长肌肉哦",
            "增加坚果、酸奶等健康加餐，而不是依赖高糖高油食品！",
            "可以配合适量力量训练，提升肌肉量，身体线条会更流畅好看哦",
        ],
        "正常": [
            "继续保持规律三餐，不建议因为追求更瘦而盲目节食！你现在的样子是最好哒",
            "保证主食、蛋白质、蔬菜和水果的基本平衡，好好吃饭哦",
            "减少高糖饮料和高加工食品的摄入，会更健康哦",
            "保持稳定运动和睡眠习惯",
        ],
        "超重": [
            "优先减少含糖饮料、奶茶、炸物和高热量零食，超级长肉！",
            "主食可以适当增加粗粮比例，但不要极端断碳水，比起瘦得快不如瘦的稳定",
            "每餐增加蔬菜和优质蛋白的占比，体脂率马上说byeヾ(•ω•`)o",
            "把快走、骑行等中等强度活动加入日常生活",
        ],
        "肥胖": [
            "建议以渐进式生活方式调整为主，不采用极端节食，慢慢来~",
            "减少含糖饮料、夜宵和高油食品",
            "增加蔬菜、全谷物和优质蛋白的比例，坚持下来会发现维度变小哦",
            "如有持续体重管理需求，建议咨询专业医生或营养师！",
        ],
    }

    base = advice[status].copy()

    if gender == "男" and status in ("正常", "超重"):
        base.append("如果有运动习惯，可适当加入力量训练，关注体能而不是只看体重数字。")
    elif gender == "女" and status in ("正常", "超重"):
        base.append("关注规律作息和均衡饮食，不建议为了追求更低体重而长期极低热量饮食。")
    elif gender == "女" and status == "偏瘦":
        base.append("可以增加奶制品、蛋类和豆制品等营养密度较高的食物。")
    elif gender == "男" and status == "偏瘦":
        base.append("可结合基础力量训练与充足蛋白质摄入，帮助增加肌肉量。")

    return base


# =========================
# 健康指数
# =========================

def calculate_health_score(bmi):
    if bmi < 18.5:
        return max(68, int(90 - (18.5 - bmi) * 8))

    if bmi < 24:
        distance = abs(bmi - 21.2)
        return int(max(84, 95 - distance * 4))

    if bmi < 28:
        return int(max(72, 84 - (bmi - 24) * 3.5))

    return max(60, int(70 - (bmi - 28) * 2.5))


# =========================
# 保存健康结果
# =========================

def save_result():
    p = st.session_state.profile

    bmi = calculate_bmi(p["height"], p["weight"])
    status, color = bmi_status(bmi)

    result = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "gender": p["gender"],
        "age": p["age"],
        "height": p["height"],
        "weight": p["weight"],
        "bmi": bmi,
        "status": status,
        "score": calculate_health_score(bmi),
    }

    # 保存到数据库
    db.save_health_record(
        p["name"],
        result
    )

    # 当前页面继续使用 session_state
    st.session_state.latest_result = result
    st.session_state.records.append(result)

    return result


# ============================================================
# 第一次建档
# ============================================================

if not st.session_state.onboarding_done:

    st.sidebar.markdown("## 🍀 Health Space(*^▽^*)")
    st.sidebar.caption("第一次使用，请先完成你的健康建档！")

    st.markdown(
        '<div class="main-title">先全面认识自己，再开始管理健康 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">只需要两步：告诉我你的基本情况，再告诉我你想改善什么！</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">① 建立我的健康档案</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:

        # 初始化建档输入框状态
        if "onboarding_gender" not in st.session_state:
            st.session_state.onboarding_gender = "女"

        if "onboarding_age" not in st.session_state:
            st.session_state.onboarding_age = 19

        if "onboarding_height" not in st.session_state:
            st.session_state.onboarding_height = 165.0

        if "onboarding_weight" not in st.session_state:
            st.session_state.onboarding_weight = 50.0

        if "existing_profile" not in st.session_state:
            st.session_state.existing_profile = None


        # 输入姓名后自动读取数据库
        def load_profile():
            user_name = st.session_state.onboarding_name.strip()

            if user_name:
                profile = db.get_profile(user_name)

                if profile:
                    st.session_state.onboarding_gender = profile[1]
                    st.session_state.onboarding_age = int(profile[2])
                    st.session_state.onboarding_height = float(profile[3])
                    st.session_state.onboarding_weight = float(profile[4])
                    st.session_state.existing_profile = profile

                else:
                    # 新用户恢复默认值
                    st.session_state.onboarding_gender = "女"
                    st.session_state.onboarding_age = 19
                    st.session_state.onboarding_height = 165.0
                    st.session_state.onboarding_weight = 50.0
                    st.session_state.existing_profile = None


        name = st.text_input(
            "怎么称呼你？",
            value="",
            placeholder="例如：杏仁",
            key="onboarding_name",
            on_change=load_profile
        )


        existing_profile = st.session_state.get(
            "existing_profile",
            None
        )

        if existing_profile:
            st.info("📂 检测到数据库中已有你的健康档案。")


        # 性别
        gender = st.radio(
            "性别",
            ["女", "男"],
            horizontal=True,
            key="onboarding_gender",
            help="注意！！性别当然不影响 BMI 公式计算，但会用于调整饮食和运动建议~"
        )


        # 年龄
        age = st.number_input(
            "年龄",
            min_value=18,
            max_value=100,
            step=1,
            key="onboarding_age"
        )


        # 身高 / 体重
        c1, c2 = st.columns(2)

        with c1:
            height = st.number_input(
                "身高（cm）",
                min_value=100.0,
                max_value=240.0,
                step=0.5,
                key="onboarding_height"
            )

        with c2:
            weight = st.number_input(
                "体重（kg）",
                min_value=25.0,
                max_value=200.0,
                step=0.5,
                key="onboarding_weight"
            )


    # BMI 实时预览
    preview_bmi = calculate_bmi(height, weight)
    preview_status, preview_color = bmi_status(preview_bmi)
    preview_min_w, preview_max_w = healthy_weight_range(height)

    with right:

        icon = {
            "green": "🟢",
            "yellow": "🟡",
            "orange": "🟠",
            "red": "🔴"
        }.get(preview_color, "🟢")

        st.subheader("LIVE BMI PREVIEW")

        st.metric(
            "当前 BMI",
            preview_bmi
        )

        st.info(
            f"{icon} 当前状态：{preview_status}"
        )

        st.write(
            f"参考正常体重范围：**{preview_min_w}–{preview_max_w} kg**"
        )

        st.caption(
            "BMI 是体重管理参考指标，不代表完整健康状况。"
        )


    # ============================================================
    # 健康目标
    # ============================================================

    st.markdown(
        '<div class="section-title">② 告诉我你想改善什么</div>',
        unsafe_allow_html=True
    )

    goal_options = [
        "保持当前状态",
        "温和减脂",
        "增肌塑形",
        "改善饮食",
    ]

    if preview_bmi < 18.5:
        recommended_goal = "改善饮食"
        goal_reason = "你的 BMI 偏低，系统更推荐先关注营养和规律饮食。"

    elif preview_bmi < 24:
        recommended_goal = "保持当前状态"
        goal_reason = "你的 BMI 处于正常范围，系统更推荐维持状态或提升体能。"

    else:
        recommended_goal = "温和减脂"
        goal_reason = "你的 BMI 高于正常范围，系统更推荐从温和的饮食和活动调整开始。"


    gc1, gc2 = st.columns([1.05, 0.95], gap="large")

    with gc1:
        health_goal = st.radio(
            "选择你的主要目标",
            goal_options,
            horizontal=True,
            key="health_goal_radio"
        )

    with gc2:
        st.info(
            f"💡 系统根据当前 BMI 推荐：**{recommended_goal}**\n\n"
            f"{goal_reason}\n\n"
            "你仍然可以按照自己的实际需求选择其他目标。"
        )


    # ============================================================
    # 主题
    # ============================================================

    st.markdown(
        '<div class="section-title">③ 选择属于你的主题</div>',
        unsafe_allow_html=True
    )

    themes = {
        "鼠尾草绿": {
            "primary": "#7BAE8B",
            "secondary": "#9B86B3",
            "soft": "#EEF4EA",
            "bg": "#F7F8F3",
        },
        "樱花粉": {
            "primary": "#D8899A",
            "secondary": "#9B86B3",
            "soft": "#F9ECEF",
            "bg": "#FCF7F8",
        },
        "海盐蓝": {
            "primary": "#79A8C8",
            "secondary": "#8F8CC7",
            "soft": "#EAF3F8",
            "bg": "#F5F9FB",
        },
        "元气橙": {
            "primary": "#E49A62",
            "secondary": "#A58AC2",
            "soft": "#FFF2E7",
            "bg": "#FCF8F4",
        },
    }

    theme_choice = st.radio(
        "选择一个你喜欢的主题色",
        list(themes.keys()),
        horizontal=True,
        key="theme_choice"
    )

    t = themes[theme_choice]


    tc1, tc2 = st.columns([0.18, 0.82])

    with tc1:
        st.markdown(
            f"""
            <div style="
                width:52px;
                height:52px;
                border-radius:16px;
                background:{t['primary']};
                box-shadow:0 8px 20px rgba(0,0,0,0.08);
            "></div>
            """,
            unsafe_allow_html=True
        )

    with tc2:
        st.markdown(
            f"""
            <div style="padding-top:5px;">
                <b>{theme_choice}</b><br>
                <span style="color:#7A857C;">
                    创建后整个健康空间都会使用这个主题。
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ============================================================
    # 创建健康空间
    # ============================================================

    if st.button(
        "✨ 创建我的专属健康空间",
        type="primary",
        use_container_width=True,
        key="create_health_space"
    ):

        if not name.strip():
            st.error("先给自己设置一个昵称吧～")

        else:

            st.session_state.profile = {
                "name": name.strip(),
                "gender": gender,
                "age": age,
                "height": height,
                "weight": weight,
            }

            st.session_state.health_goal = health_goal

            st.session_state.theme = {
                "name": theme_choice,
                **t,
            }

            # 保存 / 更新数据库中的个人档案
            db.save_profile(
                name.strip(),
                gender,
                age,
                height,
                weight
            )

            st.session_state.onboarding_done = True
            st.session_state.records = []
            st.session_state.latest_result = None

            # 保存第一条 BMI 健康记录
            save_result()

            st.rerun()


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(
        """
        <div class="soft-card">
            <b>🔐 隐私说明</b><br><br>
            本课程项目的数据保存在系统数据库中，
            仅用于健康管理功能展示与课程作业演示。
            请勿填写真实敏感个人信息。
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="footer">BMI 仅用于日常健康管理参考，不用于疾病诊断－O－</div>',
        unsafe_allow_html=True
    )

    st.stop()


# =========================
# 从数据库加载今天的健康挑战
# =========================

today = datetime.now().strftime("%Y-%m-%d")

if st.session_state.profile is not None:

    if st.session_state.get("task_date") != today:

        st.session_state.tasks = db.get_tasks(
            st.session_state.profile["name"],
            today
        )

        st.session_state.task_date = today

# ============================================================
# 主界面
# ============================================================

st.sidebar.markdown("## 🍀 Health Space(*^▽^*)")
st.sidebar.caption("我的健康空间")
st.sidebar.markdown("---")


page = st.sidebar.radio(
    "导航",
    [
        "🏠 今日首页",
        "💚 我的状态",
        "🔮 体重模拟",
        "🍽 今天吃什么",
        "📈 我的变化",
        "🎯 健康挑战",
    ],
    key="main_navigation"
)


st.sidebar.markdown("---")


if st.sidebar.button(
    "⚙️ 修改个人档案",
    use_container_width=True,
    key="edit_profile_button"
):
    st.session_state.onboarding_done = False
    st.rerun()


st.sidebar.markdown("### 快速信息")

p = st.session_state.profile

sidebar_bmi = calculate_bmi(
    p["height"],
    p["weight"]
)

sidebar_status, _ = bmi_status(sidebar_bmi)

st.sidebar.write(f"👤 {p['name']}")
st.sidebar.write(f"📏 {p['height']:.0f} cm")
st.sidebar.write(f"⚖️ {p['weight']:.1f} kg")
st.sidebar.write(f"💚 BMI {sidebar_bmi}")
st.sidebar.caption(f"当前状态：{sidebar_status}")


# ============================================================
# 今日首页
# ============================================================

if page == "🏠 今日首页":

    p = st.session_state.profile

    bmi = calculate_bmi(
        p["height"],
        p["weight"]
    )

    status, color = bmi_status(bmi)
    score = calculate_health_score(bmi)

    min_w, max_w = healthy_weight_range(
        p["height"]
    )

    persona, persona_desc = get_persona(
        p["gender"],
        bmi
    )


    st.markdown(
        '<div class="main-title">Hi，{} 👋</div>'.format(p["name"]),
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">今天也要照顾好自己。你的身体状态，值得被认真记录。</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(
        [1.25, 0.75],
        gap="large"
    )

    with col1:

        pill_class = f"pill-{color}"

        st.markdown(
            textwrap.dedent(
                f"""
                <div class="hero-card">
                    <div class="hero-label">TODAY'S HEALTH</div>
                    <div class="hero-bmi">{bmi}</div>
                    <div class="small-muted">BMI · 当前身体指数参考</div>
                    <div class="status-pill {pill_class}">
                        {
                '🟢'
                if color == 'green'
                else
                '🟡'
                if color == 'yellow'
                else
                '🟠'
                if color == 'orange'
                else
                '🔴'
                }
                        {status}
                    </div>
                    <div style="margin-top:18px;color:#5f6d63;">
                        当前体重：<b>{p['weight']:.1f} kg</b>　
                        推荐范围：<b>{min_w}–{max_w} kg</b>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            textwrap.dedent(
                f"""
                <div class="persona-card">
                    <div class="small-muted">YOUR HEALTH PERSONA</div>
                    <div class="persona-name">{persona}</div>
                    <div class="persona-desc">{persona_desc}</div>
                    <div style="margin-top:20px;">
                        <span class="small-muted">今日健康指数</span>
                        <div style="font-size:2.6rem;font-weight:800;color:#566776;">
                            {score}
                            <span style="font-size:1rem;color:#8B958D;">/ 100</span>
                        </div>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )


    # 当前状态
    st.markdown(
        '<div class="section-title">📌 你现在的状态</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)


    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">BMI</div>
                <div class="metric-value">{bmi}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">体重</div>
                <div class="metric-value">
                    {p["weight"]:.1f} kg
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">推荐下限</div>
                <div class="metric-value">{min_w} kg</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">推荐上限</div>
                <div class="metric-value">{max_w} kg</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # 今日挑战
    st.markdown(
        '<div class="section-title">🎯 今日健康挑战</div>',
        unsafe_allow_html=True
    )


    task_cols = st.columns(4)

    for idx, (task, value) in enumerate(
        st.session_state.tasks.items()
    ):

        with task_cols[idx]:

            checked = st.checkbox(
                task,
                value=value,
                key=f"home_task_{task}"
            )

            st.session_state.tasks[task] = checked


    done = sum(
        st.session_state.tasks.values()
    )

    total = len(
        st.session_state.tasks
    )

    st.progress(
        done / total
        if total
        else 0
    )

    st.caption(
        f"今日完成 {done}/{total} 项挑战"
    )


    # 今日菜单
    st.markdown(
        '<div class="section-title">🍽 今天可以这样吃</div>',
        unsafe_allow_html=True
    )

    foods = diet_plan(
        status,
        p["gender"]
    )

    food_cols = st.columns(4)

    for idx, (emoji, meal, food) in enumerate(foods):
        with food_cols[idx]:
            st.markdown(
                textwrap.dedent(
                    f"""
                    <div class="food-card">
                        <div class="food-emoji">{emoji}</div>
                        <div class="food-title">{meal}</div>
                        <div class="food-text">{food}</div>
                    </div>
                    """
                ).strip(),
                unsafe_allow_html=True,
            )


    st.markdown(
        '<div class="footer">健康管理仅供日常参考，不能替代专业医学诊断。</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 我的状态
# ============================================================

elif page == "💚 我的状态":

    st.markdown(
        '<div class="main-title">💚 我的状态</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">把一个数字，变成真正看得懂的健康信息。</div>',
        unsafe_allow_html=True
    )


    p = st.session_state.profile


    with st.expander(
        "✏️ click here 修改我的健康档案与目标",
        expanded=False
    ):

        c1, c2 = st.columns(2)

        with c1:

            new_name = st.text_input(
                "昵称",
                value=p["name"],
                key="edit_name"
            )

            new_gender = st.radio(
                "性别",
                ["男", "女"],
                index=0 if p["gender"] == "男" else 1,
                horizontal=True,
                key="edit_gender"
            )

            new_age = st.number_input(
                "年龄",
                18,
                100,
                int(p["age"]),
                key="edit_age"
            )

        with c2:
            new_height = st.number_input(
                "身高（cm）",
                100.0,
                240.0,
                float(p["height"]),
                step=0.5,
                key="edit_height"
            )

            new_weight = st.number_input(
                "体重（kg）",
                25.0,
                200.0,
                float(p["weight"]),
                step=0.5,
                key="edit_weight"
            )



        st.markdown("### 🎨 主题色")


        theme_names = [
            "鼠尾草绿",
            "樱花粉",
            "海盐蓝",
            "元气橙"
        ]


        theme_map = {

            "鼠尾草绿": {
                "primary": "#7BAE8B",
                "secondary": "#9B8AC4",
                "soft": "#EEF4EA",
                "bg": "#F7F8F3"
            },

            "樱花粉": {
                "primary": "#D8899A",
                "secondary": "#9B86B3",
                "soft": "#F9ECEF",
                "bg": "#FCF7F8"
            },

            "海盐蓝": {
                "primary": "#79A8C8",
                "secondary": "#8F8CC7",
                "soft": "#EAF3F8",
                "bg": "#F5F9FB"
            },

            "元气橙": {
                "primary": "#E49A62",
                "secondary": "#A58AC2",
                "soft": "#FFF2E7",
                "bg": "#FCF8F4"
            },

        }


        current_theme = st.session_state.theme.get(
            "name",
            "鼠尾草绿"
        )


        selected_theme = st.radio(
            "选择主题",
            theme_names,
            index=(
                theme_names.index(current_theme)
                if current_theme in theme_names
                else 0
            ),
            horizontal=True,
            key="edit_theme"
        )


        if st.button(
            "保存并生成最新状态",
            type="primary",
            key="save_status_button"
        ):

            new_name = new_name.strip() or "同学"


            st.session_state.profile = {

                "name": new_name,

                "gender": new_gender,

                "age": new_age,

                "height": new_height,

                "weight": new_weight,

            }


            st.session_state.theme = {

                "name": selected_theme,

                **theme_map[selected_theme],

            }


            # 更新数据库中的个人档案
            db.save_profile(

                st.session_state.profile["name"],

                st.session_state.profile["gender"],

                st.session_state.profile["age"],

                st.session_state.profile["height"],

                st.session_state.profile["weight"]

            )


            # 生成最新健康记录
            save_result()


            st.success(
                "已经生成新的健康状态！"
            )

            st.rerun()


    p = st.session_state.profile


    bmi = calculate_bmi(
        p["height"],
        p["weight"]
    )

    status, color = bmi_status(bmi)

    min_w, max_w = healthy_weight_range(
        p["height"]
    )


    c1, c2 = st.columns(
        [0.95, 1.05],
        gap="large"
    )


    with c1:
        st.markdown(
            textwrap.dedent(
                f"""
                <div class="report-card">
                    <div class="hero-label">CURRENT BMI</div>
                    <div style="font-size:3.6rem; font-weight:800; color:#34483C;">{bmi}</div>
                    <div class="status-pill pill-{color}">{status}</div>
                    <div style="margin-top:18px; color:#69756D; line-height:1.8;">
                        身高：{p['height']:.1f} cm<br>
                        体重：{p['weight']:.1f} kg<br>
                        年龄：{p['age']} 岁
                    </div>
                </div>
                """
            ).strip(),
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            '<div class="section-title">📊 BMI 区间</div>',
            unsafe_allow_html=True
        )


        bar_width = bmi_bar_width(bmi)


        st.markdown(
            f"""
            <div style="
                background:#E8ECE7;
                border-radius:999px;
                height:22px;
                overflow:hidden;
            ">

                <div style="
                    width:{bar_width}%;
                    height:100%;
                    background:linear-gradient(
                        90deg,
                        #A9D2AD,
                        #86B891,
                        #E3BF74,
                        #DB8F8F
                    );
                    border-radius:999px;
                ">
                </div>

            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                color:#7F8982;
                font-size:0.78rem;
                margin-top:8px;
            ">
                <span>偏瘦 18.5</span>
                <span>正常 23.9</span>
                <span>超重 27.9</span>
                <span>肥胖</span>
            </div>
            """,
            unsafe_allow_html=True
        )


        st.info(
            f"对于 {p['height']:.1f} cm 的身高，"
            f"参考正常体重范围约为 "
            f"**{min_w}–{max_w} kg**。"
        )


        st.markdown(
            '<div class="section-title">🌱 你现在最需要做什么？</div>',
            unsafe_allow_html=True
        )


        for i, item in enumerate(
            status_advice(
                status,
                p["gender"]
            ),
            1
        ):

            st.markdown(
                f"**{i}.** {item}"
            )


    # 健身推荐
    st.markdown(
        '<div class="section-title">🏋️ 给你的健身推荐</div>',
        unsafe_allow_html=True
    )


    video_data = {

        ("女", "增肌塑形"): {
            "title": "💪 女生基础力量训练",
            "description": "适合刚开始进行力量训练的同学，从简单动作开始。",
            "url": "https://player.bilibili.com/player.html?bvid=BV1fCjQ6QE8t"
        },

        ("男", "增肌塑形"): {
            "title": "🏋️ 新手力量训练",
            "description": "适合初学者的基础力量训练，可以从简单的自重动作开始。",
            "url": "https://player.bilibili.com/player.html?bvid=BV1fiui6dEj9"
        },

        ("女", "温和减脂"): {
            "title": "🔥 低冲击燃脂训练",
            "description": "15分钟低冲击、无需器械，更适合刚开始运动或希望减少关节压力的训练。",
            "url": "https://player.bilibili.com/player.html?bvid=BV1bhRcBpE3j"
        },

        ("男", "温和减脂"): {
            "title": "🔥 居家有氧训练",
            "description": "30分钟全身站立有氧训练，无需器械，适合居家运动。",
            "url": "https://player.bilibili.com/player.html?bvid=BV1DLpszZEK7"
        },

        ("女", "保持当前状态"): {
            "title": "🌿 全身活力训练",
            "description": "10分钟全身活动与拉伸，适合久坐学习后放松身体。",
            "url": "https://player.bilibili.com/player.html?bvid=BV11dkYBGEyc"
        },

        ("男", "保持当前状态"): {
            "title": "🏃 全身自重基础训练",
            "description": "适合作为日常运动，帮助维持体能和活动量。",
            "url": "https://player.bilibili.com/player.html?bvid=BV1qr4y1i7tq"
        },

        ("女", "改善饮食"): {
            "title": "🧘 10分钟全身拉伸",
            "description": "如果目前更想改善生活方式，可以先从简单拉伸和轻运动开始。",
            "url": "https://player.bilibili.com/player.html?bvid=BV1gb411x7tY"
        },

        ("男", "改善饮食"): {
            "title": "🧘 日常全身活动",
            "description": "简单的全身运动，适合运动基础较少的同学",
            "url": "https://player.bilibili.com/player.html?bvid=BV11dkYBGEyc"
        },

    }


    current_gender = p["gender"]

    current_goal = st.session_state.get(
        "health_goal",
        "保持当前状态"
    )


    current_video = video_data.get(
        (current_gender, current_goal),
        video_data[("男", "保持当前状态")]
    )


    video_col, info_col = st.columns(
        [1.45, 0.85],
        gap="large"
    )


    with video_col:

        st.components.v1.iframe(
            current_video["url"],
            height=430,
            scrolling=False
        )

    with info_col:
        st.markdown(
            textwrap.dedent(
                f"""
                <div class="soft-card" style="min-height:430px;">
                    <div class="small-muted">小建议~</div>
                    <div style="font-size:1.4rem; font-weight:800; color:#35443A; margin-top:12px; margin-bottom:12px;">{current_video["title"]}</div>
                    <div style="color:#758178; line-height:1.8;">{current_video["description"]}</div>
                    <div style="margin-top:25px; padding:15px; border-radius:14px; background:#F4F7F2;">
                        <div style="font-weight:700; color:#435148;">🎯 为什么推荐给你？</div>
                        <div style="margin-top:7px; color:#768178; line-height:1.7;">系统根据你的性别、BMI 状态和健康目标，为你匹配了当前更适合的运动内容。</div>
                    </div>
                    <div style="margin-top:20px; color:#879188; font-size:0.85rem; line-height:1.7;">
                        当前状态：{status}<br>
                        当前目标：{current_goal}<br>
                        性别：{current_gender}
                    </div>
                </div>
                """
            ).strip(),
            unsafe_allow_html=True
        )


    st.caption(
        "💡 建议根据自己的身体状态循序渐进运动。"
        "如运动过程中出现明显不适，应及时停止。"
    )


# ============================================================
# 体重模拟
# ============================================================

elif page == "🔮 体重模拟":

    st.markdown(
        '<div class="main-title">🔮 体重模拟</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">拖动体重，看看 BMI 和健康状态会如何变化！</div>',
        unsafe_allow_html=True
    )


    p = st.session_state.profile

    current_weight = float(
        p["weight"]
    )


    target_weight = st.slider(
        "预测体重（kg）",
        min_value=40.0,
        max_value=120.0,
        value=float(
            round(
                current_weight,
                1
            )
        ),
        step=0.5,
        key="weight_simulation"
    )


    current_bmi = calculate_bmi(
        p["height"],
        current_weight
    )

    future_bmi = calculate_bmi(
        p["height"],
        target_weight
    )

    current_status, current_color = bmi_status(
        current_bmi
    )

    future_status, future_color = bmi_status(
        future_bmi
    )


    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            textwrap.dedent(
                f"""
                <div class="metric-card">
                    <div class="metric-title">现在</div>
                    <div class="metric-value">{current_weight:.1f} kg</div>
                    <div style="margin-top:5px; color:#7B887E;">BMI {current_bmi} · {current_status}</div>
                </div>
                """
            ).strip(),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            textwrap.dedent(
                f"""
                <div class="metric-card">
                    <div class="metric-title">模拟后</div>
                    <div class="metric-value">{target_weight:.1f} kg</div>
                    <div style="margin-top:5px; color:#7B887E;">BMI {future_bmi} · {future_status}</div>
                </div>
                """
            ).strip(),
            unsafe_allow_html=True
        )


    delta = round(
        target_weight - current_weight,
        1
    )


    if delta > 0:
        delta_text = f"体重增加 {delta:.1f} kg"

    elif delta < 0:
        delta_text = f"体重减少 {abs(delta):.1f} kg"

    else:
        delta_text = "体重保持不变"


    st.markdown("---")


    if current_status != future_status:

        st.success(
            f"✨ {delta_text} 后，你的 BMI 状态可能从 "
            f"**{current_status}** 变为 **{future_status}**。"
        )

    else:

        st.info(
            f"🌿 {delta_text} 后，BMI 仍处于 "
            f"**{future_status}** 范围。"
        )


    st.markdown(
        """
        <div class="soft-card" style="margin-top:18px;">
            <b>小提醒，请看这里！！</b><br>
            这个模拟器初衷希望帮助你理解
            “身高、体重与 BMI”之间的关系，
            不代表真实健康结果，也不建议为了追求某个 BMI 数字而快速改变体重，
            做一些极端的行为。
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 今天吃什么
# ============================================================

elif page == "🍽 今天吃什么":

    st.markdown(
        '<div class="main-title">🍽 今天吃什么</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">不是一句“少吃多运动”，而是一份更具体的日常选择！</div>',
        unsafe_allow_html=True
    )


    p = st.session_state.profile

    bmi = calculate_bmi(
        p["height"],
        p["weight"]
    )

    status, _ = bmi_status(bmi)

    foods = diet_plan(
        status,
        p["gender"]
    )


    st.markdown(
        f"""
        <div class="soft-card">
            当前 BMI：<b>{bmi}</b>　
            当前状态：<b>{status}</b>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">🥗 今日菜单</div>',
        unsafe_allow_html=True
    )


    cols = st.columns(4)


    for idx, (emoji, meal, food) in enumerate(foods):

        with cols[idx]:

            st.markdown(
                f"""
                <div class="food-card">
                    <div class="food-emoji">
                        {emoji}
                    </div>
                    <div class="food-title">
                        {meal}
                    </div>
                    <div class="food-text">
                        {food}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        '<div class="section-title">💡 为什么这么推荐？</div>',
        unsafe_allow_html=True
    )


    explanation = {

        "偏瘦":
            "你当前 BMI 偏低，因此建议优先保证规律进食和优质营养，而不是简单用高糖高脂食品“增重”。",

        "正常":
            "你的 BMI 处于正常范围，因此目标是维持稳定，而不是为了更瘦而刻意降低摄入。",

        "超重":
            "你的 BMI 处于超重范围，因此建议减少高能量食品，同时保证蛋白质和蔬菜摄入。",

        "肥胖":
            "你的 BMI 较高，因此更适合采用渐进式的饮食结构调整，并结合稳定的日常活动。",

    }


    st.info(
        explanation[status]
    )


    st.markdown(
        '<div class="section-title">🛒 可以优先买这些</div>',
        unsafe_allow_html=True
    )


    shopping = {

        "偏瘦":
            ["牛奶", "鸡蛋", "酸奶", "鱼肉", "坚果", "水果"],

        "正常":
            ["鸡蛋", "牛奶", "鱼肉", "蔬菜", "水果", "全麦面包"],

        "超重":
            ["鸡胸肉", "鱼肉", "西兰花", "番茄", "无糖酸奶", "粗粮"],

        "肥胖":
            ["鸡蛋", "低脂奶", "鱼肉", "豆制品", "绿叶菜", "低糖水果"],

    }


    tags = shopping[status]

    st.markdown(
        "　".join(
            [f"`{x}`" for x in tags]
        )
    )


# ============================================================
# 我的变化
# ============================================================

elif page == "📈 我的变化":

    st.markdown(
        '<div class="main-title">📈 我的变化</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">健康不是一次测量，而是一段时间里的变化。</div>',
        unsafe_allow_html=True
    )

    # 从数据库读取当前用户的健康历史
    p = st.session_state.profile
    records = db.get_health_records(p["name"])

    if not records:

        st.info(
            "目前还没有历史记录。"
            "先去「💚 我的状态」保存一次最新状态吧。"
        )

    else:

        # 数据库返回的是元组，需要转换成 DataFrame
        df = pd.DataFrame(
            records,
            columns=[
                "date",
                "gender",
                "age",
                "height",
                "weight",
                "bmi",
                "status",
                "score"
            ]
        )

        # 转换时间格式
        df["date"] = pd.to_datetime(df["date"])

        # 按时间排序
        df = df.sort_values("date")

        # =========================
        # 顶部数据卡片
        # =========================

        latest = df.iloc[-1]

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">最近 BMI</div>
                    <div class="metric-value">{latest["bmi"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">记录次数</div>
                    <div class="metric-value">{len(df)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # =========================
        # BMI 趋势
        # =========================

        st.markdown(
            '<div class="section-title">BMI 趋势</div>',
            unsafe_allow_html=True
        )

        bmi_chart = df.set_index("date")[["bmi"]]

        st.line_chart(
            bmi_chart,
            height=310
        )

        # =========================
        # 体重趋势
        # =========================

        st.markdown(
            '<div class="section-title">体重趋势</div>',
            unsafe_allow_html=True
        )

        weight_chart = df.set_index("date")[["weight"]]

        st.line_chart(
            weight_chart,
            height=280
        )

        # =========================
        # 历史记录
        # =========================

        st.markdown(
            '<div class="section-title">📋 我的记录</div>',
            unsafe_allow_html=True
        )

        show_df = df.rename(
            columns={
                "date": "时间",
                "gender": "性别",
                "age": "年龄",
                "height": "身高(cm)",
                "weight": "体重(kg)",
                "bmi": "BMI",
                "status": "状态",
                "score": "健康指数"
            }
        )

        st.dataframe(
            show_df,
            use_container_width=True,
            hide_index=True
        )

        # =========================
        # 最新健康报告
        # =========================

        st.markdown(
            '<div class="section-title">📄 我的健康报告</div>',
            unsafe_allow_html=True
        )

        persona, desc = get_persona(
            latest["gender"],
            latest["bmi"]
        )

        min_w, max_w = healthy_weight_range(
            latest["height"]
        )

        report_time = latest["date"].strftime(
            "%Y-%m-%d %H:%M"
        )

        st.markdown(
            f"""
            <div class="report-card">
                <div class="hero-label">
                    MY HEALTH REPORT
                </div>
                <h2 style="margin-bottom:8px;">
                    {report_time} 健康报告
                </h2>
                <p>
                    <b>基本信息：</b>
                    {latest["gender"]} ·
                    {int(latest["age"])} 岁 ·
                    {latest["height"]:.1f} cm ·
                    {latest["weight"]:.1f} kg
                </p>
                <p>
                    <b>BMI：</b>{latest["bmi"]}
                    <b>状态：</b>{latest["status"]}
                </p>
                <p>
                    <b>推荐体重范围：</b>
                    {min_w}–{max_w} kg
                </p>
                <p>
                    <b>健康人格：</b>
                    {persona}
                </p>
                <p style="
                    line-height:1.8;
                    color:#69756D;
                ">
                    {desc}
                </p>
                <hr style="
                    border:none;
                    border-top:1px solid #E6ECE4;
                ">
                <p style="color:#7A857C;">
                    建议把注意力放在长期趋势，而不是单次数字！
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 健康挑战
# ============================================================

elif page == "🎯 健康挑战":

    st.markdown(
        '<div class="main-title">🎯 健康挑战</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">今天完成几个小目标，让健康管理变成一点点有趣的习惯。</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">✅ 今日任务</div>',
        unsafe_allow_html=True
    )

    for i, task in enumerate(st.session_state.tasks):

        old_value = st.session_state.tasks[task]

        checked = st.checkbox(
            task,
            value=old_value,
            key=f"task_{task}",
        )

        if checked != old_value:
            db.save_task(
                st.session_state.profile["name"],
                today,
                task,
                checked
            )

        st.session_state.tasks[task] = checked


    done = sum(
        st.session_state.tasks.values()
    )

    total = len(
        st.session_state.tasks
    )

    percent = (
        int(done / total * 100)
        if total
        else 0
    )


    c1, c2 = st.columns([1, 1])


    with c1:

        st.markdown(
            f"""
            <div class="hero-card">
                <div class="hero-label">
                    TODAY'S PROGRESS
                </div>
                <div class="hero-bmi">
                    {percent}%
                </div>
                <div class="small-muted">
                    今日挑战完成度
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            """
            <div class="persona-card">
                <div class="small-muted">
                    TODAY'S NOTE
                </div>
                <div class="persona-name">
                    别追求一次做到完美。
                </div>
                <div class="persona-desc">
                    健康管理真正重要的是持续。
                    哪怕今天只完成一项，
                    也比完全不开始更好！！
                    fighting！！ヽ(￣ω￣(￣ω￣〃)ゝ
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.progress(
        percent / 100
    )


    if percent == 100:

        st.balloons()

        st.success(
            "🎉 今日挑战全部完成！你的健康进度条拉满了"
        )

    elif percent >= 50:

        st.info(
            "🌱 已经完成一半以上，继续保持"
        )

    else:

        st.warning(
            "✨ 从最容易的一项开始就好"
        )


# =========================
# 页面底部
# =========================

st.markdown(
    '<div class="footer">Health Space · BMI 仅作为健康管理参考，不用于疾病诊断。</div>',
    unsafe_allow_html=True
)
