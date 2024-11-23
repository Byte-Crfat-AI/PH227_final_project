import streamlit as st


# Have to be replaced with the responses of Gemini
def chatbot_response(user_input): 
    if user_input.lower() == "hello":
        return "Hi there! How can I help you?"
    elif user_input.lower() == "bye":
        return "Goodbye! Have a great day!"
    else:
        return f"You said: {user_input}"



st.set_page_config(page_title="Physics Department Chatbot", layout="centered")
st.title("QuantumQubie")



if "messages" not in st.session_state:
    st.session_state["messages"] = []



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    response = chatbot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
