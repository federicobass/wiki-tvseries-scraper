
# Wikipedia TV Series Scraper

The project consists in a Wikipedia scraper that retrieves data about TV series. \
Currently, the script aims to scrap a list of TV series' episode plots and titles and output them as a list of dictionaries. In the future, I plan to implement more features which are better described in section [Future Works](#future-works). \
This piece of code is particularly useful for Machine Learning purposes, as in generating datasets to train certain ML models regarding TV series.

## Usage / Examples

Simply copy & paste the functions or import the .py file and use accordingly. \
Some pre-processing has already been implemented in the generated output such as the removal of Wikipedia text formatting, although any more pre-processing can be freely implemented as well as any other edit according to the [License](LICENSE.md). \
Currently, a list of Wikipedia pages needs to be given in input, in order to generate the desired output. \
 \
For example:

| TV series | Input | Wikipedia URL title |
| --------------- | --------------- | --------------- |
| `How I Met Your Mother` | How I Met Your Mother | How_I_Met_Your_Mother |
| `Superstore` | Superstore (TV series) | Superstore_(TV_series) |
|

As shown, some TV series titles have the suffix `(TV Series)` according to their title in the Wikipedia pages.

### Usage Showcase

In this showcase I demonstrate how to scrape episodes' plot and title of the TV series "How I Met Your Mother":

``` python
series_episodes = [ ]

season_entry_list = get_wiki_page_sections("How I Met Your Mother")

for season_num, season in enumerate(season_entry_list, 1):
  series_episodes.append({ "season": season_num, "data": get_episodes_data(season) })
```

The output will be a dictionary with the following structure:

| Dictionary Field | Description |
| --- | --- |
| `season` | _Season number of the TV series_ |
| `data` | _List of dictionaries comprising the `title` and the `plot` of each season's episode_ |
|

## Known Issues

The scraper _might_ not fully work due to Wikipedia not always offering every episode's plot for a given TV series. \
As a result of this, the generated data may have "holes" of missing episodes (or entire seasons) due to this unavailability. \
As a suggestion, always check for a TV series completeness on its Wikipedia page(s) before extracting data.

## Future Works

As for the project improvement, I plan to add the following features:

- [ ] Add more categories to parse (such as n. of seasons, n. of episodes, genre, etc.)
- [ ] Add different output types such as CSV
- [ ] Find a way to search TV series without needing to input the exact Wikipedia name
