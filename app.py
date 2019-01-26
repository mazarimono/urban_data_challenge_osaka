import dash   
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
import pandas as pd 
import os  

# CSS 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# DATA AREA
## 概要に使う自動車、バス、地下鉄データ
dfcar_allarea = pd.read_csv('./data/car_all_all.csv', index_col=0)
dfbus = pd.read_csv('./data/bus_data.csv', index_col=0)
dfsubway = pd.read_csv('./data/sub_data.csv', index_col=0)

dfgaiyo = pd.concat([dfcar_allarea['自動車総数'], dfsubway['総数（人）'], dfbus['総数（人）']], axis=1)
dfgaiyo.columns = ['自動車（台数）', '地下鉄（人）', 'バス（人）']
dfgaiyo1 = dfgaiyo / dfgaiyo.iloc[0, :] * 100 # 交通手段の標準化
dfgaiyo2 = dfgaiyo.copy()
dfgaiyo2['年度'] = dfgaiyo.index
dfgaiyo2 = dfgaiyo2[['年度', '自動車（台数）', '地下鉄（人）', 'バス（人）']]

## 人口データの加工
dfpop = pd.read_csv('./data/yearend_pop.csv', index_col=0)
dfpop = dfpop.iloc[:, :-2]
dfpop1 = pd.read_csv('./data/yearend_pop_for3.csv', index_col=0)
dfpop1 = dfpop1[['area', 'total', 'year']]

dfpop_nonosakacity = dfpop[dfpop['area'] != '大阪市'] # 大阪市なしの人口データ

dfarea_pop = pd.read_csv('./data/area_popdata.csv', index_col=0)
dfarea_sta = dfarea_pop / dfarea_pop.iloc[0, :] * 100
dfarea_sta = dfarea_sta.round(2)
dfarea_popdata = pd.concat([pd.DataFrame(dfarea_pop.iloc[-1, :]), pd.DataFrame(dfarea_sta.iloc[-1, :])], axis=1)
dfarea_popdata.columns = ['人口', '指数']
dfarea_popdata['地域'] = dfarea_popdata.index 
dfarea_popdata = dfarea_popdata[['地域', '人口', '指数']]
dfarea_popdata = dfarea_popdata.sort_values('指数', ascending=False)
dfarea_popdata = dfarea_popdata.round(2)

# 家計データ
dfhouse = pd.read_csv('./data/area_householddata.csv', index_col=0)
dfhouse_osaka = pd.DataFrame(dfhouse['大阪市'])
dfhouse_exosaka = dfhouse.drop('大阪市', axis=1)

dfhouse_sta = dfhouse / dfhouse.iloc[0, :] * 100  #家計データ標準化
dfhouse_sta = dfhouse_sta.round(2)
dfhouse_sta_osaka = dfhouse_sta['大阪市']
dfhouse_sta_exosaka = dfhouse_sta.drop('大阪市', axis=1)

# 自動車データの加工
dfcar_allarea2 = pd.concat([dfcar_allarea.iloc[:, 3:5], dfcar_allarea.iloc[:, 6:]], axis=1)
dfcar_allarea1 = dfcar_allarea / dfcar_allarea.iloc[0, :] * 100
dfcar_allarea3 = pd.concat([pd.DataFrame(dfcar_allarea.iloc[-1, :]), pd.DataFrame(dfcar_allarea1.iloc[-1, :])], axis=1)
dfcar_allarea3.columns = ['台数', '指数']
dfcar_allarea3['車種'] = dfcar_allarea3.index
dfcar_allarea3 = dfcar_allarea3[['車種', '台数', '指数']]
dfcar_allarea3 = dfcar_allarea3.sort_values('指数', ascending=False)
dfcar_allarea3 = dfcar_allarea3.round(2)

# 渋滞データ
dftraffic = pd.read_csv('./data/zyutai.csv', index_col=0)

# 地域自動車エリアデータ
dfareacar = pd.read_csv('./data/cardata_long.csv', index_col=0)
dfcar1 = dfareacar.copy()

# 公共交通データの加工
dfsubway = pd.read_csv('./data/sub_data.csv', index_col=0)
dfshitetsu = pd.read_csv('./data/shitetsu_yearly.csv', index_col=0)
dfshitetsu.columns = ['total', '定期（人）', '定期外（人）', 'year']
dfnewt = pd.read_csv('./data/newt_data.csv', index_col=0)
dfjr = pd.read_csv('./data/jr_yearly.csv', index_col=0)
dfjr.columns = ['total', '定期（人）', '定期外（人）', 'year']
dfbus = pd.read_csv('./data/bus_data.csv', index_col=0)

# 税金データの加工
dftax = pd.read_csv('./data/sizei_data_separate.csv', index_col=0)
dftax1 = dftax[dftax['name'] == 'total']

# 事業データ
dfzigyodata = pd.read_csv('./data/zigyo_data_spread.csv', index_col=0)
df1zigyodata = dfzigyodata[dfzigyodata['area'] != '総数']

# 高齢化データ
dfelder = pd.read_csv('./data/areage.csv', index_col=0)
dfelder1 = dfelder[['area', '65-(%)','year']]
dfspread = pd.read_csv('./data/age-spread.csv', index_col=0)
dfellabor = pd.read_csv('./data/agepoplabor.csv', index_col=0)

