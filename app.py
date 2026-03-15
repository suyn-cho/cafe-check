import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, timezone, timedelta

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Café Order",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── KST 시간 헬퍼 ──────────────────────────────────────────────
KST = timezone(timedelta(hours=9))

def kst_now():
    return datetime.now(KST)

def kst_today_str():
    return kst_now().strftime("%Y-%m-%d")

def kst_time_str():
    return kst_now().strftime("%H:%M:%S")

# ─── 상수 ────────────────────────────────────────────────────────
ADMIN_PASSWORD = "2664"
DATA_FILE = "orders.json"
DAILY_LIMIT = 1   # 1일 최대 주문 횟수

GROUPS = {
    "생명": {
        "icon": "❤️",
        "members": ["서은주", "박민형", "정택연", "서석호", "강서연", "신금주", "한정빈"]
    },
    "카드": {
        "icon": "💳",
        "members": ["이상아", "김보미", "강홍석", "정서라", "곽민준", "최송화", "김주희"]
    },
    "화재": {
        "icon": "🔥",
        "members": ["이원진", "최영철", "이호철", "배강현", "채수지", "권슬기"]
    },
    "증권": {
        "icon": "📈",
        "members": ["양은원", "이수진", "심예현", "조성진", "한성원", "박가훈", "최민석"]
    },
    "강사": {
        "icon": "📚",
        "members": ["문현실", "이우진", "방혜진", "박도형"]
    },
    "운영진": {
        "icon": "⭐",
        "members": ["조수연", "강병규", "김민정", "이상은", "박진용", "조윤호"]
    },
    "기타": {
        "icon": "✏️",
        "members": []
    }
}

MENUS = {
    "☕ 커피 (Coffee)": [
        "아메리카노", "달달커피", "헤이즐넛 아메리카노", "꿀화이트 아메리카노",
        "콜드브루", "카페라떼", "카푸치노", "바닐라라떼", "연유카페라떼",
        "카페모카", "화이트초콜릿모카", "카라멜마끼아또", "아포카토",
        "시그니처라떼", "넛츠크림라떼", "민트모카", "흑당콜드브루",
        "콜드브루라떼", "연유콜드브루"
    ],
    "🍵 티 (Tea)": [
        "캐모마일", "히비스커스", "페퍼민트", "얼그레이", "루이보스",
        "아이스티", "아샷추", "아망추", "쌍화차", "배모과차",
        "살얼음식혜", "유자차", "자몽차", "레몬차", "생강차",
        "복분자뱅쇼", "로열밀크티"
    ],
    "🍊 에이드 (Ade)": [
        "자몽포멜로에이드", "감귤레몬에이드", "꿀복숭아에이드",
        "머스캣모히또 에이드", "샹그리아에이드"
    ],
    "🥛 논커피 (Non Coffee)": [
        "흑당라떼", "미숫가루라떼", "초콜릿", "달고나라떼", "말차라떼",
        "민트초콜릿", "화이트초콜릿", "토피넛라떼", "고구마라떼",
        "딸기듬뿍라떼", "딸기초고라떼", "말차초코라떼", "버블흑당라떼"
    ],
    "🥤 블렌디드 (Blended)": [
        "과일플랫치노", "밀크플랫치노", "요거트플랫치노", "밀크쉐이크",
        "초코쿠키쉐이크", "에스프레소쉐이크", "딸기쉐이크", "말차초코쉐이크"
    ],
    "🍓 과일주스 (Fruit Juice)": [
        "사과당근클렌즈주스", "키위케일샐러리 클렌즈주스", "딸기주스",
        "망고주스", "블루베리주스", "믹스주스"
    ]
}

CAT_SHORTS = [
    "커피 (Coffee)", "티 (Tea)", "에이드 (Ade)",
    "논커피 (Non Coffee)", "블렌디드 (Blended)", "과일주스 (Fruit Juice)"
]
CAT_ICONS = ["☕", "🍵", "🍊", "🥛", "🥤", "🍓"]

# ─── 데이터 함수 ─────────────────────────────────────────────────
def load_orders():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def get_today_order_count(name):
    today = kst_today_str()
    return sum(1 for o in load_orders() if o["이름"] == name and o["날짜"] == today)

def add_order(name, group, menu):
    orders = load_orders()
    orders.append({
        "이름": name,
        "소속": group,
        "날짜": kst_today_str(),
        "시간": kst_time_str(),
        "메뉴": menu
    })
    save_orders(orders)

