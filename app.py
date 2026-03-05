import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. 앱 페이지 설정 및 테마 적용
st.set_page_config(page_title="Cafe Order System", layout="centered")

# CSS 커스텀 디자인 (사진의 다크 브라운 느낌 반영)
st.markdown("""
    <style>
    .stApp {
        background-color: #2D2424; /* 다크 브라운 배경 */
    }
    h1, h2, h3, p, span, label {
        color: #E0C097 !important; /* 베이지색 텍스트 */
    }
    .stAlert {
        background-color: #5C3D2E;
        color: #E0C097;
        border: none;
    }
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #B85C38; /* 오렌지 브라운 */
        color: white;
        border-radius: 25px;
        border: none;
        height: 3.5em;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #E0C097;
        color: #2D2424;
    }
    /* 드롭다운 스타일 */
    div[data-baseweb="select"] > div {
        background-color: #5C3D2E;
        border-radius: 10px;
        border: 1px solid #E0C097;
    }
    </style>
    """, unsafe_allow_html=True) # 오타 수정 완료

# 상단 이미지
st.image("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80", use_container_width=True)

st.title("☕ Cafe Order System")

# 안내 문구
st.info("""
**[Notice]**
* 성함과 메뉴를 선택해 주세요. (1인 1일 2회 제한)
* ⚠️ **베이커리류 주문 불가 / 그란데 사이즈 변경 불가**
""")

# 데이터 저장 설정
DB_FILE = "cafe_usage_log.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["날짜", "소속", "이름", "메뉴"]).to_csv(DB_FILE, index=False, encoding='utf-8-sig')

# --- 명단 및 메뉴 데이터 ---
member_data = {
    "생명": ["강서연", "박민형", "서석호", "서은주", "신금주", "정택연", "한정빈"],
    "카드": ["강홍석", "곽민준", "김보미", "김주희", "이상아", "정서라", "최송화"],
    "화재": ["권슬기", "이원진", "최영철", "이호철", "배강현", "채수지"],
    "증권": ["박가훈", "심예현", "양은원", "이수진", "조성진", "최민석", "한성원"],
    "강사": ["문현실", "이우진", "방혜진", "박도형"],
    "운영진": ["조수연", "강병규", "김민정", "이상은", "박진용", "조윤호"],
    "기타": []
}

menu_data = {
    "커피": ["아메리카노(Hot)", "아메리카노(Ice)", "카페라떼", "바닐라라떼", "카라멜마끼아또"],
    "음료": ["초코라떼", "그린티라떼", "고구마라떼", "밀크티"],
    "에이드": ["레몬에이드", "자몽에이드", "청포도에이드", "블루베리에이드"],
    "티": ["녹차", "홍차", "캐모마일", "페퍼민트", "유자차"],
    "과일주스": ["딸기주스", "망고주스", "키위주스", "토마토주스"]
}

# --- 주문 폼 ---
with st.container():
    st.subheader("1. User Information")
    selected_dept = st.segmented_control("소속을 선택하세요", list(member_data.keys()))

    name = ""
    if selected_dept:
        if selected_dept == "기타":
            name = st.text_input("성함을 직접 입력하세요")
        else:
            name = st.selectbox("성함을 선택하세요", ["선택하세요"] + sorted(member_data[selected_dept]))

    st.subheader("2. Menu Selection")
    selected_category = st.segmented_control("카테고리를 선택하세요", list(menu_data.keys()))

    selected_menu = ""
    if selected_category:
        selected_menu = st.selectbox(f"{selected_category} 세부 메뉴", ["메뉴를 선택하세요"] + menu_data[selected_category])

    st.markdown("---")
    
    # 주문하기 버튼
    if st.button("ORDER NOW (주문하기)", use_container_width=True):
        if not selected_dept or not name or name == "선택하세요" or not selected_menu or selected_menu == "메뉴를 선택하세요":
            st.warning("정보를 모두 선택해 주세요.")
        else:
            df = pd.read_csv(DB_FILE, encoding='utf-8-sig')
            today = datetime.now().strftime("%Y-%m-%d")
            user_today = df[(df['이름'] == name) & (df['날짜'] == today)]
            
            if len(user_today) >= 2:
                st.error(f"⚠️ {name}님은 오늘 이미 2회 주문하셨습니다.")
            else:
                new_data = {"날짜": today, "소속": selected_dept, "이름": name, "메뉴": selected_menu}
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
                st.balloons()
                st.success(f"✅ {name}님, 주문 완료! (오늘 {len(user_today) + 1}회째)")

# 관리자 대시보드
with st.expander("📊 Admin Dashboard"):
    if os.path.exists(DB_FILE):
        admin_df = pd.read_csv(DB_FILE)
        st.dataframe(admin_df, use_container_width=True)
        st.download_button("Excel(CSV) 다운로드", admin_df.to_csv(index=False).encode('utf-8-sig'), "cafe_log.csv")
