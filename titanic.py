import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import time
import io

df = sns.load_dataset('titanic')


############# background image ###############
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_file = "pics/titanic1.jpeg"
img_base64 = get_base64_of_bin_file(img_file)


############# basic stats ###############
total_passengers = df.shape[0]
total_children = (df['who'] == 'child').sum()
total_female = (df['who'] == 'woman').sum()
total_male = (df['who'] == 'man').sum()
total_survived = (df['survived'] == 1).sum()

## arkaplan icin.
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
      font-size: 50px; padding: 10px; border-radius: 10px; color: white;
    }}
    .subtitle {{
      font-size: 30px; margin-top: 0px; color: white;
      }}
    .all {{ 
      color: white; margin-top: 0px; font-size: 20px; 
    }}
    .tot_pass, .child_pass, .female_pass, .male_pass {{
      background: none; border: none; font-size: 25px; color: yellow;
    }}
    .tot_pass:hover, .child_pass:hover, .female_pass:hover, .male_pass:hover {{
      font-size: 30px; transition: font-size 0.4s ease;
    }}
    .survived_pass{{
      text-align:center; font-size: 18px; color: white;
      }}
  </style>
    
  <div class="entrance">
    <h1>World of Titanic</h1>
    <div class="subtitle">
      <p>Peeking into the World of Titanic.</p>
    </div>
    <div class="all">
        <p class="total_people">
          There were <button class="tot_pass">{total_passengers}</button> people in Titanic.<br>
          <button class="child_pass">{total_children}</button> children,
          <button class="female_pass">{total_female}</button> female,
          <button class="male_pass">{total_male}</button> male.
        </p>
    </div>
  </div> 
""", unsafe_allow_html=True)


############# survived animation ###############
# CSS animasyonu
st.markdown("""
    <style>
    @keyframes countUp {
        from {
            transform: scale(0.9);
            opacity: 0.3;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }

    .survived_pass {
        text-align: center;
        font-size: 25px;
        font-weight: bold;
        color: yellow;
        animation: countUp 0.2s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)
survived_placeholder = st.empty()

# CountUp icin.
for i in range(total_survived + 1):
    survived_placeholder.markdown(
        f"""
        <p class="survived_pass">
            {i} passengers survived out of {total_passengers} passengers.
        </p>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.0001) 


############# deck analysis ###############
df['embarked'] = df['embarked'].astype('category')
df['embarked'] = df['embarked'].cat.add_categories(['Unknown']).fillna('Unknown')
df['embarked'] = df['embarked'].cat.rename_categories({'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'})

counts = df['embarked'].value_counts().reset_index()
counts.columns = ['embarked', 'count']

# Pie chart
fig = px.pie(
    counts,
    values='count',
    names='embarked',
    title='Passenger Distribution by Embarked',
    hover_data=['count'],
    labels={'count':'Number of Passengers'}
)

fig.update_traces(textposition='inside', textinfo='percent+label')

fig.update_layout(
       title={
        'text': "Passenger Distribution by Embarked",  # Başlık metni
        'x': 0.5,           # Ortalamak için
        'xanchor': 'center',# Ortalamanın referans noktası
        'font': {'color': '#4682B4', 'size': 24}  # Font rengi ve boyutu
    },
    legend_font_color='white',
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)


# sinif sayilari icin.
df['pclass'] = df['pclass'].replace({1: '1st Class', 2: '2nd Class', 3: '3rd Class'})

st.markdown("""
    <h1 style="
        color:#4682B4;
        text-align:center;
        font-size:30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">
        Titanic Yolcu Sınıf Dağılımı
    </h1>
""", unsafe_allow_html=True)

class_counts = df['pclass'].value_counts().reset_index()
class_counts.columns = ['Passenger Class', 'Count']

# Özet kartlar (Metric)
cols = st.columns(len(class_counts))
for i, row in class_counts.iterrows():
    cols[i].metric(label=row['Passenger Class'], value=row['Count'])

st.markdown("---")

# Pasta grafik
fig_pie = px.pie(class_counts, names='Passenger Class', values='Count',
                 title='Passenger Class Distribution',
                 color='Passenger Class',
                 color_discrete_map={'1st Class':'gold', '2nd Class':'silver', '3rd Class':'bronze'})

fig_pie.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Çubuk grafik
fig_pie = px.pie(class_counts, names='Passenger Class', values='Count',
                 title='Passenger Class Distribution',
                 color='Passenger Class',
                 color_discrete_map={
                     '1st Class': '#FFD700',  # gold
                     '2nd Class': '#C0C0C0',  # silver
                     '3rd Class': '#CD7F32'   # bronze
                 })

fig_pie.update_traces(textposition='inside', textinfo='percent+label')

fig_bar = px.bar(class_counts, x='Passenger Class', y='Count',
                 color='Passenger Class',
                 color_discrete_map={
                     '1st Class': '#FFD700',
                     '2nd Class': '#C0C0C0',
                     '3rd Class': '#CD7F32'
                 },
                 title='Passenger Count by Class',
                 text='Count')

fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(yaxis_title='Passenger Count', xaxis_title='Passenger Class')


st.plotly_chart(fig_bar, use_container_width=True)

df['alone'] = (df['sibsp'] + df['parch'] == 0)
df['alone'] = df['alone'].map({True: 'Alone', False: 'Not Alone'})

# sınıf renkleri
color_map = {
    '1st Class': '#FFD700',  # gold
    '2nd Class': '#C0C0C0',  # silver
    '3rd Class': '#CD7F32'   # bronze
}

fig_pie = px.pie(class_counts, names='Passenger Class', values='Count',
                 title='Passenger Class Distribution',
                 color='Passenger Class',
                 color_discrete_map=color_map)

fig_bar = px.bar(class_counts, x='Passenger Class', y='Count',
                 color='Passenger Class',
                 color_discrete_map=color_map,
                 title='Passenger Count by Class',
                 text='Count')

fig_bar.update_traces(textposition='outside')

# Alone durumu için pie chart
alone_counts = df['alone'].value_counts().reset_index()
alone_counts.columns = ['Alone Status', 'Count']

fig_pie_alone = px.pie(alone_counts, names='Alone Status', values='Count',
                       title='Passengers Alone vs Not Alone',
                       color='Alone Status',
                       color_discrete_map={'Alone': '#FF6F61', 'Not Alone': '#6B8E23'})

# Checkbox tablosu
if st.checkbox("Detaylı veri tablosunu göster"):
    st.dataframe(df[['pclass', 'alone', 'who', 'age']].head(20))

