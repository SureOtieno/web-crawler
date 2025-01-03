from bs4 import BeautifulSoup
import requests
import pandas as pd

from dash import Dash, html, dcc, dash_table

app = Dash()


def get_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

everything = get_html("https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue")
first_table = everything.find_all('table')[0]
cols = first_table.find_all('th')

tb_cols = [col.text.strip() for col in cols]
table_columns = tb_cols[:9]
# table_columns=table_columns.pop()
# print(table_columns)

df = pd.DataFrame(columns=table_columns)
df.drop('Rank', axis=1, inplace=True)
# print(df)

rows = first_table.find_all('tr')[1:]

for row in rows[1:]:
    data = row.find_all('td')
    row_data = [td.text.strip() for td in data]
    length = len(df)
    df.loc[length] = row_data

df = df.drop(['Ref.', 'State-owned'], axis=1)
df = df.rename(columns = {'Ram': 'Company_Name', 'Headquarters[note 1]': 'Headquarters'})

# print(df['State-owned'])

app.layout = [html.Div(html.H1("Largest Companies by Revenue"),
                       style={'textAlign': 'center', 'color':'#1a1a1a'},
                       ),
                       html.Div(dash_table.DataTable(data=df.to_dict('records'), page_size=10), style={'textAlign': 'left'}),]


if __name__ == "__main__":
    app.run(debug=True)