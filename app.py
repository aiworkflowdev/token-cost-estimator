import streamlit as st
from token_calculator import count_tokens, estimate_cost, PRICING

#add streamlit app for token cost estimation
st.title("Token Cost Estimator")
st.write("This app estimates the cost of using OpenAI's GPT-3.5 and GPT-4 and xAI models")

#user input for text, model, and output tokens
input_option = st.radio("input method", ("Paste text", "Upload file"))
if input_option == "Paste text":
    text = st.text_area("Enter your text here:", height=200)
else:
    uploaded_file = st.file_uploader("Upload a file", type=["txt"])
    text = uploaded_file.read().decode("utf-8") if uploaded_file else ""
model = st.selectbox("Model", list(PRICING.keys()), index=3)
output_tokens = st.number_input("Estimated output tokens:", min_value=1, value=100, step=1)

#calculate and display results
if st.button("Calculate"):
    if text:
        try:
            input_tokens = count_tokens(text, model)
            input_cost, output_cost = estimate_cost(input_tokens, output_tokens, model)
            st.write(f"**Input tokens**: {input_tokens}")
            st.write(f"**Output tokens (estimated)**: {output_tokens}")
            st.write(f"**Estimated input cost**: ${input_cost:.4f}")
            st.write(f"**Estimated output cost**: ${output_cost:.4f}")
            st.write(f"**Total estimated cost**: ${(input_cost + output_cost):.4f}")
        except ValueError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
    else:
        st.error("Please enter text or upload a file to calculate the token cost.")

