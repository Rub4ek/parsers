[![Build Status](https://travis-ci.org/mini-kep/parsers.svg?branch=master)](https://travis-ci.org/mini-kep/parsers)
[![Coverage badge](https://codecov.io/gh/mini-kep/parsers/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parsers)


```parsers``` give you access to data sources,  use ```runner.py``` as entry point. 

Full dataset obtained using code below. The datapoints are from start of dataset. 

```python 
from runner import Dataset

gen = Dataset.yield_dicts()

```

Querying full dataset each time we want up update is a burden on the original API sources. 
Thus, individual parsers can return datapoints from a specific date to present: 

```python
from runner import CBR_USD

gen = CBR_USD(start='2017-09-01').yield_dicts()
```

Generator in ```.yield_dicts()``` method produces dictionaries like this: 

```python 
{'date': '2017-09-13', 
 'freq': 'd', 
 'name': 'BRENT', 
 'value': 55.52}
```

# Parser descriptions

| Parser | RosstatKEP_Monthly |
| ------ | ------------------ |
| Description | Monthly indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Monthly |
| Variables | CPI, GDP, etc |

| Parser | RosstatKEP_Quarterly |
| ------ | -------------------- |
| Description | Quarterly indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Quarterly |
| Variables | CPI, GDP, etc |

| Parser | RosstatKEP_Annual |
| ------ | ----------------- |
| Description | Annual indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Annual |
| Variables | CPI, GDP, etc |

| Parser | CBR_USD |
| ------ | ------- |
| Description | Bank of Russia official USD to RUB exchange rate |
| URL | [http://www.cbr.ru/scripts/Root.asp?PrtId...](http://www.cbr.ru/scripts/Root.asp?PrtId=SXML) |
| Frequency | Daily |
| Variables | USDRUR_CB |

| Parser | BrentEIA |
| ------ | -------- |
| Description | Brent oil price from US EIA |
| URL | [https://www.eia.gov/opendata/qb.php?cate...](https://www.eia.gov/opendata/qb.php?category=241335) |
| Frequency | Daily |
| Variables | BRENT |

Parser types
============

**repo** (*'heavy'*, *'dirty'*) - some parsers are styled to download the data, transform it and provide the output in local folder or URL. These ususally work on bad formats of data, eg Word, and require a lot of work to extract data because the source data is not structured well. 

**serverless** (*'thin'*, *'clean'*, *'API-parcer'*) - some parsers can do the job on query, yield datapoints and die fast and easily because source data is rather clean and fast to get. 


Parser list
===========

At various time following parsers were developed, ```rosstat-kep``` is most advanced one. Original code listings are below.

#### repo: rosstat-kep
Produces output in <https://github.com/mini-kep/parser-rosstat-kep/tree/master/data/processed/latest>

#### API parcer: cbr-usd (CB)
<https://github.com/ru-stat/parser-cbr-usd>

#### API parcer: Brent (EIA)
<https://github.com/epogrebnyak/data-fx-oil/blob/master/brent.py>
result: <https://github.com/epogrebnyak/data-fx-oil/blob/master/brent_daily.txt>

To add
======

#### API parcer: yield curve (Treausry)
<https://github.com/epogrebnyak/ust>
result: <https://raw.githubusercontent.com/epogrebnyak/ust/master/ust.csv> (1.1 Mb)

#### repo: rosstat-806-regional
<https://github.com/epogrebnyak/data-rosstat-806-regional>