# TAB CSS AREA

tabs_styles = {
    'height': '55px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# color select
titlecolor = '#0cff00'

# APP AREA

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
            dcc.Tabs(id='tabs', style=tabs_styles, children=[
                # 背景をすべて画像にしてしまってタイトルページにするのが良いかな？
                dcc.Tab(label='タイトル / 目次', style=tab_style, selected_style = tab_selected_style, 
                children=[
                    html.Div([
                        html.Div([
                        html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                        ),
                        html.Div(style = {'backgroundColor': titlecolor,'height': '20px'}),
                        html.Div([
                        html.H1('大阪市の交通手段、人口動向の変化を見る'),
                        ],
                        style={'backgroundColor': titlecolor,'textAlign': 'center'}),
                        html.Div([
                            html.Div([
                            html.H4('概要'),], style={'backgroundColor': titlecolor}),
                            html.H5('・大阪市の交通手段、人口動向の変化を見るアプリです。'),
                            html.H5('・画面上にあるタブをクリックするとそのページに移ります。'),
                            html.H5('・チャート横の凡例をクリックするとその要素が消えます。もう一度クリックすると再び現れます。'),
                            html.H5('・データからみると、自動車台数の原因は、人々の移動手段の変化を表しているわけではなさそうです。'),
                            html.H5('・その要因を探るため、人口動向、雇用動向などを探りました。'),
                            html.H5('・データを沢山入れる事により、見る人々が自分で現状を考えられるアプリを目指しました。'),
                            ], style = {'marginBottom': '2%', 'textAlign': 'left', 'marginLeft': '10%'}),
                        html.Div([
                            html.Div([
                            html.H4('ページ概要'),], style={'backgroundColor': titlecolor}),
                            html.H5('・交通手段の変化概要: 大阪市の自動車台数、地下鉄、バスの利用概況を確認します。'),
                            html.H5('・大阪市の人口変動: 大阪市全体の人口、区別の人口を調査します。'),
                            html.H5('・自動車データ: 大阪市の自動車データの詳細を見ます。渋滞データも掲載しました。'),
                            html.H5('・区別自動車台数 / インタラクティブ: 区別の車種データがインタラクティブに見られます。'),
                            html.H5('・人口と収入と自動車台数: 区別の3つの指標の関連を見ました。収入は個人市民税を利用しました。'),
                            html.H5('・公共交通機関データ: 地下鉄、ニュートラム、市バス、私鉄、JRの利用状況を見ました。'),
                            html.H5('・民間事業所・雇用: 区別の事業所、従業員数の増減をインタラクティブに見れるチャートを作成しました。'),
                            html.H5('・高齢化: 区別の高齢化割合の変化、高齢化と人口減少、雇用の関係を調べました。'),
                        ], style = {'textAlign': 'left', 'marginLeft': '10%'}),
                        html.Div([
                            html.Div([
                            html.H4('利用データ'),], style={'backgroundColor': titlecolor}),
                            html.H5('・利用データに関してはgithubを参照ください。'),
                        ], style = {'textAlign': 'left', 'marginLeft': '10%'}),
                        ], style={'textAlign': 'center'}),
                        html.Div([
                        html.H3('アーバンデータチャレンジ2018　応募作品　'),
                        html.H3('合同会社長目　小川　英幸'),
                        ], style={'backgroundColor': titlecolor, 'textAlign': 'center', 'Color': 'white'}),
                    
                ]),]),
                dcc.Tab(label='交通手段の変化概況', style=tab_style, selected_style=tab_selected_style,
                children=[
                    html.Div([
                        html.Div([
                            html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                        ),
                            html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                        html.Div([
                            html.H1('大阪市の交通手段の変化概況(1997-2016)')
                        ], ),
                        html.Div([
                            html.P('・自動車は市内の保有台数。地下鉄、バスは一日の乗車人数の平均人数。'),
                            html.P('・全体的に低下傾向にある。バスの利用の減少が目立つ。'),
                            
                        ], ),
                        ], style={'textAlign': 'center','backgroundColor': titlecolor}),
                        html.Div([
                            dash_table.DataTable(
                                id='osaka_gaiyo_table',
                                columns = [
                                    {'name': i, 'id': i} for i in dfgaiyo2.columns
                                ],
                                data = dfgaiyo2.to_dict('rows'),
                                style_cell_conditional=[
                                    {'if': {'column_id': '年度'}, 'width': '3%', 'textAlign': 'center'},
                                    {'if': {'column_id': '自動車（台数）'}, 'width': '3%', 'textAlign': 'center'},
                                    {'if': {'column_id': '地下鉄（人）'}, 'width': '3%', 'textAlign': 'center'},
                                    {'if': {'column_id': 'バス（人）'}, 'width': '3%', 'textAlign': 'center'},
                                ]
                            ),
                        ], style={'width': '25%', 'display': 'inline-block'}),
                        html.Div([
                            dcc.Graph(
                                id='osaka_gaiyo_graph',
                                figure={
                                    'data':[
                                        go.Scatter(
                                        x = dfgaiyo1[i].index,
                                        y = dfgaiyo1[i],
                                        name = i) for i in dfgaiyo1.columns
                                    ],
                                    'layout': go.Layout(
                                        title = '交通手段利用の変化（1997年度：100）',
                                        height = 500
                                    )
                                }
                            ),
                            html.Div([
                                html.Div([
                                    html.H4('概観'),
                                    html.H5('・長期的には、全体的に利用は減少傾向にある。'),
                                    html.H5('・大阪市の人口はどうなっているのか？？'),],
                                    style={'marginLeft': '3%'}
                                )
                            ])
                        ], style={'height': '100%', 'width':'70%', 'float': 'right', 'display': 'inline-block'})
                ]
                )]),
                dcc.Tab(label='大阪市の人口変動', style=tab_style, selected_style=tab_selected_style,
                        children=[
                            html.Div([
                                html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                                ),
                                html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                                html.Div([
                                    html.H1('大阪市の人口変動(1997-2016)'),
                                    html.P('・大阪市全体の人口は約20年で4％弱伸びている。世帯数は同期間で22％弱の伸び。'),
                                    html.P('・人口が伸びているのは中央区、西区、北区、浪速区。減少は西成区、大正区、生野区、住之江区。(減少11区)'),
                                    html.P('・世帯数で見ると伸びているところは似ているが、減少地域が異なる。生野区、住之江区は世帯数で見ると増加している。（減少4区）'),
                                ], style={'textAlign': 'center','backgroundColor': titlecolor}),
                                html.Div([
                                dcc.Graph(
                                    id = 'osaka_pop_graph',
                                    figure={
                                        'data':[
                                            go.Scatter(
                                            x = dfpop[dfpop['area']=='大阪市']['date'],
                                            y = dfpop[dfpop['area']=='大阪市']['total'],
                                            name = '大阪市',
                                            stackgroup='one')
                                        ],
                                        'layout':
                                            go.Layout(
                                               title = '大阪市内の人口推移' ,
                                               height =500,
                                               width = 700,
                                            )
                                    }
                                )], style={'width': '35%', 'display': 'inline-block'}),
                                html.Div([
                                dcc.Graph(
                                    id='kubetsu_stackpop_graph',
                                    figure={
                                        'data':[
                                        go.Scatter(
                                            y = dfpop_nonosakacity[dfpop_nonosakacity['area']==i]['total'],
                                            x = dfpop_nonosakacity[dfpop_nonosakacity['area']==i]['date'],
                                            name = i,
                                            stackgroup='one',
                                        ) for i in dfpop_nonosakacity['area'].unique()
                                        ],
                                        'layout':
                                        go.Layout(
                                            title ='大阪市内区別人口推移',
                                            height = 500,
                                        )
                                    }
                                )], style={'height': '100%', 'width':'65%', 'float': 'right', 'display': 'inline-block', 'testAlign': 'center'}),
                                html.Div([
                                    html.Div([
                                        html.H3('区域別の人口推移を指数化して表示する（1997年度: 100）')
                                    ], style={'backgroundColor': titlecolor,'textAlign': 'center'}),
                                    html.Div([
                                        html.H6('2016年度の人口'),
                                        dash_table.DataTable(
                                            id = 'area_pop_table',
                                            columns = [{'name': i, 'id': i} for i in dfarea_popdata.columns],
                                            data = dfarea_popdata.to_dict('rows'),
                                            style_cell = {'textAlign': 'center'},
                                            style_cell_conditional =[
                                                {'if': {'column_id': '地域', 'width': '3%'}},
                                                {'if': {'column_id': '人口', 'width': '3%'}},
                                                {'if': {'column_id': '指数', 'width': '3%'}}
                                            ],
                                            style_table={'maxHeight': 500,  'overflowY': 'scroll'}
                                        )
                                    ], style={'width': '15%', 'display': 'inline-block'}),
                                    html.Div([
                                    dcc.Graph(
                                        id='osaka_area_pop',
                                        figure ={
                                            'data':[
                                                go.Scatter(
                                                    x = dfarea_sta.index,
                                                    y = dfarea_sta[i],
                                                    name = i, 
                                            ) for i in dfarea_sta.columns],
                                            'layout':go.Layout(
                                                height=500,
                                                title = '地域別人口の推移（指数）'
                                            )
                                        }
                                    ),
                                    html.Div([
                                        html.H5('・大阪市全体では人口は増加傾向にある。'),
                                        html.H5('・区域別に見ると増減の差が大きい。'),
                                    ], style={'marginLeft': '3%'})], style={'width': '80%', 'float': 'right', 'display': 'inline-block'})
                                ]),
                                html.Div([
                                    html.Div([
                                        html.H3('大阪市の世帯数データ')
                                    ], style = {'backgroundColor': titlecolor, 'textAlign': 'center', 'marginTop': '4%'}),
                                ]),
                                html.Div([
                                    html.Div([
                                        dcc.Graph(
                                            id = 'osaka-household',
                                            figure = {
                                                'data':[
                                                go.Scatter(
                                                    x = dfhouse.index, 
                                                    y = dfhouse['大阪市'],
                                                    name = '大阪市',
                                                    stackgroup='one'
                                                )],
                                                'layout':go.Layout(
                                                    height = 350,
                                                    title = '大阪市の世帯数',
                                                )
                                            }
                                        ),
                                        dcc.Graph(
                                            id = 'osaka-household-and-popu',
                                            figure = {
                                                'data':[
                                                    {'x': dfhouse_sta_osaka.index, 
                                                         'y': dfhouse_sta_osaka,
                                                         'name':'世帯数',
                                                         'type': 'line'
                                                        },
                                                    {'x': dfhouse_sta_osaka.index, 
                                                        'y': dfarea_sta['大阪市'],
                                                        'name': '人口',
                                                        'type': 'line'
                                                    }    
                                                        ],
                                                'layout':go.Layout(
                                                    height= 350,
                                                    title = '人口と世帯数（指数 1997年:100）'
                                                )
                                            }
                                        )
                                    ], style = {'width': '30%', 'display': 'inline-float', 'float':'left'}),
                                html.Div([
                                    dcc.Graph(
                                        id = 'area-household-stand',
                                        figure = {
                                            'data':[
                                            go.Scatter(
                                                x = dfhouse_sta_exosaka.index, 
                                                y = dfhouse_sta_exosaka[i], 
                                                name = i, 

                                            )for i in dfhouse_sta_exosaka.columns],
                                            'layout':
                                            go.Layout(
                                                height = 600,
                                                title = '地域別世帯数の推移（指数）'
                                            )
                                        }
                                    ),
                                    html.Div([
                                        html.H4('概観'),
                                        html.H5('・人口は微増（20年で+4%）。世帯数は増加（20年で+21%）。少子化。'),
                                        html.H5('・人口減少地域も、世帯数はそれほど減少していない。')
                                    ])
                                ], style = {'width': '65%', 'float': 'right', 'display': 'inline-float'})
                                ])
                            ])
                        ]),
                dcc.Tab(label='自動車データ', style=tab_style, selected_style=tab_selected_style,
                        children = [
                            html.Div([
                                html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                                ),
                                html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                                html.Div([
                                    html.H1('大阪市の自動車データ'),
                                    html.P('・自動車全体で見ると91.3万台から84.5万台へと7.4％減少している。'),
                                    html.P('・減少は貨物車、特殊用途者など、商用に使われるものが目立つ。一方で、一般に利用される軽自動車、普通乗用車は増加傾向にある。'),
                                    html.P('・渋滞時間の減少は商用車の減少が一因だろう。'),
                                ], style={'backgroundColor': titlecolor, 'textAlign': 'center'}),
                                html.Div([
                                    html.Div([
                                    dcc.Graph(
                                        id='car_by_kind',
                                        figure = {
                                            'data':[
                                                go.Scatter(
                                                    x = dfcar_allarea2[i].index,
                                                    y = dfcar_allarea2[i],
                                                    name = i, 
                                                    stackgroup='one'  
                                                ) for i in dfcar_allarea2.columns
                                            ],
                                            'layout':
                                                go.Layout(
                                                    title = '大阪市の自動車台数（種類別）'
                                                )
                                        }
                                    )
                                    ], style = {'width': '65%', 'display': 'inline-block', 'float': 'left'}),
                                    html.Div([
                                    dcc.Graph(
                                        id = 'traffic-jam',
                                        figure = {
                                            'data': [
                                                go.Scatter(
                                                    x = dftraffic.index,
                                                    y = dftraffic['平  均'],

                                                )
                                            ],
                                            'layout':
                                            go.Layout(
                                                title = '大阪市の渋滞（年間平均時間）'
                                            )
                                        }
                                    )
                                    ], style = {'width': '35%', 'display': 'inline-block', 'float': 'right'}),
                                ]),
                                html.Div([
                                    html.Div([
                                        dash_table.DataTable(
                                            id='car_table',
                                            columns = [{'name': i, 'id': i} for i in dfcar_allarea3.columns],
                                            data = dfcar_allarea3.to_dict('rows'),
                                            style_cell_conditional = [
                                                {'if': {'column_id': '車種'}, 'width': '3%', 'textAlign': 'center'},
                                                {'if': {'column_id': '台数'}, 'width': '3%', 'textAlign': 'center'},
                                                {'if': {'column_id': '指数'}, 'width': '3%', 'textAlign': 'center'},
                                            ]
                                        )
                                    ], style={'width': '25%', 'display': 'inline-block'}),
                                    html.Div([
                                    dcc.Graph(
                                        id='car_by_kind_standard',
                                        figure = {
                                            'data':[
                                                go.Scatter(
                                                    x = dfcar_allarea1[i].index,
                                                    y = dfcar_allarea1[i],
                                                    name = i, 
                                                ) for i in dfcar_allarea1.columns
                                            ],
                                            'layout':
                                                go.Layout(
                                                    title = '大阪市の自動車台数（種類別）'
                                                )
                                        }
                                    ),
                                    html.Div([
                                        html.Div([
                                        html.H4('衝撃の事実！'),], style={'backgroundColor': titlecolor}),
                                        html.H5('・普通乗用車の台数は増加している！'),
                                        html.H5('・商用に利用される自動車が減少している！')
                                    ], style = {'marginLeft': '5%'})], style={'width': '75%', 'display': 'inline-block', 'float': 'right'})
                                ])
                            ])
                        ]
                ),
                dcc.Tab(label='区別自動車台数', style=tab_style, selected_style=tab_selected_style,
                    children = [
                        html.Div([
                            html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                            ),
                            html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                            html.Div([
                                html.H1('大阪市の区別自動車台数'),
                                html.P('使い方　右側のドロップダウンで地域が、左側のドロップダウンで車種が選択可能。地域は複数選択可能。')
                            ], style={'textAlign': 'center', 'backgroundColor': titlecolor}),
                            html.Div([
                                dcc.Dropdown(
                                    id = 'area-dropdown',
                                    options = [{'label': i, 'value': i} for i in dfareacar['area'].unique()],
                                    value = '中央',
                                    multi = True,
                                )
                            ], style = {'width': '49%', 'display': 'inline-block', 'float': 'left'}),
                            html.Div([
                                dcc.Dropdown(
                                    id = 'kind-dropdown',
                                    options = [{'label': i, 'value': i} for i in dfareacar['車種'].unique()],
                                    value = '普通乗用車',
                                )
                            ], style = {'width': '49%', 'display': 'inline-block', 'float': 'right'}),
                        ]),
                        html.Div([
                            dcc.Graph(id = 'area-dropdown-graph')
                        ], style = {'width': '100%', 'display': 'inline-block'})
                    ]
                ),
                dcc.Tab(
                    label='人口と収入と自動車', style=tab_style, selected_style=tab_selected_style,
                    children = [
                        html.Div([
                            html.Div([
                            html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                            ),
                            html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                            html.Div([
                                html.Div([
                                    html.H1('人口と収入と自動車台数'),
                                    html.P('・人口と自動車台数、収入の関係。収入のデータが見つからず、個人市民税を利用した。'),
                                    html.P('・ボックスで車種が選択でき、グラフの下のスライダーでグラフに表示する年度が選択できる。'),
                                    html.P('・グラフの円の大きさが税金の金額を表している。グラフの円にマウスカーソルを合わせると、右側でヒストリカルグラフがその地域のものとなる。'),
                                ], style={'textAlign': 'center', 'backgroundColor': titlecolor})
                            ]),

                        ]),
                        html.Div([
                            html.Div([
                                dcc.Dropdown(
                                    id = 'syasyu-dropdown',
                                    options = [{'label': i, 'value': i} for i in dfcar1['車種']. unique()],
                                    value = '自動車総数'
                                ),
                                dcc.Graph(
                                    id = 'tax-main-chart',
                                    hoverData={'points': [{'customdata': '中央'}]}
                                ),
                                dcc.Slider(
                                    id = 'tax-year-slider',
                                    min = dftax1['year'].min(),
                                    max = dftax1['year'].max(),
                                    value = dftax1['year'].min(),
                                    marks = {str(year): str(year) for year in dftax1['year'].unique()}
                                )
                            ], style = {'width': '59%', 'display': 'inline-block', 'float': 'left', 'marginLeft': '1%'}),
                        html.Div([
                            dcc.Graph(id = 'hover-popu-chart'),
                            dcc.Graph(id = 'hover-car-chart'),
                            dcc.Graph(id = 'hover-tax-chart')
                        ], style = {'width': '39%', 'display': 'inline-block', 'float': 'right', 'marginTop': '5%'})
                        ],)
                        ])
                    ]
                ),

                dcc.Tab(label='公共交通機関データ', style=tab_style, selected_style=tab_selected_style,
                    children = [
                    html.Div([
                        html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                        ),
                        html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                        html.Div([
                            html.H1('公共交通機関データ'),
                            html.P('・電車はインバウンドの影響もあり、回復傾向にある。'),
                            html.P('・興味深いのは定期の減少です。2008年以前もなだらかに利用が減少していた。それ以降急激に減少している。これはマイスタイルの導入の影響によるものとみられる。'),
                            html.P('・マイスタイルは一月の定期代を超えると、その代金に上限が抑えられるサービスで、2008年3月に導入された。バス利用の一時的な増加もこの影響かもしれない。')
                        ], style={'textAlign': 'center', 'backgroundColor': titlecolor})
                    ]),
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id = 'subway-pop',
                                figure = {
                                    'data': [
                                        go.Scatter(
                                            x = dfsubway.index,
                                            y = dfsubway[i],
                                            name = i,
                                            stackgroup = 'one',

                                        ) for i in dfsubway.columns[:2]
                                    ],
                                    'layout':
                                        go.Layout(
                                            title='大阪地下鉄の利用者（1日平均：定期、定期外）'
                                        )
                                }
                            )
                        ], style = {'width': '49%', 'display': 'inline-block', 'float': 'left'}),
                        html.Div([
                            dcc.Graph(
                                id = 'subway-sells',
                                figure = {
                                    'data': [
                                        go.Scatter(
                                            x = dfsubway.index,
                                            y = dfsubway[i],
                                            name = i,
                                            stackgroup = 'one'
                                        ) for i in dfsubway.columns[-3: -1]
                                    ],
                                    'layout':
                                    go.Layout(
                                        title = '大阪地下鉄の収入（1日平均：定期、定期外）'
                                    )
                                }
                            )
                        ], style = {'width': '49%', 'display': 'inline-block', 'float':'right'})
                    ]),
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id = 'newt-pop',
                                figure = {
                                    'data':[
                                        go.Scatter(
                                            x = dfnewt.index,   
                                            y = dfnewt[i], 
                                            name = i,
                                            stackgroup='one'
                                        ) for i in dfnewt.columns[:2]
                                    ],
                                    'layout':
                                    go.Layout(
                                        title = '大阪市のニュートラムの利用者数（1日平均：定期、定期外）'
                                    )
                                }
                            )
                        ], style = {'width': '49%', 'display': 'inline-block', 'float': 'left'}),
                        html.Div([
                            dcc.Graph(
                                id = 'newt-sells',
                                figure = {
                                    'data':[
                                        go.Scatter(
                                            x = dfnewt.index,  
                                            y = dfnewt[i],   
                                            name = i,   
                                            stackgroup= 'one'
                                        ) for i in dfnewt.columns[-3: -1]
                                    ],
                                    'layout':
                                    go.Layout(
                                        title = '大阪市のニュートラムの収入（1日平均：定期、定期外）'
                                    )
                                }
                            )
                        ], style = {'width': '49%', 'display': 'inline-block', 'flaot': 'right'})
                    ]),
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id = 'bus-pop',
                                figure = {
                                    'data': [
                                    go.Scatter(
                                        x = dfbus.index,   
                                        y = dfbus[i],
                                        name = i,
                                        stackgroup= 'one'
                                    ) for i in dfbus.columns[:2]
                                ],
                                    'layout':
                                    go.Layout(
                                        title='大阪市のバスの利用者数'
                                    )
                                }
                            )
                        ], style = {'width': '32%', 'display': 'inline-block', 'float': 'left', 'marginLeft': '2%'}),
                        html.Div([
                            dcc.Graph(
                                id = 'shitetsu',
                                figure = {
                                    'data': [
                                        go.Scatter(
                                            x = dfshitetsu['year'],  
                                            y = dfshitetsu[i],  
                                            name = i,   
                                            stackgroup='one'
                                        ) for i in dfshitetsu.columns[1:-1]
                                    ],
                                    'layout':
                                    go.Layout(
                                        title = '大阪私鉄の利用者数'
                                    )
                                }
                            )
                        ], style = {'width': '32%', 'display': 'inline-block', 'float': 'center'}),
                        html.Div([
                            dcc.Graph(
                                id = 'jr',
                                figure = {
                                    'data': [
                                        go.Scatter(
                                            x = dfjr['year'],
                                            y = dfjr[i],
                                            name = i,
                                            stackgroup='one'
                                        ) for i in dfjr.columns[1:-1]
                                    ],
                                    'layout':
                                    go.Layout(
                                        title = '大阪のJRの利用者数'
                                    )
                                }
                            )
                        ], style = {'width': '32%', 'display': 'inline-block', 'flaot': 'right'})
                    ])
                    ]),
                    dcc.Tab(label='民間事業所・雇用', style=tab_style, selected_style=tab_selected_style,
                        children = [
                        html.Div([
                            html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                            ),
                            html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                            html.H1('民間事業所'),
                            html.P('・区別の民間事業所、雇用の変化を見る。'),
                            html.P('・多くの地域で事業所、雇用ともに減少している。')
                        ], style={'textAlign': 'center', 'backgroundColor': titlecolor}),
                        html.Div([
                    html.Div([
                        html.H3('大阪市内の事務所と従業員数の変化（2009年=>2015年）'),
                    ], style = {'textAlign': 'center', 'backgroundColor': titlecolor}),
                    html.Div([
                        dcc.Dropdown(
                            id = 'select_c_or_e',
                            options = [{'label': i, 'value': i} for i in df1zigyodata['type'].unique()],
                            value = '事業所'
                        )], style={'width': '30%', 'position': 'center'}),
                    html.Div([
                        dcc.RadioItems(
                            id = 'select_p_or_i',
                            options = [
                                {'label': 'spread', 'value': 'spread'},
                                {'label': 'spread%', 'value': 'spread%'}
                                ],
                            value = 'spread'
                        )],),
                        ],),
                            html.Div([
                            dcc.Graph(id = 'tells_about_labor')
                                ], style= {'marginLeft': '2%', 'marginRight': '2%'})
                            ]),
                dcc.Tab(label='高齢化', style=tab_style, selected_style=tab_selected_style,
                    children =[
                        html.Div([
                        html.Div(
                            style = {'height': '40px','width': 'auto', 'backgroundImage': 'url(https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190123/20190123093340.png)'}
                            ),
                            html.Div([], style={'height': '20px', 'backgroundColor': titlecolor}),
                            html.H1('高齢化'),
                            html.P('・雇用の減少、人口減少などは高齢化が影響しているのか見てみた。'),
                            html.P('・多くの地域で事業所、雇用ともに減少している。')
                        ], style={'textAlign': 'center', 'backgroundColor': titlecolor}),
                        html.Div([
                            html.H3('各区の人口に占める65歳以上の年齢の割合'),
                            html.P('・大阪市は14％＝＞25％。ちなみに全国平均は27.7％（2017年）。')
                        ], style={'textAlign': 'center', 'backgroundColor': titlecolor}),
                        html.Div([
                            dcc.Graph(
                                id = 'elder-ratio-chart',
                                figure = {
                                    'data': [
                                        go.Scatter(
                                            x = dfelder1[dfelder1['area']==i]['year'],
                                            y = dfelder1[dfelder1['area']==i]['65-(%)'],
                                            name = i,
                                            mode = 'lines+markers',
                                        ) for i in dfelder1['area'].unique()
                                    ],
                                    'layout':
                                        go.Layout(
                                            height = 500,
                                            xaxis = {'title': '65歳以上の割合（％）'},
                                            yaxis = {'title': '年度'}
                                        )
                                }
                            )
                        ], style = {'marginLeft': '10%', 'marginRight': '10%'}),
                        html.Div([
                            html.H3('人口の増減と高齢化の関係を見る')
                        ], style={'textAlign': 'center', 'backgroundColor': titlecolor}),
                        html.Div([
                            dcc.Graph(
                                id = 'ratio-corr',
                                figure ={
                                    'data':[
                                        go.Scatter(
                                            x = dfspread[dfspread['area'] == i]['人口増加率'],
                                            y = dfspread[dfspread['area'] == i]['高齢者割合増加率'],
                                            name = i,
                                            mode = 'markers',
                                            marker ={
                                                'size': 15,
                                                'opacity': 0.5
                                            }
                                        ) for i in dfspread['area'].unique()
                                    ],
                                    'layout':
                                        go.Layout(
                                            height = 500,
                                            title = '人口と高齢者割合の変化（1995=>2015）',
                                            xaxis = {'title' : '人口の増加率(%)'},
                                            yaxis = {'title' : '高齢者割合増加率(%)'}
                                        )
                                }
                            )
                        ], style = {'marginLeft': '10%', 'marginRight': '10%'}),
                        html.Div([
                            html.H3('区別の雇用者数と高齢化の関係')
                        ], style={'textAlign': 'center', 'backgroundColor': titlecolor}),
                        html.Div([
                            dcc.Graph(
                                id = 'labor-and-elder',
                                figure = {
                                    'data' : [
                                        go.Scatter(
                                            x = dfellabor[dfellabor['area'] == i]['高齢者割合増加率'],
                                            y = dfellabor[dfellabor['area'] == i]['従業員増減率'],
                                            name = i,
                                            mode = 'markers',
                                            marker = {
                                                'size': 15,
                                                'opacity': 0.5
                                            }
                                        ) for i in dfellabor['area'].unique()
                                    ],
                                    'layout':
                                    go.Layout(
                                        height = 500,
                                        title = '高齢者割合増加率と従業員数の増加率（高齢者割合増加率は1995＝＞2015、従業員増加率は2009＝＞2015）',
                                        xaxis = {'title': '高齢者割合増加率（％）'},
                                        yaxis = {'title': '従業員増減率（％）'}
                                    )
                                }
                            )
                        ], style = {'marginLeft': '10%', 'marginRight': '10%'}),
                        html.Div([
                            html.H3('区別の人口増加率と雇用者増加率の関係')
                        ], style={'textAlign': 'center', 'backgroundColor': titlecolor}),
                        html.Div([
                            dcc.Graph(
                                id = 'labor-and-pop',
                                figure = {
                                    'data':[
                                        go.Scatter(
                                            x = dfellabor[dfellabor['area'] == i]['人口増加率'],
                                            y = dfellabor[dfellabor['area'] == i]['従業員増減率'],
                                            name = i,
                                            mode = 'markers',
                                            marker = {
                                                'size': 15,
                                                'opacity': 0.5
                                            }
                                        ) for i in dfellabor['area'].unique()
                                    ],
                                    'layout':
                                        go.Layout(
                                            height= 500,
                                            title = '人口増加率と雇用者増加率の関係（人口：1995=>2015, 雇用: 2009=>2015)',
                                            xaxis = {'title': '人口増加率（％）'},
                                            yaxis = {'title': '雇用者数増加率（％）'}
                                        )
                                }
                            )
                        ], style = {'marginLeft': '10%', 'marginRight': '10%'}),
                    ]
                )

            ])
])

