# NSE Data Reader
Python Library to get publicly available data on NSE website ie. stock quotes, historical data, live indices.

## Documentation:
Please see the Usage section below. Reference documentation can also be found [here](https://aksmtr.com/articles/18-the-powerful-python-package-to-read-india-stock-data-from-nse).

## Installation
Fresh installation 

```$pip install nse-data-reader```

Upgrade

```$pip install nse-data-reader --upgrade```

## Usage

Get the price history of stocks and NSE indices directly in pandas dataframe.

### NIFTY Index - EoD OHLC (candle) data
To get NIFTY data, you will need to set the `index` parameter to `true`. 
```python
from datetime import date
from nsepy import get_history

# get all the data of NIFTY index from 01 Feb 2023 to 10 Feb 2023
nifty = get_history(symbol="NIFTY", start=date(2023,2,1), end=date(2023,2,10), 
                    index=True)

# save the data
nifty.to_csv("nifty-01Feb23-10Feb23.csv")
```
The returned data looks like as below:
```csv
Date,       Open,    High,     Low,      Close,    Volume,    Turnover
2023-02-01, 17811.6, 17972.2,  17353.4,  17616.3,  512870802, 384861900000.0
2023-02-02, 17517.1, 17653.9,  17445.95, 17610.4,  490113567, 376399600000.0
2023-02-03, 17721.75,17870.3,  17584.2,  17854.05, 424123037, 345036700000.0
2023-02-06, 17818.55,17823.7,  17698.35, 17764.6,  282544790, 218648800000.0
2023-02-07, 17790.1, 17811.15, 17652.55, 17721.5,  354395693, 236110800000.00003
2023-02-08, 17750.3, 17898.7,  17744.15, 17871.7,  290994265, 237334000000.0
2023-02-09, 17885.5, 17916.9,  17779.8,  17893.45, 260854055, 215299700000.0
2023-02-10, 17847.55,17876.95, 17801.0,  17856.5,  231991834, 170639900000.00003
```



### Stocks - EoD OHLC (candle) data
You can get EoD candle-stick data of any NSE listed stocks using the stock `symbol` as follows.
```python
from datetime import date
from nsepy import get_history

# get all the data of state bank (SBIN) from 01 Feb 2023 to 10 Feb 2023
state_bank = get_history(symbol='SBIN', start=date(2023, 2, 1), end=date(2023, 2, 10))

# save the data to a csv file
state_bank.to_csv("sbin-feb.csv")

# plot the data
state_bank[['VWAP', 'Turnover']].plot(secondary_y='Turnover')
```



### NIFTY Futures - EoD OHLC (candle) data
To get NIFTY Futures data, you will need to set the `futures` parameter to `true`. 
You will also need to provide the `expiry_date` and the `strike_price` of the futures contract.

For example, below code will get the data of NIFTY February 18000 futures contract from 1st Feb 2023 to 10th Feb 2023 -
```python
from datetime import date
from nsepy import get_history

# get all the data of NIFTY index from 01 Jan 2023 to 10 Jan 2023
future = get_history(symbol="NIFTY", start=date(2023,1,1), end=date(2023,1,10), 
                    index=True, futures=True, expiry_date=date(2023, 1, 25), strike_price=18000)

# save the data
future.to_csv("nifty-18000-jan-futures-01jan23-10jan23.csv")
```
The sample data looks like this - 
```csv
Date,       Symbol, Expiry,     Open,    High,    Low,      Close,    Last,    Settle     Price,  Number of Contracts, Turnover, Open Interest, Change in OI,Underlying
2023-01-02, NIFTY,  2023-01-25, 18209.0, 18294.4, 18164.7,  18275.85, 18278.7,  18275.85, 109529, 99894735000.0,       10688150, 50600,         18197.45
2023-01-03, NIFTY,  2023-01-25, 18234.9, 18333.9, 18210.05, 18317.3,  18315.0,  18317.3,  135924, 124193686000.00002,  10972750, 284600,        18232.55
2023-01-04, NIFTY,  2023-01-25, 18299.0, 18303.3, 18083.2,  18103.05, 18102.95, 18103.05, 211764, 192351126000.0,      11165400, 192650,        18042.95
2023-01-05, NIFTY,  2023-01-25, 18155.0, 18190.0, 17964.4,  18066.0,  18070.05, 18066.0,  215143, 194462925000.0,      11157600, -7800,         17992.15
2023-01-06, NIFTY,  2023-01-25, 18073.6, 18132.0, 17872.05, 17943.2,  17949.05, 17943.2,  208849, 187794134000.0,      11521550, 363950,        17859.45
2023-01-09, NIFTY,  2023-01-25, 18028.0, 18228.0, 18018.9,  18173.2,  18161.8,  18173.2,  212748, 192975950000.0,      11259900, -261650,       18101.2
2023-01-10, NIFTY,  2023-01-25, 18173.2, 18178.0, 17925.15, 17986.25, 17988.45, 17986.25, 181733, 163695778000.0,      11640350, 380450,        17914.15
```



### Stock Futures - EoD OHLC (candle) data
To get Stock Futures data, you will need to set the `futures` parameter to `true`, and `index` parameter to `False`. 
You will also need to provide the `expiry_date` and the `strike_price` of the intended stock futures contract.

For example, below code will get the data of ITC February 400 futures contract from 1st Feb 2023 to 10th Feb 2023 -
```python
from datetime import date
from nsepy import get_history

# get all the data of NIFTY index from 01 Jan 2023 to 10 Jan 2023
itc_feb_future = get_history(symbol="ITC", start=date(2023,2,1), end=date(2023,2,10), 
                    index=False, futures=True, expiry_date=date(2023, 2, 23), strike_price=400)

# save the data
itc_feb_future.to_csv("itc-400-feb-futures-01Feb23-10Feb23.csv")
```
The sample data looks like this - 
```csv
Date,Symbol,Expiry,Open,High,Low,Close,Last,Settle Price,Number of Contracts,Turnover,Open Interest,Change in OI,Underlying
2023-02-01, ITC, 2023-02-23, 348.9, 360.15, 325.65, 356.0, 354.95, 356.0, 68766,38335244000.0,57374400,5822400,361.4
2023-02-02, ITC, 2023-02-23, 354.95,379.7,  354.95, 373.1, 373.25, 373.1, 40878,24273168000.0,57601600,227200,378.6
2023-02-03, ITC, 2023-02-23, 375.6, 377.1,  366.8,  375.05,375.05, 375.05,16782,10017576000.0,57211200,-390400,380.65
2023-02-06, ITC, 2023-02-23, 377.0, 383.0,  374.25, 378.1, 378.65, 378.1, 20192,12257140000.0,58240000,1028800,383.4
2023-02-07, ITC, 2023-02-23, 373.8, 376.75, 364.05, 368.3, 368.0,  368.3, 19038,11255073000.0,54478400,-3761600,373.25
2023-02-08, ITC, 2023-02-23, 368.35,371.7,  366.75, 370.3, 369.55, 370.3, 6683, 3957991000.0000005,53796800,-681600,375.55
2023-02-09, ITC, 2023-02-23, 367.3, 374.7,  367.15, 370.0, 370.6,  370.0, 7919, 4699826000.0,53422400,-374400,374.25
2023-02-10, ITC, 2023-02-23, 368.35,371.65, 365.8,  366.7, 366.45, 366.7, 6114, 3599310000.0,51800000,-1622400,371.35
```

### NIFTY Options - EoD OHLC (candle) data
To get NIFTY Options data, you will need to set the `option_type` parameter to 'CE' or 'PE' ('CA' or 'PA' for American style options). 
Additionally, you will also need to provide the option's `expiry_date` and the `strike_price` of the option contract.

For example, below code will get the data of NIFTY's 18000 `CALL` options for the month of February from 1st Feb 2023 to 10th Feb 2023 -
```python
from datetime import date
from nsepy import get_history

# get all the data of NIFTY index from 01 Jan 2023 to 10 Jan 2023
future = get_history(symbol="NIFTY", start=date(2023,2,1), end=date(2023,2,10), 
                    index=True, futures=False, option_type='CE', expiry_date=date(2023, 2, 23), strike_price=18000)

# save the data
future.to_csv("nifty-18000-feb-ce-01Feb23-10Feb23.csv")
```
The sample data looks like this - 
```csv
Date,      Symbol, Expiry,     Option Type, Strike Price, Open,  High,   Low,    Close,  Last,  Settle Price, Number of Contracts,Turnover,          Premium Turnover,Open Interest,Change in OI,Underlying
2023-02-01,NIFTY,  2023-02-23, CE,          18000.0,      220.0, 283.9,  100.2,  136.35, 131.0, 136.35,       190910,             173613336000.0,    1794336000.0,2765050,154000,17616.3
2023-02-02,NIFTY,  2023-02-23, CE,          18000.0,      119.95,142.75, 96.85,  114.55, 112.0, 114.55,       77046,              69789964000.0,     448564000.00000006,2904800,139750,17610.4
2023-02-03,NIFTY,  2023-02-23, CE,          18000.0,      131.1, 179.8,  92.0,   166.65, 150.0, 166.65,       105887,             95981525000.0,     683225000.0,2930150,25350,17854.05
2023-02-06,NIFTY,  2023-02-23, CE,          18000.0,      140.1, 147.65, 105.05, 117.0,  113.0, 117.0,        81645,              73961452000.0,     480952000.00000006,3266350,336200,17764.6
2023-02-07,NIFTY,  2023-02-23, CE,          18000.0,      129.15,134.65, 83.5,   96.75,  95.0,  96.75,        90064,              81525422000.0,     467822000.0,3521550,255200,17721.5
2023-02-08,NIFTY,  2023-02-23, CE,          18000.0,      98.0,  142.0,  95.95,  126.45, 123.1, 126.45,       123661,             112065422000.0,    770522000.0,3308550,-213000,17871.7
2023-02-09,NIFTY,  2023-02-23, CE,          18000.0,      125.0, 146.75, 90.5,   129.1,  134.6, 129.1,        122787,             111236568000.0,    728268000.0,3355650,47100,17893.45
2023-02-10,NIFTY,  2023-02-23, CE,          18000.0,      129.1, 129.1,  77.4,   89.2,   87.0,  89.2,         136399,             123361410000.00002,602310000.0,3669300,313650,17856.5
```

### Important Disclaimer:
- This library is heavily inspired and originally forked from [nsepy](https://nsepy.xyz/) library. 
The only reason I decided to create a separate repository here is because I found that 
NSEPY is no longer getting updated in a timely manner, and there are number of PRs with useful features 
and bug-fixes which are not merged to the project for quite some time. 
By having this separate repo, I will be able to keep the project up-to-date and relevant.
- Use this library at your own risk. The author has no liability whatsoever of any financial or reputation loss you may encounter directly or indirectly from using this library.
- This library is provided for education use only. 

## FAQ
### Is this Legal to get this Data?

The data obtained by this Python Library is already available publicly in NSE website. Anyone can visit the website and download this data. This code only provides an easy-to-use wrapper for using this data. It is completely legal.

### Why did I create this Python Library separately where Nsepy already exists?

nse-data-reader is heavily inspired from nsepy - an excellent package originally created by Swapnil Jariwala. I do not know the author personally, but of late I noticed that the nsepy library is not being maintained properly in a timely manner.

I also noticed that there are many PRs with good features and bug fixes which have not been incorporated to the library by the original author.

Due to such uncertainties, I decided to fork my own copy of the nsepy library and maintain it separately.

I added all the bugfixes and some of the new features proposed by others and I improved the overall readability of the code.

### How Can I contribute?
Feel free to fork the repo, make changes/enhancements and send me PR requests. Please make sure to add tests for any code change proposed in the PR.
