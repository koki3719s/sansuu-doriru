import streamlit as st
import random

st.set_page_config(page_title="算数ドリル", layout="centered")

st.title("🧮 算数ドリル")

# セッション状態の初期化
if 'stage' not in st.session_state:
    st.session_state.stage = "mode_select"      # "mode_select" → "level_select" → "playing" → "finished"
    st.session_state.mode = None
    st.session_state.level = None
    st.session_state.question_number = 0
    st.session_state.score = 0
    st.session_state.total_questions = 10
    st.session_state.current_a = None
    st.session_state.current_b = None
    st.session_state.correct_answer = None
    st.session_state.display_text = ""
    st.session_state.answered = False
    st.session_state.message = ""

# 問題生成関数
def generate_question():
    level = st.session_state.level
    
    if level == "easy":
        min_val, max_val = 1, 20
    elif level == "medium":
        min_val, max_val = 10, 99
    else:  # hard
        min_val, max_val = 100, 999
    
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)
    
    mode = st.session_state.mode
    
    if mode == "addition":
        correct = a + b
        display = f"{a} + {b} = "
    elif mode == "subtraction":
        if a < b: a, b = b, a
        correct = a - b
        display = f"{a} - {b} = "
    elif mode == "multiplication":
        correct = a * b
        display = f"{a} × {b} = "
    else:  # division
        if level == "easy":
            b = random.randint(2, 10)
            a = b * random.randint(2, 10)
        elif level == "medium":
            b = random.randint(5, 20)
            a = b * random.randint(3, 15)
        else:
            b = random.randint(10, 50)
            a = b * random.randint(5, 30)
        correct = a // b
        display = f"{a} ÷ {b} = "
    
    st.session_state.current_a = a
    st.session_state.current_b = b
    st.session_state.correct_answer = correct
    st.session_state.display_text = display
    st.session_state.answered = False
    st.session_state.message = ""

# ── モード選択画面 ──
if st.session_state.stage == "mode_select":
    st.header("モードを選んでください")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("足し算", use_container_width=True, type="primary"):
            st.session_state.mode = "addition"
            st.session_state.stage = "level_select"
            st.rerun()
        if st.button("引き算", use_container_width=True, type="primary"):
            st.session_state.mode = "subtraction"
            st.session_state.stage = "level_select"
            st.rerun()
    with col2:
        if st.button("掛け算", use_container_width=True, type="primary"):
            st.session_state.mode = "multiplication"
            st.session_state.stage = "level_select"
            st.rerun()
        if st.button("割り算", use_container_width=True, type="primary"):
            st.session_state.mode = "division"
            st.session_state.stage = "level_select"
            st.rerun()

# ── 難易度選択画面 ──
elif st.session_state.stage == "level_select":
    mode_name = {
        "addition": "足し算",
        "subtraction": "引き算",
        "multiplication": "掛け算",
        "division": "割り算"
    }.get(st.session_state.mode, "算数")
    
    st.header(f"{mode_name} の難易度を選択")
    
    if st.button("初級（1〜20くらい）", use_container_width=True):
        st.session_state.level = "easy"
        st.session_state.stage = "playing"
        generate_question()
        st.rerun()
    
    if st.button("中級（10〜99くらい）", use_container_width=True):
        st.session_state.level = "medium"
        st.session_state.stage = "playing"
        generate_question()
        st.rerun()
    
    if st.button("上級（100〜999くらい）", use_container_width=True):
        st.session_state.level = "hard"
        st.session_state.stage = "playing"
        generate_question()
        st.rerun()
    
    st.divider()
    if st.button("← モード選択に戻る", use_container_width=True, type="secondary"):
        st.session_state.stage = "mode_select"
        st.session_state.level = None
        st.rerun()

# ── 問題画面 ──
elif st.session_state.stage == "playing":
    st.markdown(f"**問題 {st.session_state.question_number + 1} / {st.session_state.total_questions}**")
    st.markdown(f"**現在の正解数：{st.session_state.score} / {st.session_state.question_number}**")
    
    st.divider()
    
    st.subheader("問題")
    st.markdown(f"<h2 style='text-align:center;'>{st.session_state.display_text}</h2>", unsafe_allow_html=True)
    
    user_input = st.number_input(
        "答えを入力してください",
        min_value=0,
        step=1,
        format="%d",
        key=f"answer_{st.session_state.question_number}",
        disabled=st.session_state.answered
    )
    
    if not st.session_state.answered:
        if st.button("答え合わせ", type="primary", use_container_width=True):
            if user_input == "":
                st.warning("数字を入力してください")
            else:
                try:
                    answer = int(user_input)
                    st.session_state.question_number += 1
                    
                    if answer == st.session_state.correct_answer:
                        st.session_state.score += 1
                        st.success("○ 正解！ すごい！ 🎉")
                        st.session_state.message = "正解です！"
                    else:
                        st.error(f"× 残念… 正解は **{st.session_state.correct_answer}** でした")
                        st.session_state.message = f"不正解（正解：{st.session_state.correct_answer}）"
                    
                    st.session_state.answered = True
                except ValueError:
                    st.warning("有効な数字を入力してください")
    
    if st.session_state.answered:
        st.info(st.session_state.message)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("次の問題へ →", type="primary", use_container_width=True):
                if st.session_state.question_number < st.session_state.total_questions:
                    generate_question()
                else:
                    st.session_state.stage = "finished"
                st.rerun()
        with col2:
            if st.button("← 難易度選択に戻る", type="secondary", use_container_width=True):
                st.session_state.stage = "level_select"
                st.session_state.question_number = 0
                st.session_state.score = 0
                st.rerun()

# ── 終了画面 ──
elif st.session_state.stage == "finished":
    st.subheader("終了！ お疲れ様でした！")
    percentage = (st.session_state.score / st.session_state.total_questions) * 100
    st.markdown(f"<h3 style='text-align:center;'>正解数：{st.session_state.score} / {st.session_state.total_questions} ({percentage:.1f}%)</h3>", unsafe_allow_html=True)
    
    if percentage >= 90:
        st.balloons()
        st.success("素晴らしい！ 天才レベルだね！ 🌟")
    elif percentage >= 70:
        st.success("よく頑張った！ えらいよ！ 👍")
    elif percentage >= 50:
        st.info("半分以上正解！ もう少しで上達するよ！")
    else:
        st.warning("次はもっと正解できるはず！ また挑戦しよう！")
    
    if st.button("最初からやり直す（モード選択へ）", type="primary", use_container_width=True):
        st.session_state.stage = "mode_select"
        st.session_state.mode = None
        st.session_state.level = None
        st.session_state.question_number = 0
        st.session_state.score = 0
        st.rerun()