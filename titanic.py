import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import time

# Titanic verisi
df = sns.load_dataset('titanic')

#background
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

#basics
total_passengers = df.shape[0]
total_children = (df['who'] == 'child').sum()
total_female = (df['who'] == 'woman').sum()
total_male = (df['who'] == 'man').sum()
total_survived = (df['survived'] == 1).sum()

st.markdown(f"""
  <style>
    h1 {{ font-size:50px; color:white; text-align:center; }}
    .subtitle {{ font-size:30px; color:white; text-align:center; }}
    .stats {{ font-size:20px; color:white; text-align:center; }}
    .highlight {{ color: yellow; font-size:25px; }}
    .highlight:hover {{ font-size:30px; transition: font-size 0.4s; }}
    .survived {{ font-size:25px; color:yellow; text-align:center; font-weight:bold; }}
  </style>

  <h1>World of Titanic</h1>
  <div class="subtitle">Peeking into the World of Titanic.</div>
  <div class="stats">
    There were <span class="highlight">{total_passengers}</span> people in Titanic.<br>
    <span class="highlight">{total_children}</span> children, 
    <span class="highlight">{total_female}</span> female, 
    <span class="highlight">{total_male}</span> male.
  </div>
""", unsafe_allow_html=True)

#survived
survived_placeholder = st.empty()

for i in range(total_survived + 1):
    survived_placeholder.markdown(f"<div class='survived'>{i} passengers survived out of {total_passengers} passengers.</div>", unsafe_allow_html=True)
    time.sleep(0.0001)

#embarked icin
st.markdown(
    "<h1 style='text-align:center; color:#4682B4; font-size:30px; text-shadow: 2px 2px 5px rgba(0,0,0,0.5); margin-up: 10px;'>Passenger Distribution by Embarked</h2>",
    unsafe_allow_html=True
)

df['embarked'] = df['embarked'].astype('category')
df['embarked'] = df['embarked'].cat.add_categories(['Unknown']).fillna('Unknown')
df['embarked'] = df['embarked'].cat.rename_categories({'S':'Southampton', 'C':'Cherbourg', 'Q':'Queenstown'})

embarked_counts = df['embarked'].value_counts().reset_index()
embarked_counts.columns = ['Embarked', 'Count']

fig = px.bar(
    embarked_counts,
    x='Embarked',
    y='Count',
    color='Embarked',
    text='Count',
    title='Passenger Distribution by Embarked',
    color_discrete_map={
        'Southampton':'#0D3B66',
        'Cherbourg':'#F4D35E',
        'Queenstown':'#FFAD60',
        'Unknown':'#95A5A6'
    },
    hover_data={'Embarked': True, 'Count': True},
)

fig.update_traces(
    textposition='inside',
    marker_line_width=1.5,
    marker_line_color='white',
    opacity=0.9
)

fig.update_layout(
    width=800,
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.2)',
    bargap=0.6,
    font=dict(color='white'),
    showlegend=False
)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.plotly_chart(fig, use_container_width=False)

#passenger class icin
st.markdown(
    "<h1 style='text-align:center; color:#4682B4; font-size:30px; text-shadow: 2px 2px 5px rgba(0,0,0,0.5); margin-bottom:30px;'>Passenger Class Analysis</h1>",
    unsafe_allow_html=True
)

df['pclass'] = df['pclass'].astype('category')
df['pclass'] = df['pclass'].replace({1:'1st Class', 2:'2nd Class', 3:'3rd Class'})

class_counts = df['pclass'].value_counts().reset_index()
class_counts.columns = ['Passenger Class','Count']

cols = st.columns(len(class_counts))
for i, row in enumerate(class_counts.itertuples(index=False)):
    cols[i].metric(label=row[0], value=row[1])

fig_class_pie = px.pie(
    class_counts, 
    names='Passenger Class', 
    values='Count',
    color='Passenger Class',
    color_discrete_map={'1st Class':'#FFD700', '2nd Class':'#C0C0C0', '3rd Class':'#CD7F32'}
)
fig_class_pie.update_traces(textposition='inside', textinfo='percent+label')

fig_class_pie.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    font=dict(color='white')
)

st.plotly_chart(fig_class_pie, use_container_width=True)

### yaş analizi için
st.markdown(
    "<h1 style='text-align:center; color:#4682B4; font-size:30px; text-shadow: 2px 2px 5px rgba(0,0,0,0.5); margin-bottom:30px;'>Age Analysis</h1>",
    unsafe_allow_html=True
)

col1, col2 =st.columns(2)
with col1:
    survived_filter = st.multiselect(
        "Survived",
        options=[0, 1],
        default=[0, 1],
        format_func=lambda x: "Unalive" if x==0 else "Alive"
    )

with col2:
    sex_options_display = ["All", "Male", "Female"]
    sex_filter_display = st.radio(
        "Sex",
        options=sex_options_display,
        index=0,
        horizontal=True
    )

filtered_df = df[df['survived'].isin(survived_filter)]
if sex_filter_display != "All":
    filtered_df = filtered_df[filtered_df['sex'].str.lower() == sex_filter_display.lower()]

fig = px.histogram(
    filtered_df,
    x='age',
    color='survived',
    nbins=30,
    color_discrete_map={0:'red', 1:'green'},
    labels={'survived':'Survived'}
)

fig.update_layout(
    width=600,
    height=300,
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis_title="Age",
    yaxis_title="Passenger Count"
)

st.plotly_chart(fig)
