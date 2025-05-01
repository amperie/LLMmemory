import streamlit as st
from ChatManager import ChatManager

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "use_memory" not in st.session_state:
    st.session_state.use_memory = False


@st.cache_resource
def get_chat_manager():
    return ChatManager()


chat_manager = get_chat_manager()

# App title and description
st.title("🤖 Chatbot")
st.markdown("A simple chatbot with optional memory")

# Memory toggle
st.session_state.use_memory = st.checkbox(
    "Use Chat Memory", value=st.session_state.use_memory)
memory_text = st.text_input("User ID", key="memory_text")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from ChatManager
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat_manager.process_user_message(
                    user_id="1",
                    message=prompt,
                    use_memory=st.session_state.use_memory
                )
                st.markdown(response)

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
