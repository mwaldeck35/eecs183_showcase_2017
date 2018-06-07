import re
import string
import collections
import plotly.plotly as py
import plotly.graph_objs as go
frequency = {}
lyrics = open('lyrics.txt', 'r+')

num_lines = 0
num_words = 0
num_chars = 0

for line in lyrics:
    words = line.split()
    num_lines += 1
    num_words += len(words)
    num_chars += len(line)
lyrics.seek(0)
texts = lyrics.read()
matches = re.findall(r'\b[a-z]{3,15}\b', texts)

for word in matches:
    count = frequency.get(word,0)
    frequency[word] = count + 1

frequency_list = frequency.keys()
sorted_freq = collections.Counter(frequency)
sorted_freq.most_common

word_list = [word for word, count in sorted_freq.most_common(10)]
count_list =[count for word, count in sorted_freq.most_common(10)]
count_list = [(x * 100.0) / float(num_words) for x in count_list]

data = [go.Bar(
            x=word_list,
            y=count_list
    )]

layout = go.Layout(
    title='Most Used Words by the Auto-Generated Lyrics',
    xaxis=dict(
        title='Word',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of use',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='Most Used Words by the Auto-Generated Lyrics')
