# euromilhoes
Time Series data analysis for the Euromilhões lottery draws

This project develops an exercise from an assignment for the
Time Series and Forecast, from the Data Science M.Sc. course,
from UP - Universidade do Porto (Porto University, Portugal).

## The assignment
[The project is described in this page](docs/assignment.md)

## The project
The project was developed since the extraction of the data, up to
developing the analysis and reports. The data is about the draws for the
Portuguese part os the EuroMillions draw.

### Technology
This project was developed using Python v3.10 and several Python libraries
running locally over a virtual environment managed by Python Poetry. The
GNU/Linux OS is the core for the used distribution, Ubuntu v23.

***To run this project's code, setup Python Poetry and install the project.***

### Data extraction
The dataset for the Euromilhões draw is not directly available, but the data
can be fetched through HTTP. It is available throught the
[Portal Jogos Santa Casa](https://www.jogossantacasa.pt/web/JogarEuromilhoes/)
website.

A webscraping module was built using Python and libraries available 
for the programming language. The code for this module can be found
in the [setup directory](setup).

#### Python libraries
For the data extraction module, along with some built-in libraries,
a list of third-parties libraries were used. The main ones are listed bellow:

- [requests](https://pypi.org/project/requests/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)

#### Instructions
A Makefile is available with recipes.
[Check the file](Makefile) or simply run the following to extract, parse and store:
```shell
make extract-raw-data && make parse-and-store
```

_414.8 MB are fetched when scrapping all data; 1600+ html files will be stored from the extraction_

### Data load and Plots creation
Data loading is part of the main Python module. The stored data
is loaded and feeds the system to generate reportas and plots.
Check [the data directory](data) for the dataset, created plots and reports.

#### Python libraries
For the data visualization module, along with some built-in libraries,
a list of third-parties libraries were used. The main ones are listed bellow:

- [numpy](https://pypi.org/project/numpy/)
- [pandas](https://pypi.org/project/pandas/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [seaborn](https://pypi.org/project/seaborn/)

#### Instructions
A Makefile is available with recipes.
[Check the file](Makefile) or simply run the following to crete the plots:
```shell
make create-plots
```
