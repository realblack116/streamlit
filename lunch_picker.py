import streamlit as st
import datetime
import random
import json
import os

st.title("오늘 뭐 먹지?")
st.subheader("랜덤 점심 메뉴 선택기")

DATA_FILE = "food_menu.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "korean": ["비빔밥", "김치찌개", "된장찌개", "불고기", "제육볶음", "갈비탕", "냉면", "떡볶이", "김밥", "부대찌개"],
        "chinese": ["짜장면", "짬뽕", "탕수육", "볶음밥", "마파두부", "양장피", "깐풍기", "군만두"],
        "japanese": ["초밥", "라멘", "돈까스", "우동", "규동", "가츠동", "오니기리", "텐동"],
        "western": ["파스타", "피자", "햄버거", "샌드위치", "스테이크", "리조또", "샐러드", "오믈렛"],
        "other": ["쌀국수", "카레", "타코", "팟타이", "케밥", "나시고랭"],
        "history": []
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")

data = load_data()

selected_date = st.sidebar.date_input("날짜 선택", today)
selected_date_str = selected_date.strftime("%Y-%m-%d")

st.sidebar.subheader("메뉴 카테고리")
categories = {
    "korean": "한식",
    "chinese": "중식",
    "japanese": "일식",
    "western": "양식",
    "other": "기타"
}

selected_categories = {}
for key, value in categories.items():
    selected_categories[key] = st.sidebar.checkbox(value, value=True)

st.sidebar.subheader("새 메뉴 추가")
with st.sidebar.form("add_menu"):
    new_menu = st.text_input("메뉴 이름")
    category = st.selectbox("카테고리", list(categories.values()))
    category_key = next((k for k, v in categories.items() if v == category), None)
    submit = st.form_submit_button("추가")
    if submit and new_menu and category_key:
        if new_menu not in data[category_key]:
            data[category_key].append(new_menu)
            save_data(data)
            st.sidebar.success(f"'{new_menu}'가 {category}에 추가됨")

if st.button("오늘의 메뉴 추천받기", type="primary"):
    all_menus = []
    for key, selected in selected_categories.items():
        if selected:
            all_menus.extend(data[key])
    if all_menus:
        today_menu = random.choice(all_menus)
        st.balloons()
        st.success(f"## 오늘의 추천 메뉴: {today_menu}")
        data["history"].append({
            "date": selected_date_str,
            "menu": today_menu
        })
        save_data(data)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("선택하기"):
                st.write("다시 선택하기")
        with col2:
            if st.button("👎 다시 추천받기"):
                st.experimental_rerun()
    else:
        st.error("선택된 카테고리가 없음")

st.header("메뉴 목록")
tab_names = list(categories.values())
tabs = st.tabs(tab_names)

for i, (key, name) in enumerate(categories.items()):
    with tabs[i]:
        if data[key]:
            col_count = 3
            menu_chunks = [data[key][i:i + col_count] for i in range(0, len(data[key]), col_count)]
            for chunk in menu_chunks:
                cols = st.columns(col_count)
                for j, menu in enumerate(chunk):
                    with cols[j]:
                        st.write(menu)
                        if st.button("삭제", key=f"delete_{key}_{menu}"):
                            data[key].remove(menu)
                            save_data(data)
                            st.success(f"'{menu}'가 삭제됨")
                            st.experimental_rerun()
        else:
            st.info(f"{name} 메뉴가 없음")

st.header("식사 히스토리")
history = data.get("history", [])

if history:
    history_by_date = {}
    for item in history:
        date = item["date"]
        if date not in history_by_date:
            history_by_date[date] = []
        history_by_date[date].append(item["menu"])
    for date in sorted(history_by_date.keys(), reverse=True):
        display_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y년 %m월 %d일")
        with st.expander(display_date):
            for i, menu in enumerate(history_by_date[date]):
                st.write(f"{i+1}. {menu}")
else:
    st.info("아직 식사 히스토리가 없음")

st.markdown("---")
st.caption("랜덤 점심 메뉴 선택기 © 2025.TEo")
