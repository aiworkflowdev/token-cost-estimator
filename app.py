import streamlit as st
from token_calculator import count_tokens, estimate_cost, PRICING

#add streamlit app for token cost estimation
st.title("Token Cost Estimator")
st.write("This app estimates the cost of using OpenAI's GPT-3.5 and GPT-4 and xAI models")

#user input 
text = st.text_area("Enter your text here:", height=200) 
model = st.selectbox("Model", list(PRICING.keys()), index=3)
output_tokens = st.number_input("Estimated output tokens:", min_value=1, value=100, step=1)

#calculate and display results
if st.button("Calculate"):
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

