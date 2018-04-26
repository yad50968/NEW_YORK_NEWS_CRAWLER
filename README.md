# New York News Crawler

Easily getting the news from [New York Times](https://www.nytimes.com/).

## INFO

ONLY FOR EDUCATION 方便從New York Times抓取新聞資料，供學術使用

## Requirements

1. [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
2. [selenium](https://www.seleniumhq.org)
3. [python3](https://www.python.org/)

### INPUT FILE FORMAT

```sh

It will fetch all the search topic during start time and end time.
```
```
| Search | Start Time | End Time |
| ------ | ---------- | -------- |
| Wet Seal Inc | 2010/7/1 |	2010/12/31 |
| Local Corp   | 2010/7/1 | 2010/12/31 |

### OUTPUT FILE FORMAT

One topic output to one folder.

NEWS_TOPIC </br>
NEWS_TIME </br>
NEWS_CONTENT </br>

### RUN

```sh
git clone https://github.com/yad50968/NEW_YORK_NEWS_CRAWLER.git
cd NEW_YORK_NEWS_CRAWLER
python3 ./main.py
```
