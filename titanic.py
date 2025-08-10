import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors

df = sns.load_dataset('titanic')
df['sex'] = df['sex'].map({'male': 'Erkek', 'female': 'Kadın'})

# Cinsiyete göre hayatta kalanlar için
plt.figure(figsize=(6,4))
ax = sns.countplot(x='sex', hue='survived', data=df)
plt.title('Cinsiyete Göre Hayatta Kalanlar')
plt.xlabel('Cinsiyet')
plt.ylabel('Kişi Sayısı')
plt.legend(title='Durumu', labels=['Hayatını Kaybetti', 'Hayatta Kaldı'])

total_counts = df['sex'].value_counts()

def show_count_and_percent(sel):
  count=int(sel.target[1])
  bar_index=sel.index

  if bar_index in[0,1]:
    sex='Erkek'
  else:
    sex='Kadın'
  
  percent = count/total_counts[sex] * 100
  sel.annotation.set_text(f"{count} kişi\n%{percent:.1f}")

cursor = mplcursors.cursor(ax, hover=True)
cursor.connect("add", show_count_and_percent)

plt.show()