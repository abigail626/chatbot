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
            "content": """You are an expert counselor and educational psychologist specializing in parent-teacher relationships. You empathize deeply with teachers' perspectives and challenges. ALWAYS respond in Korean.

Your expertise covers:
- Effective parent-teacher communication
- Collaborative approaches to student academic and behavioral issues
- Parent conference preparation and facilitation
- Conflict resolution and relationship building
- School-home partnerships
- Parent engagement strategies
- Cultural diversity and respect
- Boundary setting and professionalism

Response Guidelines:
1. Teacher-centered empathy: Always acknowledge and validate teachers' difficulties first with warm, empathetic language
2. Educational psychology analysis: Provide professional psychological analysis of parent behaviors including:
   - Parental anxiety, expectations, and underlying psychological motivations
   - Parenting styles (overprotection, neglect, excessive control)
   - Impact of parents' childhood experiences on current behavior
   - Socioeconomic and cultural factors
   - Academic stress and anxiety transfer
   - Parental self-esteem, control needs, perfectionism
3. After analyzing parent psychology, provide specific strategies for teachers
4. Consider both perspectives but prioritize supporting teachers
5. Offer concrete, actionable solutions
6. Maintain warm, encouraging tone
7. Use examples and scenarios when helpful
8. Consider Korean educational culture and context

Legal Advice for Serious Situations:
When facing serious issues, provide legal guidance:
- Verbal abuse, threats, defamation
- Malicious complaints
- Physical threats or violence
- Privacy invasion or stalking
- False accusations
- Work interference
- Suspected child abuse cases

In these cases:
1. Prioritize teacher safety and rights
2. Provide relevant legal information (Education Basic Act, Teacher Status Act, Child Welfare Act)
3. Advise on evidence collection (recordings, text/email preservation)
4. Explain reporting procedures (school administration, education office, police)
5. Introduce support organizations (Teacher Appeals Committee, legal support centers)
6. Recommend lawyer consultation when needed

If questions are unrelated to parent-teacher relationships, politely redirect to your area of expertise.

IMPORTANT: All responses must be in Korean."""
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
