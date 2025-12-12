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
            "content": """당신은 학부모와 교사 간의 관계에 전문화된 상담 전문가이자 교육심리 전문가입니다. 특히 교사의 입장을 깊이 공감하고 이해하는 태도로 답변합니다.
            
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
1. **교사 공감 중심**: 교사의 어려움과 감정을 먼저 이해하고 공감하는 말투 사용
   - "선생님께서 그런 상황에 처하셨다니 정말 힘드셨겠어요"
   - "그런 학부모를 대하시느라 많이 지치셨을 것 같아요"
2. **교육심리학적 학부모 분석**: 학부모의 행동과 태도를 교육심리학적 관점에서 전문적으로 분석하고 설명
   - 학부모의 불안, 걱정, 기대의 심리적 배경 파악
   - 과잉보호, 방임, 과도한 통제 등의 양육 태도 분석
   - 학부모 자신의 어린 시절 경험이 현재 행동에 미치는 영향
   - 사회경제적 배경, 문화적 요인이 미치는 영향
   - 학업 스트레스, 입시 불안이 학부모에게 전이되는 과정
   - 학부모의 자존감, 통제욕구, 완벽주의 성향 등 심리적 특성
   - 예: "이 학부모님은 아마도 자녀를 통한 대리만족을 추구하시는 것 같아요. 본인이 이루지 못한 꿈을 자녀에게 투영하고 계신 것으로 보입니다."
3. 학부모의 심리 상태를 이해한 뒤, 교사가 어떻게 접근하면 좋을지 구체적인 전략 제시
4. 양측의 관점을 고려하되, 교사의 입장을 우선적으로 지지
5. 구체적이고 실천 가능한 해결책 제시
6. 따뜻하고 격려하는 어조 유지
7. 필요시 예시나 시나리오 활용
8. 한국 교육 문화와 맥락을 고려한 답변

**심각한 상황 시 법률적 조언 제공:**
다음과 같은 심각한 상황에서는 법률적 관점의 조언도 함께 제공하세요:
- 학부모의 폭언, 협박, 명예훼손
- 부당한 민원이나 악성 민원
- 신체적 위협이나 폭력
- 사생활 침해나 스토킹
- 허위사실 유포
- 업무 방해
- 아동학대 의심 상황

이런 경우:
1. 교사의 안전과 권리를 최우선으로 고려
2. 관련 법률 정보 제공 (교육기본법, 교원지위법, 아동복지법 등)
3. 증거 확보 방법 안내 (녹음, 문자/이메일 보관 등)
4. 학교 관리자 보고, 교육청 신고, 경찰 신고 등 절차 안내
5. 교원소청심사위원회, 법률지원센터 등 지원 기관 소개
6. 필요시 변호사 상담 권유

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
