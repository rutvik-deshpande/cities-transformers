import streamlit as st
import openai
from dotenv import load_dotenv
import os 

openai.api_key = os.getenv('api_key')

st.set_page_config(layout="wide", page_icon="🏢", page_title="Cities Transfomer")
st.title("🏢 GPT-3 for 15' City Design")

def configure():
    load_dotenv()

left, right = st.columns(2)

right.subheader("Generated Solutions 🎉")

## right.image("template.png", width=300)

left.subheader("Describe the neighborhood 💬")
form = left.form("template_form")
siteLocation = form.text_input("Site Location (Neighborhood, City, Country)", "Amposta, Madrid, Spain")
expectedProgram = form.text_area("Expected Program", "creating pedestrian and bicycle paths, shifting away from private vehicle dependence. Addressing the lack of green areas in the site. Revitalise the neighborhood through making use of available spaces considering temporary occupancy and multi-use approaches. Improving the built environment to increase buildings energy efficiency. Promoting new activities and local commercial spaces in the interior of the city blocks")
siteArea = form.text_input("Site Area (in sqm)", "60000")

course = form.selectbox(
    "Choose course",
    ["Babbage"],
    index=0,
)
maxTokens = form.slider("Max. Tokens", 50, 150, 100)
submit = form.form_submit_button("Generate Solutions")


def gpt3_classifier(item, fine_tuned_model, is_log=False):
    
  # get the reuslt:
  # max token = 1 because to predict one class
  result = openai.Completion.create(model=fine_tuned_model, 
                                    prompt=str(item),
                                    max_tokens=maxTokens, temperature=0.7)['choices'][0]['text'] 
    
  if is_log: print('- ', item, ': ', result) 
    
  return result


if submit:
    ## with st.spinner(text="This may take a moment..."):
    text = "The site is located in " + siteLocation + "." + "The expected program is " + expectedProgram + "." + "The site area is " + siteArea + "sqm."
    response = gpt3_classifier(text + ' ', "babbage:ft-personal-2022-08-12-02-03-46")
    # text2 = gpt3_classifier
    right.write(response)

    st.balloons()

    right.success("💡 Neighborhood solution generated!")
