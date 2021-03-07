# TODO adjusted close, divident amount ve split coefficient eklenecek
# simdilik random sayi var, algoritmaya (gamestonk terminal) etkisi var mi? 


#!/usr/bin/env python

import argparse
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from gamestonk_terminal.helper_funcs import (
    valid_date,
    check_positive,
    b_is_stock_market_open,
    plot_view_stock,
)
from gamestonk_terminal.fundamental_analysis import fa_menu as fam
from gamestonk_terminal.technical_analysis import ta_menu as tam
from gamestonk_terminal.due_diligence import dd_menu as ddm
from gamestonk_terminal.discovery import disc_menu as dm
from gamestonk_terminal.sentiment import sen_menu as sm
from gamestonk_terminal.prediction_techniques import pred_menu as pm
from gamestonk_terminal.papermill import papermill_menu as mill
from gamestonk_terminal import res_menu as rm
from gamestonk_terminal import config_terminal as cfg

# import warnings
# warnings.simplefilter("always")
## IMPORT OZGUn
import investpy

arg = None
ticker = 'GME'
interval = 1440
# ----------------------------------------------------- LOAD -----------------------------------------------------
def load(l_args, s_ticker, s_start, s_interval, df_stock):
    parser = argparse.ArgumentParser(
        prog="load", description=""" Load a stock in order to perform analysis"""
    )
    parser.add_argument(
        "-t",
        "--ticker",
        action="store",
        dest="s_ticker",
        required=True,
        help="Stock ticker",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=valid_date,
        dest="s_start_date",
        help="The starting date (format YYYY-MM-DD) of the stock",
    )
    parser.add_argument(
        "-i",
        "--interval",
        action="store",
        dest="n_interval",
        type=int,
        default=1440,
        choices=[1, 5, 15, 30, 60],
        help="Intraday stock minutes",
    )

    try:
        (ns_parser, l_unknown_args) = parser.parse_known_args(l_args)
    except SystemExit:
        print("")
        return [s_ticker, s_start, s_interval, df_stock]

    if l_unknown_args:
        print(f"The following args couldn't be interpreted: {l_unknown_args}")

    # Update values:
    s_ticker = ns_parser.s_ticker
    s_start = ns_parser.s_start_date
    s_interval = str(ns_parser.n_interval) + "min"

    try:
        ts = TimeSeries(key=cfg.API_KEY_ALPHAVANTAGE, output_format="pandas")
        # Daily
        if s_interval == "1440min":
            # pylint: disable=unbalanced-tuple-unpacking
            df_stock, _ = ts.get_daily_adjusted(
                symbol=ns_parser.s_ticker, outputsize="full"
            )
        # Intraday
        else:
            # pylint: disable=unbalanced-tuple-unpacking
            df_stock, _ = ts.get_intraday(
                symbol=ns_parser.s_ticker, outputsize="full", interval=s_interval
            )

        df_stock.sort_index(ascending=True, inplace=True)

    except Exception as e:
        print(e)
        print("Either the ticker or the API_KEY are invalids. Try again!")
        return [s_ticker, s_start, s_interval, df_stock]

    s_intraday = (f"Intraday {s_interval}", "Daily")[s_interval == "1440min"]

    if s_start:
        # Slice dataframe from the starting date YYYY-MM-DD selected
        df_stock = df_stock[ns_parser.s_start_date :]
        print(
            f"Loading {s_intraday} {s_ticker} stock with starting period {s_start.strftime('%Y-%m-%d')} for analysis."
        )
    else:
        print(f"Loading {s_intraday} {s_ticker} stock for analysis.")

    print("")
    return [s_ticker, s_start, s_interval, df_stock]

s_ticker = "GME"
s_start = ""
df_stock = pd.DataFrame()
s_interval = "1440min"

# Set stock by default to speed up testing
# s_ticker = "BB"
# ts = TimeSeries(key=cfg.API_KEY_ALPHAVANTAGE, output_format='pandas')
# df_stock, d_stock_metadata = ts.get_daily_adjusted(symbol=s_ticker, outputsize='full')
# df_stock.sort_index(ascending=True, inplace=True)
# s_start = datetime.strptime("2020-06-04", "%Y-%m-%d")
# df_stock = df_stock[s_start:]

# Add list of arguments that the main parser accepts
menu_parser = argparse.ArgumentParser(prog="gamestonk_terminal", add_help=False)
menu_parser.add_argument(
    "opt",
    choices=[
        "help",
        "quit",
        "q",
        "clear",
        "load",
        "view",
        "disc",
        "mill",
        "sen",
        "res",
        "fa",
        "ta",
        "dd",
        "pred",
    ],
)

# Print first welcome message and help
print("\nWelcome to Didier's Gamestonk Terminal\n")

# # # as_input = input("> ")
as_input = 'load -t GME'
# Parse main command of the list of possible commands
(ns_known_args, l_args) = menu_parser.parse_known_args(as_input.split())

elif (ns_known_args.opt == "quit") or (ns_known_args.opt == "q"):
    print("Hope you made money today. Good bye my lover, good bye my friend.\n")
    return

elif ns_known_args.opt == "clear":
    print("Clearing stock ticker to be used for analysis")
    s_ticker = ""
    s_start = ""

elif ns_known_args.opt == "load":
    [s_ticker, s_start, s_interval, df_stock] = load(
        l_args, s_ticker, s_start, s_interval, df_stock
    )

#    elif ns_known_args.opt == "view":
#       view(l_args, s_ticker, s_start, s_interval, df_stock)


ticker, start, interval, df = load(l_args, s_ticker, s_start, s_interval, df_stock)
df0 = df.iloc[0] # first row to see what alpha is doing.
df0.round(2)


# invest.py part

stock_name = 'COSMO'
data = investpy.get_stock_historical_data(
        stock = stock_name, country = 'turkey', 
        from_date = '01/02/2021', to_date =  '05/03/2021'
        )
# currency sutununa gerek yok
data.drop(columns='Currency', inplace=True)
# sutun isimlerini gamestonk ile ayni hale getir
data = data.rename(columns={
    'Open': '1. open',
    'High': '2. high',
    'Low': '3. low',
    'Close': '4. close',
    'Volume': '6. volume'
    })

# simdilik 5 7 ve 8i rastgele doldur. algoritmayi ekliyorsa, hesap yapmak lazim 
data.insert(loc = 4, column='5. adjusted close', value= 1.0)
data.insert(loc = 6, column='7. didivent amount', value= 0.0)
data.insert(loc = 7, column='8. split coefficient', value= 0.0)

