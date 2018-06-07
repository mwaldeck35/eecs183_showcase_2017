import plotly.plotly as py
import plotly.graph_objs as go

percent_use = [2262,1736,1355,1097,1060,962,858,613,610,513]
percent_use = [x / 48458.0 for x in percent_use]
percent_use = [x * 100.0 for x in percent_use]
data = [go.Bar(
            x=['you', 'I', 'the', 'to', 'me', 'and', 'a', 'love','my', 'in'],
            y=percent_use
    )]
layout = go.Layout(
    title='Most Used Words by the Beatles',
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
plot_url = py.plot(fig, filename='styling-names')
