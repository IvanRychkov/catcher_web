from flask import Flask, render_template
from catcher.buyer import Buyer
from catcher.tinkoff import TinkoffAPI
import os
import joblib

memory = joblib.Memory(location='cache')
memory.clear()
app = Flask('__main__')
# img_tmp = 'static/images/tmp'
img_tmp = 'tmp/images'


@app.route('/')
@memory.cache()
def main():
    return render_template('body.html',
                           image_name='msft',
                           instrument='Microsoft',
                           recommend=0.05)


@app.route('/<ticker>/')
def get_ticker_plot(ticker, commission=.005):
    # print('commission =', commission)
    api = TinkoffAPI(ticker=ticker)
    buyer = Buyer(api, broker_commission=commission, policy='lar')
    result = buyer.learn_buy_recommendation(verbose=True,
                                            save_chart=True,
                                            interval='15min',
                                            batches=30,
                                            profit_threshold=.5,
                                            cross_val=False)
    print(result)
    return '''<h1>Hello, biatch! </h1>
    <br>
    <p>Your buy recommendation for {ticker} is {buy:.3%}</p>
    
    <img src={img_src}>
    '''.format(img_src=os.path.join(img_tmp, ticker.lower() + '.png'),
               **result),


if __name__ == '__main__':

    os.makedirs('tmp/images', exist_ok=True)

    app.run(host='localhost', port='8080', debug=True, use_reloader=True)
