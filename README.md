
# Wikipedia TV Series Scraper

The project consists in a Wikipedia scraper that retrieves data about TV series. \
This piece of code is particularly useful for Machine Learning purposes, as in generating datasets to train certain ML models regarding TV series. \
Currently, the script aims to scrap a list of TV series' episode plots and titles and output them in a file, or as a list of seasons where each season contains all of its episodes. The script implementation, as well as a basic how-to-use, are better explained in section [Usage / Examples](#usage--examples). \
In the future, I plan to implement more features which are better described in section [Future Works](#future-works).

## Requirements

The script uses a progress bar known as `tqdm`, in order to provide feedback of elapsed time to the user., and the library `pandas` for data handling. \
If any Python module is not installed on your current machine, simply install it via the following terminal command:

``` terminal
pip install pandas
pip install tqdm
```

## Usage / Examples

Simply copy & paste the functions or import the .py file and use accordingly. \
Some pre-processing has already been implemented in the generated output such as the removal of Wikipedia text formatting, although any more pre-processing can be freely implemented as well as any other edit according to the [License](LICENSE.md). \
Currently, a list of Wikipedia pages needs to be given in input, in order to generate the desired output.

For example:

| TV series | Input | Wikipedia URL title |
| --------------- | --------------- | --------------- |
| `How I Met Your Mother` | How I Met Your Mother | How_I_Met_Your_Mother |
| `Superstore` | Superstore (TV series) | Superstore_(TV_series) |

As shown, some TV series titles have the suffix `(TV Series)` according to their title in the Wikipedia pages.

### Usage Showcase

In this showcase I demonstrate how to scrape episodes' plot and title of the TV series `How I Met Your Mother`:

``` python
tv_series_name = "How_I_Met_Your_Mother"
wiki_episodes_list = [ ]

wiki_season_list = get_wiki_seasons_list(tv_series_name)

for season_number, season in tqdm(enumerate(wiki_season_list, 1), desc="Scraping", total=len(wiki_season_list)):
    wiki_episodes_list.append(get_episodes_data(season, season_number))

generate_output_file(tv_series_name, wiki_episodes_list, "csv")
generate_output_file(tv_series_name, wiki_episodes_list, "xlsx")

```

The output will be either a CSV file or a XLSX _(Excel)_ file with the following structure:

| CSV Field | Description |
| --- | --- |
| `season` | _Season number of the TV series_ |
| `title` | _Title of the episode_ |
| `plot` | _Plot of the episode_ |

## Functions Return

Each function gives the following output:

- `get_wiki_seasons_list`: returns a _List_ of TV series' seasons that will be given as input to the function _`get_episodes_data`_ for the next step
- `get_episodes_data`: returns a _List_ of _Dicts_, where each _Dict_ contains the data of a single episode for a (single) given season
- `generate_output_file`: generates a file containing freshly scraped data for a single TV series

## Known Issues

The scraper _might_ not fully work due to Wikipedia not always offering every episode's plot for a given TV series. \
As a result of this, the generated data may have "holes" of missing episodes (or entire seasons) due to this unavailability. \
Always check for a TV series completeness on its Wikipedia page(s) before extracting data.

## Future Works

As for the project improvement, I plan to add the following features:

- [x] Add different output types such as CSV
- [ ] Add more categories to parse (such as n. of seasons, n. of episodes, genre, etc.)
- [ ] Find a way to search TV series without needing to input the exact Wikipedia name
