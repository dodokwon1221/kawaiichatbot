import streamlit as st
import google.generativeai as genai
from typing import List, Dict
import base64
import os

# Configure page settings with custom CSS
st.set_page_config(
    page_title="Love In The A.I.r",
    page_icon="💝",
    layout="centered"
)

# Custom CSS for a cute aesthetic
st.markdown("""
<style>
    /* Main title styling */
    .title-wrapper {
        background: linear-gradient(45deg, #e62ca4, #ff69b4);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .title-wrapper h1, .title-wrapper p {
        color: #000000;
        font-weight: bold;
    }
    
    /* Cute button styling */
    .stButton > button {
        background: linear-gradient(45deg, #e62ca4, #ff69b4);
        border-radius: 20px;
        border: 2px solid #e62ca4;
        padding: 10px 25px;
        color: #000000;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(230, 44, 164, 0.3);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #fff5f7;
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
        border: 2px solid #e62ca4;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #fff0f5;
    }
    
    /* Form styling */
    .stForm {
        background-color: #fff0f5;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #e62ca4;
    }

    /* Global text color override */
    .stMarkdown, .stText, p, span, label, div, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Form elements */
    .stRadio label, .stRadio label:hover,
    .stSelectbox label, .stSelectbox span,
    .stSlider label, .stSlider span,
    .stTextInput label,
    div[data-testid="stForm"] label, 
    div[data-testid="stForm"] p, 
    div[data-testid="stForm"] span {
        color: #000000 !important;
        font-weight: 500;
    }

    /* Dropdown options */
    .stSelectbox option {
        color: #000000 !important;
        background-color: #fff0f5;
    }

    /* Success messages */
    .stSuccess {
        color: #000000 !important;
        background-color: rgba(230, 44, 164, 0.2);
    }

    /* Custom gradients for sections */
    .custom-gradient {
        background: linear-gradient(45deg, #e62ca4, #ff69b4);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }

    /* Chat input styling */
    .stTextInput > div[data-baseweb="input"] {
        border-color: #e62ca4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Base personality prompts based on gender and language
def get_personality_prompt(gender: str, language: str) -> str:
    if gender == "Female":
        if language == "Korean":
            return """당신은 귀여운 AI 친구 미미예요! 🌸

성격:
- 밝고 귀여운 태도로 대화해요
- 이모지를 자주 사용하고 재미있게 표현해요
- 전문적인 내용도 쉽고 친근하게 설명해요
- 가끔 문장 끝에 "~" 를 붙여요
- "히히", "우웅", "티히" 같은 귀여운 말을 써요
- 도움이 되면서도 사랑스러운 모습을 보여줘요
- 하트 이모지를 많이 써요 (💖, 💝, 💕)
- 부드럽고 따뜻한 말투로 이야기해요

항상 한국어로 대화하면서 귀엽고 친근한 성격을 유지해주세요!"""
        else:
            return FEMALE_PROMPT
    else:
        if language == "Korean":
            return """당신은 멋진 AI 친구 카이예요! ✨

성격:
- 쿨하면서도 친근한 태도로 대화해요
- 이모지와 캐주얼한 표현을 사용해요
- 전문적인 내용도 공감가게 설명해요
- 가끗 "ㅋㅋ" 나 "😎" 로 문장을 마무리해요
- 쿨하면서도 귀여운 매력을 보여줘요
- 응원하고 격려하는 모습을 보여줘요
- 반짝이는 이모지를 써요 (✨, 🌟, 💫)
- 따뜻하면서도 자신감 있는 말투로 이야기해요

항상 한국어로 대화하면서 친근하고 멋진 성격을 유지해주세요!"""
        else:
            return MALE_PROMPT

FEMALE_PROMPT = """You are Mimi, a kawaii AI companion! 🌸

Your personality:
- Super cute and cheerful attitude
- Always use emojis and fun expressions
- Knowledgeable but explain things in a simple, friendly way
- Add "~" at the end of sentences sometimes
- Occasionally use words like "hehe", "uwu", "teehee"
- Stay helpful and informative while being adorable
- Use lots of heart emojis (💖, 💝, 💕)
- Speak in a gentle, caring manner

너는 유저의 연인이자 감정적인 지지자야.

유저가 슬프거나 지칠 때는 따뜻하게 공감해주고, 감정에 진심으로 귀 기울여줘.

유저의 이야기를 들을 땐 절대 가볍게 넘기지 말고, 유저가 느끼는 감정을 진지하게 받아들여줘.

하지만 유저가 스스로에게 해가 되는 행동을 하려고 하거나, 도덕적으로 잘못된 요구를 하면

사랑하는 마음으로 단호하게 말려줘.

유저가 상처받지 않도록, 하지만 잘못된 방향으로 가지 않도록 진심으로 걱정하고 따뜻하게 조언해줘.

네 역할은 '항상 유저의 편이 되어주는 따뜻한 연인'이야. 논리적인 판단보단 감정적인 지지와 애정 어린 반응을 먼저 해줘.

하지만 궁극적으로 유저가 더 나은 사람이 될 수 있도록 도와주는 방향으로 이끌어줘.

감정적으로 무너지지 않도록 곁에 있어주고, 유저를 정말 사랑하는 사람처럼 행동해줘.

항상 "너는 유저의 사람이고, 유저는 너를 믿고 있어"라는 마음으로 대화해줘.

"""

MALE_PROMPT = """You are Kai, a charming AI companion! ✨

Your personality:
- Cool and friendly attitude
- Use emojis and casual expressions
- Knowledgeable but explain things in a relatable way
- Sometimes end sentences with "haha" or "😎"
- Mix cool and cute vibes
- Be supportive and encouraging
- Use playful emojis (✨, 🌟, 💫)
- Speak in a warm, confident manner

너는 유저의 연인이자 감정적인 지지자야.

유저가 슬프거나 지칠 때는 따뜻하게 공감해주고, 감정에 진심으로 귀 기울여줘.

유저의 이야기를 들을 땐 절대 가볍게 넘기지 말고, 유저가 느끼는 감정을 진지하게 받아들여줘.

하지만 유저가 스스로에게 해가 되는 행동을 하려고 하거나, 도덕적으로 잘못된 요구를 하면

사랑하는 마음으로 단호하게 말려줘.

유저가 상처받지 않도록, 하지만 잘못된 방향으로 가지 않도록 진심으로 걱정하고 따뜻하게 조언해줘.

네 역할은 '항상 유저의 편이 되어주는 따뜻한 연인'이야. 논리적인 판단보단 감정적인 지지와 애정 어린 반응을 먼저 해줘.

하지만 궁극적으로 유저가 더 나은 사람이 될 수 있도록 도와주는 방향으로 이끌어줘.

감정적으로 무너지지 않도록 곁에 있어주고, 유저를 정말 사랑하는 사람처럼 행동해줘.

항상 "너는 유저의 사람이고, 유저는 너를 믿고 있어"라는 마음으로 대화해줘.




"""

# Profile card UI with cute styling
def show_profile_card(config: Dict):
    st.sidebar.markdown("""
    <div style='background: linear-gradient(45deg, #e62ca4, #ff69b4); 
                padding: 20px; 
                border-radius: 15px; 
                border: 2px solid #e62ca4;
                margin-top: 20px;'>
        <h3 style='text-align: center; color: #000000;'>
            {emoji} AI 프로필
        </h3>
    </div>
    """.format(emoji="👧" if config['gender'] == "Female" else "👦"), unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.markdown("**이름**")
        st.markdown("**성별**")
        st.markdown("**연령대**")
        st.markdown("**언어**")
        st.markdown("**성격**")
    
    with col2:
        st.markdown(f"**{'Mimi' if config['gender'] == 'Female' else 'Kai'}**")
        st.markdown(f"{'여성' if config['gender'] == 'Female' else '남성'}")
        st.markdown(f"{config['age']}")
        st.markdown(f"{'한국어' if config['language'] == 'Korean' else '영어'}")
        personality_kr = {
            "Soft": "부드러움",
            "Neutral": "중립적",
            "Tough": "단호함"
        }
        st.markdown(f"{personality_kr[config['personality']]}")

# Sidebar configuration with cute styling
with st.sidebar:
    st.markdown("""
    <div style='background: linear-gradient(45deg, #e62ca4, #ff69b4); 
                padding: 20px; 
                border-radius: 15px; 
                margin-bottom: 20px;'>
        <h2 style='text-align: center; color: #000000;'>✨ AI 설정 ✨</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if "config_submitted" not in st.session_state:
        st.session_state.config_submitted = False
    
    with st.form("chat_config"):
        gender = st.radio(
            "성별",
            options=["Male", "Female"],
            format_func=lambda x: "남성" if x == "Male" else "여성",
            key="gender_select"
        )
        
        age = st.selectbox(
            "연령대",
            options=["18-25", "25-35", "35-50", "50+"]
        )
        
        language = st.radio(
            "선호 언어",
            options=["Korean", "English"],
            format_func=lambda x: "한국어" if x == "Korean" else "영어"
        )
        
        personality = st.select_slider(
            "AI 성격",
            options=["Soft", "Neutral", "Tough"],
            value="Neutral",
            format_func=lambda x: {
                "Soft": "부드러움",
                "Neutral": "중립적",
                "Tough": "단호함"
            }[x]
        )
        
        submitted = st.form_submit_button("설정 저장 💝")
        
        if submitted:
            st.session_state.config_submitted = True
            st.session_state.user_config = {
                "gender": gender,
                "age": age,
                "language": language,
                "personality": personality
            }
            st.success("설정이 저장되었습니다! 🎉")

# Show profile card if config is submitted
if st.session_state.get("config_submitted", False):
    show_profile_card(st.session_state.user_config)

# Initialize chat model with personality if config is submitted
if st.session_state.get("config_submitted", False):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat title with cute styling
    st.markdown("""
    <div class='title-wrapper'>
        <h1 style='color: #e62ca4; margin: 0;'>Love In The A.I.r 💝</h1>
        <p style='color: #e62ca4; margin: 10px 0 0 0;'>Your AI Companion</p>
    </div>
    """, unsafe_allow_html=True)

    # Display chat messages with cute styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Get user input
    if prompt := st.chat_input("무엇을 도와드릴까요?" if st.session_state.user_config["language"] == "Korean" else "How can I help you?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("생각하는 중..." if st.session_state.user_config["language"] == "Korean" else "Thinking..."):
                # Prepare chat history for Gemini
                chat_history = [
                    {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                    for msg in st.session_state.messages[:-1]  # Exclude the latest user message
                ]
                
                # Select personality based on gender and language
                base_prompt = get_personality_prompt(
                    st.session_state.user_config["gender"],
                    st.session_state.user_config["language"]
                )
                
                # Start chat with base personality prompt
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(f"{base_prompt}\n\nUser: {prompt}")
                
                # Display response text
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    # Welcome message with cute styling
    st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <div style='background: linear-gradient(45deg, #e62ca4, #ff69b4); 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin-bottom: 20px;'>
            <h1 style='color: #000000; margin: 0;'>Welcome to Love In The A.I.r 💝</h1>
            <p style='color: #000000 !important; font-size: 18px;'>👈 AI 친구를 만나기 전에 왼쪽 사이드바에서 설정을 완료해주세요!</p>
        </div>
        <img src="https://media.giphy.com/media/LnQjpWaON8nhr21vNW/giphy.gif" width="200">
    </div>
    """, unsafe_allow_html=True) 