from flask import Flask, render_template,url_for
import pandas as pd
import json 
import plotly
import plotly.express as px
import plotly.graph_objects as go 


# from application import app

app = Flask(__name__)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/Analytics')
def Analytics():
    return render_template('Analytics.html')

@app.route('/')
def index():

    #graphs
    df = pd.read_csv('case_time_series.csv',parse_dates=['Date'])
    dff = pd.read_csv('state_wise.csv')


    dfff = pd.read_csv('state_wise_.csv')
    In_states = json.load(open("states_india.geojson","r"))

    state_id_map = {}
    for feature in In_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]


    dfff["id"] = dfff["State"].apply(lambda x: state_id_map[x])
    fig = px.choropleth_mapbox(
        data_frame=dfff,
        locations="id",
        geojson=In_states,
        color="Confirmed",
        hover_name="State",
        hover_data=["Confirmed","Active","Recovered","Deaths"],
        title="State wise confirmed cases ",
        # template='plotly_',
        mapbox_style="carto-positron",
        center={"lat": 24, "lon": 78},
        zoom=3,
        opacity=0.5,
    )
    fig.update_geos(fitbounds="locations", visible=False)


    # fig1 = px.line(data_frame=df,x='Date',y=['DC','DR','DD'], title='Covid cases India')
    fig1 = px.line(data_frame=df,x='Date' ,y=['DC','DR','DD'],title='Daily Cases India',)
    fig1.update_xaxes(rangeslider_visible=True)
    # fig.show()
    fig2 = px.bar(data_frame=dff,x='State' ,y=['CNF'],title='Statewise comparison')
    fig3 = px.line(data_frame=df,x='Date',y=['TC','TR','TD'],title='Cumulative covid cases',log_y=True)

    fig4 = px.line(data_frame=df,x='Date',y=['TC','TR','TD'],title='Cummilative Cases India')
    fig4.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
            ])
        )
    )
    fig5 = px.line_3d(data_frame=df,x='Date',y='DR',z='DD',title='Daily Cases India',log_y= True)
    fig6 = px.funnel(data_frame=df,x='Date',y='DC',title='Daily cases w.r.t. preceeding as day parameter')

    graph0JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    graph1JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    
    graph2JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

   
    graph3JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    graph6JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



    return render_template('whatever.html',title='India',graph0JSON = graph0JSON,graph1JSON = graph1JSON,graph2JSON=graph2JSON,graph3JSON=graph3JSON,graph4JSON = graph4JSON,graph5JSON = graph5JSON,graph6JSON = graph6JSON)
    # return render_template('horizontal.html')


if __name__ == "__main__":
    app.run(debug=True,port=8000)




# fig_4 = px.bar(data_frame=df,x='Date',y='DC',template='plotly_dark',title='Daily cases comparison on preceding day parameters')
    # fig_5 = px.funnel(data_frame=df,x='Date',y='DR',template='plotly_dark',title='Daily recovery comparison on preceding day parameters')
    # fig_6 = px.funnel(data_frame=df,x='Date',y='DD',template='plotly_dark',title='Daily death comparison on preceding day parameters')
    
 
    # df = px.data.medals_wide()
    # fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")

# Graph two
    # df = px.data.iris()
    # fig2 = px.scatter_
     # # Graph three
    # df = px.data.gapminder().query("continent=='Oceania'")
    # fig3 = px.line(df, x="year", y="lifeExp", color='country',  title="Life Expectancy")

 # # Graph three
    # df = px.data.gapminder().query("continent=='Oceania'")
    # fig3 = px.line(df, x="year", y="lifeExp", color='country',  title="Life Expectancy")