@app.callback(
    dash.dependencies.Output('area-dropdown-graph', 'figure'),
    [dash.dependencies.Input('area-dropdown', 'value'),
    dash.dependencies.Input('kind-dropdown', 'value')]
)
def make_chart(area, kind):

    area_list = list()
    area_list.append(area)
    try:
        area_list = sum(area_list, [])
    except:
        pass

    kind_list = list()
    kind_list.append(kind)
    try:
        kind_list = sum(kind_list, [])
    except:
        pass 

    area_df = pd.DataFrame()
    for i in area_list:
        df_a = dfareacar[dfareacar['area'] == i]
        area_df = pd.concat([area_df, df_a])
    
    car_df = pd.DataFrame()
    for i in kind_list:
        df_c = area_df[area_df['車種'] == i]
        car_df = pd.concat([car_df, df_c])

    return {
        'data':[
            go.Scatter(
                x = car_df[car_df['area'] == i]['year'],
                y = car_df[car_df['area'] == i]['台数'],
                name = i,

            ) for i in car_df['area'].unique()
        ],
        'layout':
            go.Layout(
                height= 550,
            )
    }

@app.callback(
    dash.dependencies.Output('tax-main-chart', 'figure'),
    [dash.dependencies.Input('tax-year-slider', 'value'),
    dash.dependencies.Input('syasyu-dropdown', 'value')]
)
def make_taxmainchart(selected_year, kind):
    dfpop2 = dfpop1[dfpop1['year'] == selected_year]
    dfcar2 = dfcar1[dfcar1['車種'] == kind]
    dfcar2 = dfcar2[dfcar2['year'] == selected_year]
    dftax2 = dftax1[dftax1['year'] == selected_year]

    return {
        'data': [
            go.Scatter(
                x = dfpop2[dfpop2['area'] == i]['total'],
                y = dfcar2[dfcar2['area'] == i]['台数'],
                name = i,
                mode = 'markers',
                marker = {
                    'size': dftax2[dftax2['area'] == i]['amount'] / dftax2['amount'].max() * 100,
                    'opacity': 0.6,
                    'colorscale': 'Jet',
                },
                customdata = [i],
            ) for i in dfcar2['area'].unique()
        ],
        'layout':
            go.Layout(
                height = 650
            )
    }

