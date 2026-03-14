import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. 앱 페이지 설정 및 다크 브라운 디자인 적용
st.set_page_config(page_title="Cafe Order System", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2D2424; }
    h1, h2, h3, p, span, label { color: #E0C097 !important; }
    .stAlert { background-color: #5C3D2E; color: #E0C097; border: none; }
    /* 일반 메뉴 버튼 스타일 */
    .stButton>button {
        background-color: #5C3D2E; color: #E0C097; border-radius: 10px;
        border: 1px solid #E0C097; font-weight: bold; width: 100%;
        margin-bottom: 5px;
    }
    /* 주문하기 버튼 스타일 */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #B85C38; color: white; border-radius: 25px;
        border: none; height: 3.5em; font-size: 1.1em; margin-top: 20px;
    }
    /* 선택된 메뉴 표시 박스 */
    .selected-box {
        background-color: #B85C38; padding: 15px; border-radius: 10px;
        text-align: center; color: white; font-weight: bold; margin: 20px 0;
        border: 1px solid #E0C097;
    }
    </style>
    """, unsafe_allow_html=True)

# 상단 비주얼 및 제목
st.image("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80", use_container_width=True)
st.title("☕ Cafe Order System")

st.info("""
**[이용 안내]**
* 1인 1일 2회 주문 가능 (베이커리 및 그란데 사이즈 불가)
""")

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

# --- 1. 사용자 정보 입력 ---
st.subheader("1. 사용자 정보")
selected_dept = st.segmented_control("소속을 선택하세요", list(member_data.keys()))

name = ""
if selected_dept:
    if selected_dept == "기타":
        name = st.text_input("성함을 입력해 주세요")
    else:
        name = st.selectbox("성함을 선택하세요", ["선택하세요"] + sorted(member_data[selected_dept]))

# --- 2. 메뉴 선택 (버튼식) ---
st.subheader("2. 메뉴 선택")
selected_category = st.segmented_control("카테고리를 먼저 선택하세요", list(menu_data.keys()))

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = ""

if selected_category:
    st.write(f"**[{selected_category}] 세부 메뉴를 선택하세요:**")
    cols = st.columns(3) # 3열 그리드
    for idx, item in enumerate(menu_data[selected_category]):
        if cols[idx % 3].button(item, key=f"m_{idx}"):
            st.session_state.current_menu = item

# 선택된 메뉴 강조 표시
if st.session_state.current_menu:
    st.markdown(f"<div class='selected-box'>선택된 메뉴: {st.session_state.current_menu}</div>", unsafe_allow_html=True)

st.markdown("---")

# --- 3. 주문하기 버튼 ---
if st.button("ORDER NOW (주문하기)", use_container_width=True, type="primary"):
    if not selected_dept or not name or name == "선택하세요" or not st.session_state.current_menu:
        st.warning("정보를 모두 입력/선택해 주세요.")
    else:
        df = pd.read_csv(DB_FILE, encoding='utf-8-sig')
        today = datetime.now().strftime("%Y-%m-%d")
        count = len(df[(df['이름'] == name) & (df['날짜'] == today)])
        
        if count >= 2:
            st.error(f"⚠️ {name}님은 오늘 이미 2회 주문하셨습니다.")
        else:
            new_row = {"날짜": today, "소속": selected_dept, "이름": name, "메뉴": st.session_state.current_menu}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
            st.balloons()
            st.success(f"✅ 주문 완료! (오늘 {count + 1}회째 이용)")
            st.session_state.current_menu = "" # 완료 후 초기화

# --- 🔒 관리자 페이지 (보안) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("Admin Settings (관리자 전용)"):
    pw = st.text_input("관리자 암호", type="password")
    if pw == "1234": # 비밀번호를 원하는 숫자로 바꾸세요
        if os.path.exists(DB_FILE):
            data = pd.read_csv(DB_FILE)
            st.dataframe(data, use_container_width=True)
            st.download_button("엑셀(CSV) 다운로드", data.to_csv(index=False).encode('utf-8-sig'), "cafe_order_list.csv")
