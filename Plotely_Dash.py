import dash
import requests
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html,Input, Output


app = dash.Dash(__name__,external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css'])

year=2023

def create_movie_popularity_chart(year):
    url_movie = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&year={year}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlNWQ5OTUxYTdiNzg0ZTZkMDBjZjk3OGU4YjcyYyIsInN1YiI6IjY1Mzc3YzIxYzUwYWQyMDEyZGY0YjI2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jMOywP2uIuyrtnbX0kYWNkbGf0wTMUnNmKsFrNhcVXU"
    }
    response_movie = requests.get(url_movie, headers=headers)
    data_movie = response_movie.json()['results']
    movie_titles = [movie['original_title'] for movie in data_movie]
    popularity_movie = [movie['popularity'] for movie in data_movie]

    title = f"Popularité des films populaires en {year}"

    fig_movie = px.bar(x=movie_titles, y=popularity_movie, labels={'x': 'Film', 'y': 'Popularité'},
                       title=title, hover_name=None, color_discrete_sequence=['pink'])

    return fig_movie

def create_movie_vote_chart(year):
    url_movie = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&year={year}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlNWQ5OTUxYTdiNzg0ZTZkMDBjZjk3OGU4YjcyYyIsInN1YiI6IjY1Mzc3YzIxYzUwYWQyMDEyZGY0YjI2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jMOywP2uIuyrtnbX0kYWNkbGf0wTMUnNmKsFrNhcVXU"
    }
    response_movie = requests.get(url_movie, headers=headers)
    data_movie = response_movie.json()['results']
    movie_titles = [movie['original_title'] for movie in data_movie]
    vote_movie = [movie['vote_average'] for movie in data_movie]

    title = f"Votes des films populaires en {year}"
    fig_vote = px.bar(x=movie_titles, y=vote_movie, labels={'x': 'Film', 'y': 'Vote'},
                      title=title, hover_name=None)

    return fig_vote

def create_people_popularity():
    url_people = "https://api.themoviedb.org/3/trending/person/day?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlNWQ5OTUxYTdiNzg0ZTZkMDBjZjk3OGU4YjcyYyIsInN1YiI6IjY1Mzc3YzIxYzUwYWQyMDEyZGY0YjI2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jMOywP2uIuyrtnbX0kYWNkbGf0wTMUnNmKsFrNhcVXU"
    }
    response_people = requests.get(url_people, headers=headers)
    data_people = response_people.json()['results']
    people_names = [person['original_name'] for person in data_people]
    popularity_people = [person['popularity'] for person in data_people]

    fig_people = px.line_polar(r=popularity_people, theta=people_names, line_close=True,
                               color_discrete_sequence=['red'])
    fig_people.update_traces(fill='toself')
    fig_people.update_layout(polar=dict(radialaxis=dict(visible=True)))

    return  fig_people

def create_tv_popularity(year):
    url_tv = f"https://api.themoviedb.org/3/discover/tv?first_air_date_year={year}&include_adult=false&include_null_first_air_dates=false&language=en-US&page=1&sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlNWQ5OTUxYTdiNzg0ZTZkMDBjZjk3OGU4YjcyYyIsInN1YiI6IjY1Mzc3YzIxYzUwYWQyMDEyZGY0YjI2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jMOywP2uIuyrtnbX0kYWNkbGf0wTMUnNmKsFrNhcVXU"
    }
    response_tv = requests.get(url_tv, headers=headers)
    data_series = response_tv.json()['results']
    series_titles = [serie['name'] for serie in data_series]
    popularity_tv = [serie['popularity'] for serie in data_series]
    vote_average_tv = [serie['vote_average'] for serie in data_series]
    fig_tv = go.Figure()
    fig_tv.add_trace(go.Scatter(
        x=popularity_tv,
        y=vote_average_tv,
        mode='markers',
        text=series_titles,
        marker=dict(size=10, opacity=0.5, color='black')

    ))
    title=f"Popularité et votes des séries populaires en {year}"
    fig_tv.update_layout(
        title=title,
        xaxis_title="Popularité",
        yaxis_title="Note Moyenne"

    )
    fig_tv.update_traces(textposition='top center', hoverinfo='text+x+y')

    return fig_tv


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H4("FilmaGraph", className="text-white"),
            html.Span("", className="text-muted")
        ], className="bg-dark p-4"),

        dcc.Graph(id='selected-graph', config={'scrollZoom': False})
    ]),

    dcc.Dropdown(
        id='graph-selector',
        options=[
            {'label': 'Popularité des films', 'value': 'movie-popularity'},
            {'label': 'Vote des films', 'value': 'movie-vote'},
            {'label': 'Popularité des célébrités', 'value': 'people-popularity'},
            {'label': 'Graphique des séries', 'value': 'tv-popularity'}
        ],
        value='movie-popularity',
    ),
dcc.Input(
        id='year-input',
        type='number',
        value=year,
        placeholder='Année',
        min=1900,
        max=2100,
        step=1,
    ),
    html.Div([
        html.Footer([
            html.Ul([
                html.Li(html.A("Home", href='#', className="nav-link px-2 text-muted")),
                html.Li(html.A("Features", href='#', className="nav-link px-2 text-muted")),
                html.Li(html.A("Pricing", href='#', className="nav-link px-2 text-muted")),
                html.Li(html.A("FAQs", href='#', className="nav-link px-2 text-muted")),
                html.Li(html.A("About", href='#', className="nav-link px-2 text-muted"))
            ], className="nav justify-content-center border-bottom pb-3 mb-3"),
            html.P("© 2023 FilmaGraph, Inc", className="text-center text-muted")
        ], className="py-3 my-4")
    ])
])


@app.callback(
    Output('selected-graph', 'figure'),
    Input('graph-selector', 'value'),
    Input('year-input', 'value')
)
def update_graph(selected_value, selected_year):
    global year
    year = selected_year
    if selected_value == 'movie-popularity':
        return create_movie_popularity_chart(year)
    elif selected_value == 'movie-vote':
        return create_movie_vote_chart(year)
    elif selected_value == 'people-popularity':
        return create_people_popularity()
    elif selected_value == 'tv-popularity':
        return create_tv_popularity(year)

if __name__ == '__main__':
    app.run_server(debug=True)