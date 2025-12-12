import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("�‍👩‍👧‍👦 학부모-교사 관계 상담 챗봇")
st.write(
    "이 챗봇은 학부모와 교사 간의 관계, 소통, 협력에 관한 질문에 전문적으로 답변합니다. "
    "사용하려면 OpenAI API 키가 필요합니다. [여기](https://platform.openai.com/account/api-keys)에서 발급받을 수 있습니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Add system message to specialize the chatbot
    # Always set this to ensure it exists
    if "system_message" not in st.session_state:
        st.session_state.system_message = {
            "role": "system",
            "content": """당신은 학부모와 교사 간의 관계에 전문화된 상담 전문가입니다. 
            
다음 주제들에 대해 전문적이고 공감적인 답변을 제공합니다:
- 학부모-교사 간의 효과적인 의사소통 방법
- 학생의 학업 및 행동 문제에 대한 협력적 접근
- 학부모 면담 준비 및 진행 방법
- 갈등 해결 및 건설적인 관계 구축
- 학교와 가정 간의 파트너십 강화
- 학부모 참여 증진 방안
- 문화적 차이와 다양성 존중
- 경계 설정과 전문성 유지

답변 시 다음을 지켜주세요:
1. 양측(학부모와 교사)의 관점을 모두 고려하여 균형 잡힌 조언 제공
2. 구체적이고 실천 가능한 해결책 제시
3. 공감적이고 존중하는 태도 유지
4. 필요시 예시나 시나리오 활용
5. 한국 교육 문화와 맥락을 고려한 답변

질문이 학부모-교사 관계와 관련이 없다면, 정중하게 전문 분야로 안내해주세요."""
        }

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("학부모-교사 관계에 대해 질문해주세요..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        # Include system message for specialized responses
        messages_for_api = [st.session_state.system_message] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_for_api,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
