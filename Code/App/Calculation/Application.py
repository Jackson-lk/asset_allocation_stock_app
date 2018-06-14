from flask import Flask, render_template, request
from sklearn.externals import joblib
import pandas as pd
import pickle

# Load file
df = pd.read_csv('../../../Dataset/stats_final_mean.csv')
# Create DataFrame
df_result = df.copy()
df_result['Result'] =""
df_result

app = Flask(__name__, static_url_path='/static/')


@app.route('/')
def form():
    return render_template('index.html')


@app.route('/predict_price', methods = ['POST', 'GET'])
def predict_price():

    # get the parameters
    Growth_of_Company = float(request.form['Growth_of_Company'])
    Value_of_Company = float(request.form['Value_of_Company'])
    PE_ratio = float(request.form['PE_ratio'])
    Return = float(request.form['Return'])
    Stock_Volatility = float(request.form['Stock_Volatility'])
    Stock_Volatility_to_Market = float(request.form['Stock_Volatility_to_Market'])

    # load the table and calculate
    for i in range(0, len(df.index)):
        df_result.loc[i, 'Revenue_Growth'] = (df.loc[i, 'Revenue_Growth'] * Growth_of_Company)
        df_result.loc[i, 'Enterprise_Value'] = (df.loc[i, 'Enterprise_Value'] * Value_of_Company)
        df_result.loc[i, 'Forward_P/E'] = (df.loc[i, 'Forward_P/E'] * PE_ratio)
        df_result.loc[i, 'Risk_Free_Return'] = (df.loc[i, 'Risk_Free_Return'] * Return)
        df_result.loc[i, 'Stock_Volatility'] = (df.loc[i, 'Stock_Volatility'] * Stock_Volatility * -1)
        df_result.loc[i, 'Beta'] = (df.loc[i, 'Beta'] * Stock_Volatility_to_Market * -1)
        df_result.loc[i, 'Result'] = (
                    df_result.loc[i, 'Revenue_Growth'] + df_result.loc[i, 'Enterprise_Value'] + df_result.loc[
                i, 'Forward_P/E'] + df_result.loc[i, 'Risk_Free_Return'] + df_result.loc[i, 'Stock_Volatility'] +
                    df_result.loc[i, 'Beta'])
    df_ticker = df_result.sort_values('Result', ascending=False).head(8)
    storage = list(df_ticker['Ticker'])
    return render_template('results.html',
                           Growth_of_Company=int(Growth_of_Company),
                           Value_of_Company=int(Value_of_Company),
                           PE_ratio=int(PE_ratio),
                           Return=int(Return),
                           Stock_Volatility=int(Stock_Volatility),
                           Stock_Volatility_to_Market = int(Stock_Volatility_to_Market),
                           # predicted_price="{:,}".format(list)
                           recommendation1 = storage[0],
                           recommendation2 = storage[1],
                           recommendation3 = storage[2],
                           recommendation4 = storage[3],
                           recommendation5 = storage[4],
                           recommendation6 = storage[5],
                           recommendation7 = storage[6],
                           recommendation8 = storage[7]

                           )

if __name__ == '__main__':
    app.run(debug=True)