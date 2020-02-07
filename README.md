# twitter-stock-sentiment-analysis
A sentiment analysis in the Brazil Stock Market using tweets

## Tweets Search

```
usage: search.py [-h] [-c COUNT] [--since SINCE] [--until UNTIL] [-l LANG]
                 [--dest DEST]
                 query

positional arguments:
  query                 Query to be searched

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of tweets per page
  --since SINCE         Start date
  --until UNTIL         End date
  -l LANG, --lang LANG  Tweets language
  --dest DEST           Destination path
```