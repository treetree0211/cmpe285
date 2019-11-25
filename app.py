# coding=utf-8
from flask import Flask, render_template, request
from datetime import datetime
import pytz

from pip._vendor import requests

app = Flask(__name__)


@app.route('/')
def stock_display():
    return render_template('stock.html')


@app.route('/network')
def ticker_display():
    return render_template('main.html')


@app.route('/current_result', methods=['POST', 'GET'])
def current_result():
    if request.method == 'POST':
        ticker = request.form['Ticker Symbol']
        now = datetime.now(pytz.timezone('US/Pacific'))
        time = now.strftime("%m/%d/%Y, %H:%M:%S")
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-quotes"
        querystring = {"region": "US", "lang": "en", "symbols": ticker}
        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "x-rapidapi-key"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        result = data['quoteResponse']['result']

        if len(result) == 0:
            name = "Invalid Ticker"
            price = ""
            value_change = ""
            percent_change = ""
        else:
            name = result[0]['longName']
            price = '{:,.2f}'.format(result[0]['regularMarketPrice'])
            v_change = float(result[0]['regularMarketChange'])
            p_change = float(result[0]['regularMarketChangePercent'])

            if v_change > 0:
                value_change = "+" + '{:,.2f}'.format(v_change)
            else:
                value_change = '{:,.2f}'.format(v_change)

            if p_change > 0:
                percent_change = "+" + '{:,.2f}'.format(p_change) + "%"
            else:
                percent_change = '{:,.2f}'.format(p_change) + "%"

    return render_template('res.html', time=time, name=name, price=price, value_change=value_change,
                           percent_change=percent_change)


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        allotment = int(request.form['Allotment'])
        final_share_price = float(request.form['Final Share Price'])
        sell_commission = float(request.form['Sell Commission'])
        buy_commission = float(request.form['Buy Commission'])
        init_share_price = float(request.form['Initial Share Price'])
        tax = float(request.form['Capital Gain Tax Rate (%)'])

        proceed = "$" + '{:,.2f}'.format(allotment * final_share_price)
        difference = "$" + '{:,.2f}'.format(
            allotment * (final_share_price - init_share_price) - (sell_commission + buy_commission))

        capital_tax = (allotment * (final_share_price - init_share_price) - (sell_commission + buy_commission)) * (
            0.01) * tax

        purchase_price = allotment * init_share_price
        cost_num = capital_tax + purchase_price + sell_commission + buy_commission
        net_profit_num = allotment * final_share_price - cost_num
        return_investment_num = net_profit_num / cost_num * 100
        return_on_investment = '{:,.2f}'.format(return_investment_num) + "%"

        net_profit = "$" + '{:,.2f}'.format(net_profit_num)

        b_commission = "$" + '{:,.2f}'.format(buy_commission)
        s_commission = "$" + '{:,.2f}'.format(sell_commission)

        purchase_display = str(allotment) + " X " + "$" + '{:,.2f}'.format(purchase_price) + \
                           " = " + '{:,.2f}'.format(purchase_price)
        tax_display = str(tax) + "% of " + difference + " = $" + '{:,.2f}'.format(capital_tax)

        cost = "$" + '{:,.2f}'.format(cost_num)

        even_price_num = (purchase_price + sell_commission + buy_commission) / allotment
        even_price = "$" + '{:,.2f}'.format(even_price_num)

        return render_template("result.html", proceed=proceed, cost=cost, b_comission=b_commission,
                               s_comission=s_commission, purchase_display=purchase_display, tax_display=tax_display,
                               net_profit=net_profit, return_on_investment=return_on_investment, even_price=even_price)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
