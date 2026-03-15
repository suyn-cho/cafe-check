import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. 앱 페이지 설정 및 디자인
st.set_page_config(page_title="Cafe Order System", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2D2424; }
    h1, h2, h3, p, span, label { color: #E0C097 !important; }
    .stAlert { background-color: #5C3D2E; color: #E0C097; border: none; }
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #5C3D2E; color: #E0C097; border-radius: 10px;
        border: 1px solid #E0C097; font-weight: bold; width: 100%;
        margin-bottom: 10px;
    }
    /* 주문하기 버튼 (강조) */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #B85C38; color: white; border-radius: 25px;
        border: none; height: 3.5em; font-size: 1.1em;
    }
    /* 선택된 항목 표시 박스 */
    .selected-box {
        background-color: #B85C38; padding: 15px; border-radius: 10px;
        text-align: center; color: white; font-weight: bold; margin: 20px 0;
        border: 1px solid #E0C097;
    }
    </style>
    """, unsafe_allow_html=True)

# 상단 비주얼
st.image("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80", use_container_width=True)
st.title("☕ Cafe Order System")

# 데이터 저장 설정
DB_FILE = "cafe_usage_log.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["날짜", "소속", "이름", "메뉴"]).to_csv(DB_FILE, index=False, encoding='utf-8-sig')

# --- 데이터 정의 ---
member_data = {
    "생명": ["강서연", "박민형", "서석호", "서은주", "신금주", "정택연", "한정빈"],
    "카드": ["강홍석", "곽민준", "김보미", "김주희", "이상아", "정서라", "최송화"],
    "화재": ["권슬기", "배강현", "이원진", "이호철", "채수지", "최영철"],
    "증권": ["박가훈", "심예현", "양은원", "이수진", "조성진", "최민석", "한성원"],
    "강사": ["문현실", "박도형", "방혜진", "이우진"],
    "운영진": ["강병규", "김민정", "박진용", "이상은", "조수연", "조윤호"],
    "기타": []
}

menu_data = {
    "커피(coffee)": ["아메리카노", "달달커피", "헤이즐넛 아메리카노", "꿀화이트 아메리카노", "콜드브루", "카페라떼", "카푸치노", "바닐라라떼", "연유카페라떼", "카페모카", "화이트초콜릿모카", "카라멜마끼아또", "아포카토", "시그니처라떼", "넛츠크림라떼", "민트모카", "흑당콜드브루", "콜드브루라떼", "연유콜드브루"],
    "티(tea)": ["캐모마일", "히비스커스", "페퍼민트", "얼그레이", "루이보스", "아이스티", "아샷추", "아망추", "쌍화차", "배모과차", "살얼음식혜", "유자차", "자몽차", "레몬차", "생강차", "복분자뱅쇼", "로열밀크티"],
    "에이드(ade)": ["자몽포멜로에이드", "감귤레몬에이드", "꿀복숭아에이드", "머스캣모히또 에이드", "샹그리아에이드"],
    "논커피(non coffee)": ["흑당라떼", "미숫가루라떼", "초콜릿", "달고나라떼", "말차라떼", "민트초콜릿", "화이트초콜릿", "토피넛라떼", "고구마라떼", "딸기듬뿍라떼", "딸기초고라떼", "말차초코라떼", "버블흑당라떼"],
    "블렌디드(blended)": ["과일플랫치노", "밀크플랫치노", "요거트플랫치노", "밀크쉐이크", "초코쿠키쉐이크", "에스프레소쉐이크", "딸기쉐이크", "말차초코쉐이크"],
    "과일주스(fruit juice)": ["사과당근클렌즈주스", "키위케일샐러리 클렌즈주스", "딸기주스", "망고주스", "블루베리주스", "믹스주스"]
}

# 세션 상태 초기화
if 'sel_dept' not in st.session_state: st.session_state.sel_dept = ""
if 'sel_name' not in st.session_state: st.session_state.sel_name = ""
if 'sel_menu' not in st.session_state: st.session_state.sel_menu = ""

# --- 1. 소속 선택 (2열 배치) ---
st.subheader("1. 소속 선택")
dept_keys = ["생명", "카드", "화재", "증권", "강사", "운영진"]

# 2개씩 짝지어 버튼 생성
for i in range(0, len(dept_keys), 2):
    cols = st.columns(2)
    for j in range(2):
        d_name = dept_keys[i+j]
        if cols[j].button(d_name, key=f"dept_{d_name}"):
            st.session_state.sel_dept = d_name
            st.session_state.sel_name = "" # 소속 변경 시 이름 초기화

# 기타 버튼 (단독행)
if st.button("기타", key="dept_etc"):
    st.session_state.sel_dept = "기타"
    st.session_state.sel_name = ""

# 선택된 소속 표시 및 이름 입력
if st.session_state.sel_dept:
    st.markdown(f"<div style='color:#E0C097; font-weight:bold;'>선택된 소속: {st.session_state.sel_dept}</div>", unsafe_allow_html=True)
    if st.session_state.sel_dept == "기타":
        st.session_state.sel_name = st.text_input("성함을 입력하세요", key="input_etc_name")
    else:
        st.session_state.sel_name = st.selectbox("성함을 선택하세요", ["선택하세요"] + sorted(member_data[st.session_state.sel_dept]))

# --- 2. 메뉴 선택 ---
if st.session_state.sel_name and st.session_state.sel_name != "선택하세요":
    st.subheader("2. 메뉴 선택")
    cat_keys = list(menu_data.keys())
    
    # 카테고리 버튼 (2열 배치)
    for i in range(0, len(cat_keys), 2):
        c_cols = st.columns(2)
        for j in range(min(2, len(cat_keys)-i)):
            cat_name = cat_keys[i+j]
            if c_cols[j].button(cat_name, key=f"cat_{cat_name}"):
                st.session_state.sel_cat = cat_name

    # 세부 메뉴 버튼 (3열 그리드)
    if 'sel_cat' in st.session_state:
        st.write(f"**[{st.session_state.sel_cat}] 메뉴 클릭:**")
        m_cols = st.columns(3)
        for idx, item in enumerate(menu_data[st.session_state.sel_cat]):
            if m_cols[idx % 3].button(item, key=f"m_{item}"):
                st.session_state.sel_menu = item

# 선택 현황 요약
if st.session_state.sel_menu:
    st.markdown(f"<div class='selected-box'>{st.session_state.sel_name}님 선택: {st.session_state.sel_menu}</div>", unsafe_allow_html=True)

# --- 3. 주문하기 ---
if st.button("ORDER NOW (주문하기)", type="primary", use_container_width=True):
    if not st.session_state.sel_dept or not st.session_state.sel_name or not st.session_state.sel_menu or st.session_state.sel_name == "선택하세요":
        st.warning("모든 항목을 선택 완료해 주세요.")
    else:
        df = pd.read_csv(DB_FILE, encoding='utf-8-sig')
        today = datetime.now().strftime("%Y-%m-%d")
        used_count = len(df[(df['이름'] == st.session_state.sel_name) & (df['날짜'] == today)])
        
        if used_count >= 2:
            st.error(f"⚠️ 오늘 2회 주문하셨습니다. 내일 이용해 주세요.")
        else:
            new_row = {"날짜": today, "소속": st.session_state.sel_dept, "이름": st.session_state.sel_name, "메뉴": st.session_state.sel_menu}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
            st.balloons()
            st.success(f"주문 완료! (오늘 {used_count+1}회째)")
            # 초기화
            st.session_state.sel_menu = ""

# 관리자 보안 (비밀번호: 1234)
with st.expander("Admin"):
    if st.text_input("PW", type="password") == "1234":
        data = pd.read_csv(DB_FILE)
        st.dataframe(data)
        st.download_button("Download CSV", data.to_csv(index=False).encode('utf-8-sig'), "cafe_log.csv")
