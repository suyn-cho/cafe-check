import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. 앱 페이지 설정 및 다크 브라운 테마 적용
st.set_page_config(page_title="Cafe Order System", layout="centered")

# CSS를 이용한 커스텀 디자인 (사진의 느낌 반영)
st.markdown("""
    <style>
    /* 전체 배경색 */
    .stApp {
        background-color: #2D2424;
    }
    /* 텍스트 색상 */
    h1, h2, h3, p, span, label {
        color: #E0C097 ! sectarian;
    }
    /* 안내문 박스 */
    .stAlert {
        background-color: #5C3D2E;
        border: none;
        color: #E0C097;
    }
    /* 버튼 및 입력창 테두리 둥글게 */
    .stButton>button {
        background-color: #B85C38;
        color: white;
        border-radius: 20px;
        border: none;
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #E0C097;
        color: #2D2424;
    }
    /* 드롭다운 및 입력창 스타일 */
    div[data-baseweb="select"] > div {
        background-color: #5C3D2E;
        border-radius: 10px;
        border: 1px solid #E0C097;
    }
    </style>
    """, unsafe_allow_status=True)

# 상단 이미지 영역 (사진 느낌의 플레이스홀더)
st.image("https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80", use_container_width=True)

st.title("☕ Cafe Order System")

# 안내 문구
st.info("""
**[Notice]**
* 1인 1일 2회 주문 가능
* 베이커리류 주문 불가 / 그란데 사이즈 불가
""")

# 데이터 저장 설정
DB_FILE = "cafe_usage_log.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["날짜", "소속", "이름", "메뉴"]).to_csv(DB_FILE, index=False, encoding='utf-8-sig')

# --- 데이터 정의 ---
member_data = {
    "생명": ["서은주", "박민형", "정택연", "서석호", "강서연", "신금주", "한정빈"],
    "카드": ["이상아", "김보미", "강홍석", "정서라", "곽민준", "최송화", "김주희"],
    "화재": ["이원진", "최영철", "이호철", "배강현", "채수지", "권슬기"],
    "증권": ["양은원", "이수진", "심예현", "조성진", "한성원", "박가훈", "최민석"],
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

# --- 주문 폼 영역 ---
with st.container():
    st.subheader("1. User Information")
    col1, col2 = st.columns(2)
    with col1:
        selected_dept = st.selectbox("소속", list(member_data.keys()))
    with col2:
        if selected_dept == "기타":
            name = st.text_input("성함 입력")
        else:
            name = st.selectbox("성함 선택", ["선택하세요"] + sorted(member_data[selected_dept]))

    st.subheader("2. Menu Selection")
    selected_category = st.segmented_control("카테고리", list(menu_data.keys()))

    selected_menu = ""
    if selected_category:
        selected_menu = st.selectbox(f"{selected_category} 메뉴 선택", ["메뉴를 선택하세요"] + menu_data[selected_category])

    st.markdown("---")
    
    # 주문하기 버튼
    if st.button("ORDER NOW", use_container_width=True):
        if not selected_dept or not name or name == "선택하세요" or not selected_menu or selected_menu == "메뉴를 선택하세요":
            st.warning("모든 정보를 선택해 주세요.")
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
                st.success(f"✅ 주문 완료! (오늘 {len(user_today) + 1}회째)")

# 관리자 영역
with st.expander("📊 Admin Dashboard"):
    if os.path.exists(DB_FILE):
        admin_df = pd.read_csv(DB_FILE)
        st.dataframe(admin_df, use_container_width=True)
        st.download_button("Excel 다운로드", admin_df.to_csv(index=False).encode('utf-8-sig'), "cafe_log.csv")
