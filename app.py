import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 앱 설정 및 안내문
st.set_page_config(page_title="카페 이용 체크", layout="centered")
st.title("☕ 카페 이용 주문 시스템")
st.markdown("---")

# 안내 문구 수정: 베이커리 및 사이즈 제한 추가
st.info("""
**[이용 안내]**
* 성함과 메뉴를 선택해 주세요. (1인 1일 2회 제한)
* ⚠️ **베이커리류 주문 불가**
* ⚠️ **그란데 사이즈 변경 불가**
""")

# 데이터 저장용 파일 (CSV) 설정
DB_FILE = "cafe_usage_log.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["날짜", "소속", "이름", "메뉴"]).to_csv(DB_FILE, index=False, encoding='utf-8-sig')

# --- 명단 데이터 ---
member_data = {
    "생명": ["서은주", "박민형", "정택연", "서석호", "강서연", "신금주", "한정빈"],
    "카드": ["이상아", "김보미", "강홍석", "정서라", "곽민준", "최송화", "김주희"],
    "화재": ["이원진", "최영철", "이호철", "배강현", "채수지", "권슬기"],
    "증권": ["양은원", "이수진", "심예현", "조성진", "한성원", "박가훈", "최민석"],
    "강사": ["문현실", "이우진", "방혜진", "박도형"],
    "운영진": ["조수연", "강병규", "김민정", "이상은", "박진용", "조윤호"],
    "기타": []
}

# --- 메뉴 데이터 (대분류 -> 소분류) ---
menu_data = {
    "커피": ["아메리카노(Hot)", "아메리카노(Ice)", "카페라떼", "바닐라라떼", "카라멜마끼아또"],
    "음료": ["초코라떼", "그린티라떼", "고구마라떼", "밀크티"],
    "에이드": ["레몬에이드", "자몽에이드", "청포도에이드", "블루베리에이드"],
    "티": ["녹차", "홍차", "캐모마일", "페퍼민트", "유자차"],
    "과일주스": ["딸기주스", "망고주스", "키위주스", "토마토주스"]
}

# 1. 소속 및 이름 선택
st.subheader("1. 사용자 정보")
dept_list = list(member_data.keys())
selected_dept = st.segmented_control("소속을 선택하세요", dept_list)

name = ""
if selected_dept:
    if selected_dept == "기타":
        name = st.text_input("성함을 직접 입력하세요")
    else:
        name_list = ["선택하세요"] + sorted(member_data[selected_dept])
        name = st.selectbox("성함을 선택하세요", name_list)

# 2. 메뉴 선택 (버튼형 대분류 -> 드롭다운 소분류)
st.subheader("2. 메뉴 선택")
selected_category = st.segmented_control("카테고리를 선택하세요", list(menu_data.keys()))

selected_menu = ""
if selected_category:
    detailed_menus = ["메뉴를 선택하세요"] + menu_data[selected_category]
    selected_menu = st.selectbox(f"{selected_category} 세부 메뉴", detailed_menus)

# 3. 주문하기 버튼 (문구 수정)
if st.button("주문하기", use_container_width=True, type="primary"):
    if not selected_dept or not name or name == "선택하세요" or not selected_menu or selected_menu == "메뉴를 선택하세요":
        st.warning("정보를 모두 입력/선택해 주세요.")
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
            st.success(f"✅ {name}님, 주문이 완료되었습니다! (오늘 {len(user_today) + 1}회째)")

# 관리자 확인용
with st.expander("📊 관리자 데이터 확인"):
    if os.path.exists(DB_FILE):
        admin_df = pd.read_csv(DB_FILE)
        st.dataframe(admin_df, use_container_width=True)
        st.download_button("데이터 다운로드(CSV)", admin_df.to_csv(index=False).encode('utf-8-sig'), "cafe_log.csv")
