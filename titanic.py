import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors
import streamlit as st
import base64
import time

df = sns.load_dataset('titanic')
# print(df.shape)
# print(df.columns.tolist())
# print(df.head(20))
# print(df.info())
# print(df.isnull().sum())
# print(df.dtypes)
# print("\n--- Kategorik Sütun İstatistikleri ---")
print(df.describe(include='object'))


############# all python codes ###############
total_passengers = df.shape[0]
total_children = (df['who'] == 'child').sum()
total_female = (df['who'] == 'woman').sum()
total_male = (df['who'] == 'man').sum()

total_survived = (df['survived'] == 1).sum()


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_file = "pics/titanic1.jpeg"
img_base64 = get_base64_of_bin_file(img_file)

page_bg_img = f"""
  <style>
    .stApp {{
      position: relative;
      z-index: 0;
    }}

    .stApp::before {{
      content: "";
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background-image: url("data:image/jpeg;base64,{img_base64}");
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      opacity: 0.3;
      z-index: -1;
    }}

    .stApp > div {{
      position: relative;
      z-index: 1;
    }}
  </style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.set_page_config(layout="wide")


st.markdown(f"""
  <style>
    .entrance{{
      text-align:center;
    }}   
    h1 {{
      font-size: 50px;
      padding: 10px;
      border-radius: 10px;
      max-width: 100%;
      margin: 20px auto 5px auto;
      color: white;
    }}
    .subtitle {{
      font-size: 30px;
      margin-top: 0px;
      color: white;
    }}
    .all {{
      color: white;
      margin-top: 0px;
      font-size: 20px;
    }}
    .tot_pass,
    .child_pass,
    .female_pass,
    .male_pass{{
      background: none;
      border: none;
      font-size: 25px;
      color: yellow;
    }}
    .tot_pass:hover,
    .child_pass:hover,
    .female_pass:hover,
    .male_pass:hover{{
      font-size: 30px;
      transition: font-size 0.4s ease;
    }}
    .survived_pass{{
      text-align:center;
      font-size: 18px;
      color: white;
    }}
  </style>
    
  <div class= "entrance">
    <h1>World of Titanic</h1>
      
    <div class="subtitle">
      <p>Peeking into the World of Titanic.</p>
    </div>

    <div class="all">
        <p class="total_people">
          There were <button class="tot_pass">{total_passengers}</button> people in Titanic.<br>
          <button class = "child_pass">{total_children}</button> children,
          <button class = "female_pass">{total_female}</button> female,
          <button class = "male_pass">{total_male}</button> male.
        </p>
    </div>
  </div> 
""",
unsafe_allow_html=True)



survived_placeholder = st.empty()
for i in range(total_survived + 1):
    survived_placeholder.markdown(
        f"""
        <div>
          <p class="survived_pass"
          style="
          text-align:center;
          color:yellow;">
            {i} passengers survived out of {total_passengers} passengers.
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.07)




# st.write(df.head(20))

# # Grafik çizimi
# plt.figure(figsize=(8,5))
# sns.countplot(data=df, x='sex')
# plt.title('Cinsiyete Göre Yolcuların Sayısı')
# st.pyplot(plt)
