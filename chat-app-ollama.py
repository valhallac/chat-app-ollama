import json
import os

import streamlit as st
import requests

st.write("# Welcome to Chat Assistant! 👋")
st.write("### :information_source: Chat Assistant powered by Ollama")

model = st.sidebar.selectbox("Model", ["llama2", "mistral", "phi", "llava"])
streaming = st.sidebar.selectbox("Streaming", [True, False])
BACKEND_URL = "http://localhost:11434/api/generate"

prompt = st.chat_input("Type a message...")
if prompt:
      st.markdown(prompt)
      if streaming:
            res = requests.post(f"{BACKEND_URL}/",
                                    json={
                                            "model": model,
                                            "prompt": prompt
                                    },
                                    stream=True)

            with st.chat_message("assistant"):
                  full_response = ""
                  message_placeholder = st.empty()
                  for line in res.iter_lines():
                        # Decode the line as JSON
                        data = json.loads(line)

                        # Check if the response is done
                        if data["done"]:
                              break

                        # Append the response to the full_response string
                        full_response += data["response"]

                        # Display the response in the chat window
                        message_placeholder.markdown(full_response)

      elif not streaming:
            with st.spinner("..."):
                  res = requests.post(f"{BACKEND_URL}/", 
                                      json={
                                                "model": model,
                                                "prompt": prompt,
                                                "stream": streaming
                                      }).json()
                  res = res['response']
                  with st.chat_message("assistant"):
                        st.markdown(res)