import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 앱 설정 및 안내문
st.set_page_config(page_title="카페 이용 체크", layout="centered")
st.title("☕ 카페 이용 체크 시스템")
st.markdown("---")
st.info("안녕하세요! 성함과 메뉴를 선택해 주세요. (1일 2회 제한)")

# 데이터 저장용 파일 (CSV) 생성
DB_FILE = "cafe_usage_log.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["날짜", "소속", "이름", "메뉴"])
    df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')

# 1. 소속 선택 (버튼형)
st.subheader("1. 소속 선택")
dept_list = ["생명", "카드", "화재", "증권", "강사", "운영진"]
selected_dept = st.pills("소속을 눌러주세요", dept_list) # 버튼처럼 동작하는 pill UI

# 2. 이름 입력
st.subheader("2. 이름 입력")
name = st.text_input("본인 성함을 입력하세요", placeholder="예: 홍길동")

# 3. 메뉴 선택
st.subheader("3. 메뉴 선택")
menu_list = ["아이스 아메리카노", "따뜻한 아메리카노", "카페라떼", "바닐라라떼", "복숭아 아이스티", "녹차/홍차"]
selected_menu = st.selectbox("메뉴를 골라주세요", menu_list)

# 제출 버튼
if st.button("체크인 하기", use_container_width=True, type="primary"):
    if not selected_dept or not name:
        st.warning("소속과 이름을 모두 입력/선택해 주세요.")
    else:
        # 데이터 불러오기 및 체크
        df = pd.read_csv(DB_FILE, encoding='utf-8-sig')
        today = datetime.now().strftime("%Y-%m-%d")
        user_today_count = len(df[(df['이름'] == name) & (df['날짜'] == today)])
        
        if user_today_count >= 2:
            st.error(f"⚠️ {name}님은 오늘 이미 2회 이용하셨습니다. 내일 이용해 주세요!")
        else:
            # 저장
            new_data = {"날짜": today, "소속": selected_dept, "이름": name, "메뉴": selected_menu}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
            st.success(f"✅ {name}님, 주문 기록이 완료되었습니다! (오늘 {user_today_count + 1}회째)")

# 관리자용 데이터 다운로드 (필요시)
with st.expander("관리자 확인용"):
    if os.path.exists(DB_FILE):
        admin_df = pd.read_csv(DB_FILE)
        st.dataframe(admin_df)
        st.download_button("엑셀(CSV) 다운로드", admin_df.to_csv(index=False).encode('utf-8-sig'), "cafe_log.csv", "text/csv")