@app.callback(
    dash.dependencies.Output('hover-popu-chart', 'figure'),
    [dash.dependencies.Input('tax-main-chart', 'hoverData')]
)
def taxpop_graph(hoverData):
    areaname = hoverData['points'][0]['customdata']
    dfpop2 = dfpop1[dfpop1['area'] == areaname]
    return {
        'data': [go.Scatter(
                x = dfpop2['year'],
                y = dfpop2['total'],
                name = areaname,
                mode = 'lines + markers'

        )],
        'layout': go.Layout(
            height = 200,
            margin = {'l': 40, 'b': 20, 'r': 10, 't': 30},
            title = '<b>{}区の人口（(人)ヒストリカル）</b><br>'.format(areaname)
        )
    }

@app.callback(
    dash.dependencies.Output('hover-car-chart', 'figure'),
    [dash.dependencies.Input('tax-main-chart', 'hoverData'),
    dash.dependencies.Input('syasyu-dropdown', 'value')]
)
def taxcar_graph(hoverData, kind):
    areaname = hoverData['points'][0]['customdata']
    dfcar2 = dfcar1[dfcar1['車種'] == kind]
    dfcar2 = dfcar2[dfcar2['area'] == areaname]
    return {
        'data': [go.Scatter(
            x = dfcar2['year'],
            y = dfcar2['台数'],
            name = areaname,
            mode = 'lines + markers'
        )],
        'layout': go.Layout(
            height = 200,
            margin = {'l': 40, 'b': 20, 'r': 10, 't': 30},
            title = '<b>{}区の{}（(台)ヒストリカル）</b><br>'.format(areaname, kind)
        )
    }