# ─── 스타일 ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #fff5f0 0%, #fff0eb 40%, #fce8e0 100%) !important;
    font-family: 'Noto Sans KR', 'Nunito', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 1rem 2rem 1rem !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}
.cafe-header { text-align: center; padding: 2rem 1rem 1.2rem; }
.cafe-subtitle { font-size: 0.85rem; font-weight: 700; color: #555; margin-bottom: 0.5rem; }
.cafe-title {
    font-family: 'Nunito', sans-serif;
    font-size: 2.6rem; font-weight: 900;
    background: linear-gradient(135deg, #FF4500 0%, #FF6B35 50%, #FFA500 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0; line-height: 1.1;
}
.cafe-title span { -webkit-text-fill-color: #222; }
.rule-badge {
    display: inline-block;
    background: linear-gradient(135deg, #FF4500, #FFA500);
    color: white; font-size: 0.78rem; font-weight: 700;
    padding: 0.45rem 1.2rem; border-radius: 999px;
    margin: 0.8rem auto 1.5rem; letter-spacing: 0.03em;
}
.section-title {
    font-size: 0.75rem; font-weight: 700; color: #aaa;
    text-transform: uppercase; letter-spacing: 0.1em;
    text-align: center; margin: 1.2rem 0 0.8rem;
}
.step-bar { display: flex; align-items: center; justify-content: center; gap: 0.3rem; margin: 0.5rem 0 1rem; }
.step-dot { width: 8px; height: 8px; border-radius: 50%; background: #e0e0e0; }
.step-dot.active { background: #FF4500; width: 22px; border-radius: 4px; }
.warning-box {
    background: #fff0f0; border: 2px solid #FF4500; border-radius: 16px;
    padding: 1rem 1.2rem; text-align: center; color: #cc2200;
    font-weight: 700; font-size: 0.9rem; margin: 0.5rem 0;
}
.success-box {
    background: linear-gradient(135deg, #FF4500, #FFA500);
    border-radius: 16px; padding: 1.2rem; text-align: center;
    color: white; font-weight: 800; font-size: 1rem; margin: 0.5rem 0;
}
.admin-header { text-align: center; padding: 1.5rem 0 0.5rem; }
.admin-title { font-size: 1.4rem; font-weight: 900; color: #FF4500; }
.stButton > button {
    background: linear-gradient(135deg, #FF4500, #FF6B35) !important;
    color: white !important; border: none !important;
    border-radius: 999px !important; font-weight: 800 !important;
    font-size: 1rem !important; padding: 0.65rem 2rem !important;
    width: 100% !important; box-shadow: 0 6px 20px rgba(255,80,0,0.3) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(255,80,0,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── 세션 초기화 ─────────────────────────────────────────────────
for _key, _val in {
    "page": "main",
    "selected_group": None,
    "selected_name": None,
    "selected_menu": None,
    "selected_category": None,
    "admin_auth": False,
}.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val


# ─── 헤더 컴포넌트 ───────────────────────────────────────────────
def render_header(step=0):
    st.markdown("""
    <div class="cafe-header">
        <div class="cafe-subtitle">2026 삼성금융사 'AI 전략과정'</div>
        <div class="cafe-title">Café <span>order</span></div>
    </div>
    """, unsafe_allow_html=True)
    if step > 0:
        dots = "".join(
            '<div class="step-dot{}"></div>'.format(" active" if i == step else "")
            for i in range(1, 4)
        )
        st.markdown('<div class="step-bar">{}</div>'.format(dots), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 메인 페이지
# ═══════════════════════════════════════════════════════════════
def render_main():
    render_header()
    st.markdown("""
    <div style="text-align:center">
        <div class="rule-badge">1일 1잔 &nbsp;|&nbsp; 베이커리 불가 &nbsp;|&nbsp; EXTRA 사이즈 불가</div>
    </div>
    <div class="section-title">소속을 선택해 주세요</div>
    """, unsafe_allow_html=True)

    regular = [g for g in GROUPS if g != "기타"]
    cols = st.columns(2)
    for i, group in enumerate(regular):
        info = GROUPS[group]
        with cols[i % 2]:
            if st.button("{} {}".format(info["icon"], group), key="grp_{}".format(group), use_container_width=True):
                st.session_state.selected_group = group
                st.session_state.selected_name = None
                st.session_state.selected_menu = None
                st.session_state.selected_category = None
                st.session_state.page = "select_name"
                st.rerun()

    if st.button("✏️  기타", key="grp_기타", use_container_width=True):
        st.session_state.selected_group = "기타"
        st.session_state.selected_name = None
        st.session_state.selected_menu = None
        st.session_state.selected_category = None
        st.session_state.page = "select_name"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔒 관리자 페이지", key="admin_btn"):
            st.session_state.page = "admin"
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# 이름 선택 페이지
# ═══════════════════════════════════════════════════════════════
def render_select_name():
    group = st.session_state.selected_group
    info  = GROUPS[group]
    render_header(step=1)
    st.markdown(
        '<div class="section-title">{} {} · 이름을 선택해 주세요</div>'.format(info["icon"], group),
        unsafe_allow_html=True
    )

    if group == "기타":
        custom = st.text_input("이름을 직접 입력해 주세요", placeholder="홍길동", key="custom_name_input")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 뒤로", key="back_name"):
                st.session_state.page = "main"
                st.session_state.selected_group = None
                st.rerun()
        with col2:
            if st.button("다음 →", key="next_custom", use_container_width=True):
                name = custom.strip()
                if not name:
                    st.warning("이름을 입력해 주세요.")
                else:
                    st.session_state.selected_name = name
                    st.session_state.selected_menu = None
                    st.session_state.page = "select_menu"
                    st.rerun()
    else:
        cols = st.columns(3)
        for i, name in enumerate(info["members"]):
            with cols[i % 3]:
                label = "✓ {}".format(name) if st.session_state.selected_name == name else name
                if st.button(label, key="name_{}".format(name), use_container_width=True):
                    st.session_state.selected_name = name
                    st.session_state.selected_menu = None
                    st.session_state.page = "select_menu"
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← 뒤로", key="back_name"):
            st.session_state.page = "main"
            st.session_state.selected_group = None
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# 메뉴 선택 페이지  (A: 카테고리 → B: 세부메뉴)
# ═══════════════════════════════════════════════════════════════
def render_select_menu():
    name  = st.session_state.selected_name
    group = st.session_state.selected_group
    count = get_today_order_count(name)

    render_header(step=2)
    st.markdown(
        '<div class="section-title">👤 {} · {} &nbsp;|&nbsp; 오늘 {}/{}잔</div>'.format(
            group, name, count, DAILY_LIMIT),
        unsafe_allow_html=True
    )

    if count >= DAILY_LIMIT:
        st.markdown(
            '<div class="warning-box">⚠️ 오늘의 주문({}잔)을 이미 완료했습니다.<br>내일 다시 이용해 주세요!</div>'.format(DAILY_LIMIT),
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← 처음으로", key="back_limit"):
            st.session_state.page = "main"
            st.session_state.selected_group = None
            st.session_state.selected_name = None
            st.session_state.selected_category = None
            st.rerun()
        return

    st.markdown(
        '<div style="text-align:center"><div class="rule-badge">1일 1잔 · 베이커리 불가 · EXTRA 사이즈 불가</div></div>',
        unsafe_allow_html=True
    )

    cat_list = list(MENUS.keys())

    if st.session_state.selected_category is None:
        st.markdown('<div class="section-title">카테고리를 선택해 주세요</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, cat in enumerate(cat_list):
            icon  = CAT_ICONS[i]  if i < len(CAT_ICONS)  else "🍹"
            short = CAT_SHORTS[i] if i < len(CAT_SHORTS) else cat
            with cols[i % 2]:
                if st.button("{} {}".format(icon, short), key="cat_{}".format(i), use_container_width=True):
                    st.session_state.selected_category = cat
                    st.session_state.selected_menu = None
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← 뒤로", key="back_to_name"):
            st.session_state.page = "select_name"
            st.session_state.selected_category = None
            st.rerun()

    else:
        cat   = st.session_state.selected_category
        items = MENUS[cat]
        st.markdown(
            '<div class="section-title">{} · 음료를 선택해 주세요</div>'.format(cat),
            unsafe_allow_html=True
        )

        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                is_sel = st.session_state.selected_menu == item
                label  = "✓ {}".format(item) if is_sel else item
                if st.button(label, key="item_{}".format(i), use_container_width=True):
                    st.session_state.selected_menu = item
                    st.rerun()

        if st.session_state.selected_menu:
            st.markdown(
                "<div style='text-align:center; padding:0.8rem 0 0.3rem'>"
                "<span style='font-weight:800; color:#FF4500; font-size:1.05rem'>"
                "✓ 선택: {}</span></div>".format(st.session_state.selected_menu),
                unsafe_allow_html=True
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← 카테고리", key="back_to_cat"):
                    st.session_state.selected_category = None
                    st.session_state.selected_menu = None
                    st.rerun()
            with col2:
                if st.button("☕ 주문하기", key="confirm_order"):
                    add_order(name, group, st.session_state.selected_menu)
                    st.session_state.selected_category = None
                    st.session_state.page = "success"
                    st.rerun()
        else:
            if st.button("← 카테고리", key="back_to_cat2"):
                st.session_state.selected_category = None
                st.session_state.selected_menu = None
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# 주문 완료 페이지
# ═══════════════════════════════════════════════════════════════
def render_success():
    name  = st.session_state.selected_name
    menu  = st.session_state.selected_menu
    group = st.session_state.selected_group
    count = get_today_order_count(name)

    render_header(step=3)
    st.markdown(
        "<br><div class='success-box'>☕ 주문 완료!<br>"
        "<span style='font-size:1.3rem'>{}님의 <strong>{}</strong></span><br>"
        "<span style='font-size:0.85rem; opacity:0.85'>{} · 오늘 {}/{}잔 사용</span></div>".format(
            name, menu, group, count, DAILY_LIMIT),
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🏠 처음으로 돌아가기", key="go_home"):
        st.session_state.page = "main"
        st.session_state.selected_group = None
        st.session_state.selected_name  = None
        st.session_state.selected_menu  = None
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# 관리자 페이지
# ═══════════════════════════════════════════════════════════════
def render_admin():
    st.markdown('<div class="admin-header"><div class="admin-title">🔒 관리자 페이지</div></div>', unsafe_allow_html=True)

    if not st.session_state.admin_auth:
        pw = st.text_input("비밀번호를 입력하세요", type="password", key="admin_pw")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("확인", key="admin_confirm"):
                if pw == ADMIN_PASSWORD:
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("비밀번호가 틀렸습니다.")
        with col2:
            if st.button("← 뒤로", key="admin_back"):
                st.session_state.page = "main"
                st.rerun()
        return

    orders = load_orders()
    st.markdown(
        "<div style='text-align:center; color:#888; font-size:0.85rem; margin-bottom:1rem'>"
        "총 주문 수: <strong>{}건</strong> &nbsp;|&nbsp; "
        "현재 시각(KST): <strong>{}</strong></div>".format(
            len(orders), kst_now().strftime("%Y-%m-%d %H:%M:%S")),
        unsafe_allow_html=True
    )

    if orders:
        df = pd.DataFrame(orders)[["이름", "소속", "날짜", "시간", "메뉴"]]
        st.dataframe(df, use_container_width=True)

        from io import BytesIO, StringIO
        today_str = kst_now().strftime("%Y%m%d")
        excel_ok  = False

        for engine in ("openpyxl", "xlsxwriter"):
            try:
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine=engine) as writer:
                    df.to_excel(writer, index=False, sheet_name="주문내역")
                buf.seek(0)
                st.download_button(
                    label="📥 엑셀 다운로드 (.xlsx)",
                    data=buf,
                    file_name="cafe_orders_{}.xlsx".format(today_str),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                excel_ok = True
                break
            except Exception:
                continue

        if not excel_ok:
            csv_buf = StringIO()
            df.to_csv(csv_buf, index=False, encoding="utf-8-sig")
            st.warning("⚠️ 엑셀 라이브러리를 불러올 수 없어 CSV로 다운로드됩니다.")
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv_buf.getvalue().encode("utf-8-sig"),
                file_name="cafe_orders_{}.csv".format(today_str),
                mime="text/csv",
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("**날짜별 조회**")
        dates = sorted(set(o["날짜"] for o in orders), reverse=True)
        sel_date = st.selectbox("날짜 선택", dates)
        st.dataframe(df[df["날짜"] == sel_date], use_container_width=True)

        st.markdown("---")
        if st.button("🗑️ 전체 데이터 초기화", key="clear_data"):
            if st.session_state.get("confirm_clear"):
                save_orders([])
                st.session_state.confirm_clear = False
                st.success("초기화 완료!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("다시 한번 클릭하면 전체 데이터가 삭제됩니다!")
    else:
        st.info("아직 주문 내역이 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 메인으로", key="admin_home"):
            st.session_state.admin_auth = False
            st.session_state.page = "main"
            st.rerun()
    with col2:
        if st.button("🔓 로그아웃", key="admin_logout"):
            st.session_state.admin_auth = False
            st.rerun()


# ─── 라우터 ──────────────────────────────────────────────────────
{
    "main":        render_main,
    "select_name": render_select_name,
    "select_menu": render_select_menu,
    "success":     render_success,
    "admin":       render_admin,
}.get(st.session_state.page, render_main)()
