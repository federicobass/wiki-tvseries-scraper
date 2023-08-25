
# Wikipedia TV Series Scraper

The project consists in a Wikipedia scraper that retrieves data about TV series. \
Currently, the script aims to scrap a list of TV series' episode plots and titles and output them as a list of dictionaries. In the future, I plan to implement more features which are better described in section [Future Works](#future-works). \
This piece of code is particularly useful for Machine Learning purposes, as in generating datasets to train certain ML models regarding TV series.

## Requirements

The script uses a progress bar known as `tqdm` in order to provide feedback of elapsed time to the user. \
If the Python module is not installed on your current machine, simply install it via the following command:

``` terminal
pip install tqdm
```

## Usage / Examples

Simply copy & paste the functions or import the .py file and use accordingly. \
Some pre-processing has already been implemented in the generated output such as the removal of Wikipedia text formatting, although any more pre-processing can be freely implemented as well as any other edit according to the [License](LICENSE.md). \
Currently, a list of Wikipedia pages needs to be given in input, in order to generate the desired output. \

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

build_output_csv(tv_series_name, wiki_episodes_list)
```

The output will be a CSV file with the following structure (also explicited in the CSV file):

| CSV Field | Description |
| --- | --- |
| `season` | _Season number of the TV series_ |
| `title` | _Title of the episode_ |
| `plot` | _Plot of the episode_ |

## Known Issues

The scraper _might_ not fully work due to Wikipedia not always offering every episode's plot for a given TV series. \
As a result of this, the generated data may have "holes" of missing episodes (or entire seasons) due to this unavailability. \
Always check for a TV series completeness on its Wikipedia page(s) before extracting data.

## Future Works

As for the project improvement, I plan to add the following features:

- [ ] Add different output types such as CSV
- [ ] Add more categories to parse (such as n. of seasons, n. of episodes, genre, etc.)
- [ ] Find a way to search TV series without needing to input the exact Wikipedia name