@app.callback(
    dash.dependencies.Output('hover-tax-chart', 'figure'),
    [dash.dependencies.Input('tax-main-chart', 'hoverData')]
)
def taxtax_graph(hoverData):
    areaname = hoverData['points'][0]['customdata']
    dftax2 = dftax1[dftax1['area'] == areaname]
    return {
        'data': [go.Scatter(
            x = dftax2['year'],
            y = dftax2['amount'],
            name = areaname,
            mode = 'lines + markers'
        )],
        'layout': go.Layout(
            height = 200,
            margin = {'l': 40, 'b': 20, 'r': 10, 't': 30},
            title = '<b>{}区の個人市民税総額（（千円）ヒストリカル）</b><br>'.format(areaname)
        )
    }

@app.callback(
    dash.dependencies.Output('tells_about_labor', 'figure'),
    [dash.dependencies.Input('select_c_or_e', 'value'),
    dash.dependencies.Input('select_p_or_i', 'value')]
)
def make_chart(select_ce, select_pi):
    df2 = df1zigyodata[df1zigyodata['type'] == select_ce]
    df2 = df2[['area', 'amount', select_pi]]

    return {
        'data': [
            go.Scatter(
                x = df2[df2['area'] == i]['amount'],
                y = df2[df2['area'] == i][select_pi],
                name = i,
                mode = 'markers',
                marker = {
                    'size': 15,
                    'opacity': 0.5
                }
            ) for i in df2['area'].unique()
        ],
        'layout':
            go.Layout(
                height = 550,
                margin = {'l': 40, 'b': 20, 'r': 10, 't': 30},
                xaxis = {'title': '{}の数（2015年）'.format(select_ce), 
                'automargin': True},
                yaxis = {'title': '{}の増減（2009年==>2015年）'.format(select_ce),
                'automargin': True},
                hovermode = 'closest',
                title = '大阪市内の{}の数とその増減（2009年==>2015年）'.format(select_ce)
            )
    }



if __name__ == '__main__':
    app.run_server(debug=True)