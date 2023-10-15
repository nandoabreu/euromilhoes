# Time Series and Forecast project - Part 1
This paper responds to the course project for the Time Series and Forecast course,
ministered by the Professor Maria Eduarda Silva, for UP - Universidade do Porto.

## Assignment

Choose a time series of your interest and write a concise report
(pdf, max 6 pages, including appendices) describing
the exploratory analysis of the time series.

### The time series

The time series here employed has data for Euromilhões draws in Portugal. The data set,
a [CSV file](../data/euromilhoes.pt.csv), holds data from 2004 to October 2023, but the present study
will consider draws between 2018 and 2022.

In the period of our study, the time series shows events twice a week. There are 522 events in the serie.

```text
# Description of the data:
min draw_date                  2018-01-02
max draw_date                  2022-12-30
count draw_date                       522
count draws/year                  104-105
count draws/week                      1.9
sum bids                       1443202757
```

\
The following is the first visualization of the time series. The plot show the complete timeline, with the bids.
![euromilhoes-timeline.pt.png](euromilhoes-timeline.pt.png)
