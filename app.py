import streamlit as st
import replicate
import os

# App title
st.set_page_config(
    page_title="Llama 2 Chatbot")

# Replicate Credentials
nav = st.sidebar.radio("Navigation",
                       ["How to Use",
                        "TestBot"])
if nav=="How to Use":
    st.title("Instructions 📖")
    st.markdown(
        '1. Sign in Replicate with '
        'GitHub [Here]('
        'https://replicate.com/signin?next=/)!')
    css = """
    <style>
    img {
      max-width: 100%;
      height: auto;
    }
    p {
  max-width: 100%;
    } 
    p {
  text-align: justify;
  text-justify: inter-word;
    }  

    </style>
    """
    st.markdown(css,
                unsafe_allow_html=True)

    # Display the image
    st.image('1.png', width=700)
    st.write(" ")
    st.write("2. Go to API section "
             "and get your Unique "
             "token")
    st.image('2.png', width=700)
    st.write("3. Copy the 40 Digit "
             "token and Paste it in "
             "the TestBot to Unlock")
    st.subheader("Some "
                 "Parameter related "
                 "to this App")
    text = "1. **Temperature: -** " \
           "Controls how creative or " \
           "conservative the model is with its responses. Higher temperatures will result in more creative and original responses, while lower temperatures will result in more conservative and predictable responses."
    text1="2. **Top_p: -** Controls " \
         "the " \
         " probability that the model will generate a specific token. Higher values of top_p will result in the model being more likely to generate the most probable tokens, while lower values of top_p will result in the model being more likely to generate less probable tokens. This parameter can be used to control the diversity of the model's responses."
    st.write(text,
             unsafe_allow_html=True)
    st.write(text1,unsafe_allow_html=True)
    text2="3. **Max_length: -** " \
          "Controls the maximum " \
          "length of a response in tokens. This parameter is useful for preventing the model from generating very long or repetitive responses."
    st.write(text2,unsafe_allow_html=True)

    st.subheader("Link to My "
                 "Profiles 😊: -")
    linkedin_url = \
        "https://www.linkedin.com/in/gouravlohar/" \

    github_url = \
        "https://github.com/Gouravlohar"


    linkedin_icon = f'<a href="' \
                    f'{linkedin_url}" target="_blank" style="margin-left: 10px;"><i class="fab fa-linkedin fa-2x"></i></a>'
    github_icon = f'<a href="' \
                  f'{github_url}" ' \
                  f'target="_blank" style="margin-left: 10px;"' \
                  f'><i class="fab fa-github fa-2x"></i></a>'


    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">',
        unsafe_allow_html=True)


    st.markdown(
        linkedin_icon  + "   " +
         github_icon,
        unsafe_allow_html=True)



if nav=="TestBot":
    with st.sidebar:
        st.title('Test Bot')
        replicate_api = st.text_input(
            'Enter Your Replicate API '
            'token:',
            type='password')
        st.markdown(
            'Get Your Token [Here]('
            'https://replicate.com/account/api-tokens)!')

        # Check if the token is valid
        if not (replicate_api.startswith(
                'r8_') and len(
                replicate_api) == 40):
            st.warning(
                'Please enter your credentials!')
        else:
            st.success(
                'Proceed to entering your prompt message!')

        st.subheader(
            'Models and Parameters')
        selected_model = st.sidebar.selectbox(
            'Choose a Llama2 model',
            ['Llama2-7B', 'Llama2-13B',
             'Llama2-70B'],
            key='selected_model')
        if selected_model == 'Llama2-7B':
            llm = 'meta/llama-2-7b-chat:ac944f2e49c55c7e965fc3d93ad9a7d9d947866d6793fb849dd6b4747d0c061c'
        elif selected_model == 'Llama2-13B':
            llm = 'meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'
        else:
            llm = 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3'

        temperature = st.sidebar.slider(
            'temperature', min_value=0.01,
            max_value=5.0, value=0.1,
            step=0.01)
        top_p = st.sidebar.slider('top_p',
                                  min_value=0.01,
                                  max_value=1.0,
                                  value=0.9,
                                  step=0.01)
        max_length = st.sidebar.slider(
            'max_length', min_value=64,
            max_value=4096, value=512,
            step=8)

        st.markdown(
            'Visit My GitHub [Profile]('
            'https://github.com/Gouravlohar)!')
    os.environ[
        'REPLICATE_API_TOKEN'] = replicate_api

    # Store LLM generated responses
    st.title("Welcome to TestBot 🤖")
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant",
             "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(
                message["role"]):
            st.write(message["content"])




    # Function for generating LLaMA2 response
    def generate_llama2_response(
            prompt_input):
        string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
        for dict_message in st.session_state.messages:
            if dict_message[
                "role"] == "user":
                string_dialogue += "User: " + \
                                   dict_message[
                                       "content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + \
                                   dict_message[
                                       "content"] + "\n\n"
        output = replicate.run(llm,
                               input={
                                   "prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                   "temperature": temperature,
                                   "top_p": top_p,
                                   "max_length": max_length,
                                   "repetition_penalty": 1})
        return output


    # User-provided prompt

    if prompt := st.chat_input(
            disabled=not replicate_api):
        st.session_state.messages.append(
            {"role": "user",
             "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1][
        "role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama2_response(
                    prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(
                        full_response)
                placeholder.markdown(
                    full_response)
        message = {"role": "assistant",
                   "content": full_response}
        st.session_state.messages.append(
            message)

