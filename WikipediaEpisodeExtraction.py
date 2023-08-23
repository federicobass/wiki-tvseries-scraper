# USEFUL LINKS
#
# MediaWiki API, used for JSON retrieval of Wikipedia's data through GET requests
# https://www.mediawiki.org/wiki/API:Parsing_wikitext
#

import os
import re
import requests
import sys


section_typo_list = ["episodes", "season synopsis", "season synopses", "series overview"]
wiki_requests_session = requests.Session()

# Parse Wikipedia page's sections list in JSON format.
def get_wiki_page_sections(title):
    wiki_season_list = []
    wiki_section_index = "-1"

    # Clean title left and right from whitespaces and substitute whitespaces in string with underscores for compatibility
    title = title.strip().replace(" ", "_")
    # Retrieve list of page's sections in JSON format ready to be parsed
    wiki_scrapped_data = wiki_requests_session.get(f"https://en.wikipedia.org/w/api.php?action=parse&page={title}&prop=sections&format=json").json()

    # Handle inexistent Wikipedia input page
    if "error" in wiki_scrapped_data:
        print(f"ERROR: {wiki_scrapped_data['error']['info']}")
        sys.exit(os.EX_DATAERR)
    
    # Loop through Contents table entries to find episodes sub-entries
    for entry in wiki_scrapped_data["parse"]["sections"]:
        # Get entry index for next GET request to find specific section by checking for specific sub-sections
        if entry["line"].strip().lower() in section_typo_list:
            wiki_section_index = entry["index"]
            break

    # Use index entry saved above to retrieve specific section links (list of seasons in our case)
    wiki_data_subsections = wiki_requests_session.get(f"https://en.wikipedia.org/w/api.php?action=parse&page={title}&prop=links&section={wiki_section_index}&format=json").json()

    if "error" in wiki_data_subsections:
        print(f"ERROR: {wiki_data_subsections['error']['info']}")
        sys.exit(os.EX_DATAERR)

    # Loop through each entry to retrieve links text and format them to URL standard using underscores instead of whitespaces
    for entry in wiki_data_subsections["parse"]["links"]:
        # Insert all the links regarding episodes and season episodes which will be filtered later
        if "season" in entry["*"].strip().lower() or "episodes" in entry["*"].strip().lower():
            wiki_season_list.append(entry["*"].strip().replace(" ", "_"))

    # Check if "List of xxxxx episodes" page contains a link redirecting to individual seasons, each containing episodes and plots
    if "List_of_" in wiki_season_list[0] and len(wiki_season_list) == 1:
        wiki_episode_list_page = wiki_requests_session.get(f"https://en.wikipedia.org/w/api.php?action=parse&page={wiki_season_list[0]}&prop=links&format=json").json()

        # Append each season's link to our final list of links (to each individual season) to be processed
        for link in wiki_episode_list_page["parse"]["links"]:
            if "(season " in link["*"]:
                wiki_season_list.append(link["*"].strip().replace(" ", "_"))

    # Filter links inside the newly populated list by removing unnecessary "List_of_xxxxx_episodes" if individual seasons with plots are available
    if "List_of_" in wiki_season_list[0] and len(wiki_season_list) > 1:
        del wiki_season_list[0]

    return wiki_season_list

# Parse episodes' title and plot from Wikipedia for each season if available. Parse it from episode list if season synopsis is unavailable.
def get_episodes_data(season_entry):
    wiki_episodes_list = []
    wiki_section_index = "-1"

    # Get Wikipedia's page about specific series' season
    wiki_scrapped_data = wiki_requests_session.get(f"https://en.wikipedia.org/w/api.php?action=parse&page={season_entry}&prop=sections&format=json").json()

    # Loop through each section in web page to extract "Episodes" section specifically by targeting its 'index' field in JSON
    for entry in wiki_scrapped_data["parse"]["sections"]:
        if "episodes" in entry["line"].strip().lower():
            wiki_section_index = entry["index"]

    # Use 'index' field to extract links in specific section (Episodes' section in this case)
    wiki_scrapped_links = wiki_requests_session.get(f"https://en.wikipedia.org/w/api.php?action=parse&page={season_entry}&prop=wikitext&section={wiki_section_index}&format=json").json()

    # Compile regular expressions for title and plot extraction from JSON
    episode_title_pattern = re.compile(r"\| ?Title *= *(.*?) *\n")
    episode_plot_pattern = re.compile(r"\| ?ShortSummary *= *(.*?) *\n")
    episode_titles_list = episode_title_pattern.findall(wiki_scrapped_links["parse"]["wikitext"]["*"])
    episode_plots_list = episode_plot_pattern.findall(wiki_scrapped_links["parse"]["wikitext"]["*"])
    
    # Compile regular expression for plots' text pre-processing
    regex_clean_hyperlinks_pattern_v1 = re.compile(r"\[\[([^|\]]*)\]\]")
    regex_clean_hyperlinks_pattern_v2 = re.compile(r"\[\[(.*)\|(.*)\]\]")
    regex_clean_tags_pattern = re.compile(r"(.*?)(<.*>)?")
    
    # Create a dict containing each episode's title and plot (pre-processed) and append it to episodes list
    for i in range(0, len(episode_titles_list)):
        # Pre-process strings by cleaning them from useless characters (Wikipedia formatting)
        episode_title = re.sub(regex_clean_hyperlinks_pattern_v1, r"\1", episode_titles_list[i])
        episode_title = re.sub(regex_clean_hyperlinks_pattern_v2, r"\2", episode_title).strip()
        episode_plot = re.sub(regex_clean_hyperlinks_pattern_v1, r"\1", episode_plots_list[i])
        episode_plot = re.sub(regex_clean_hyperlinks_pattern_v2, r"\2", episode_plot)
        episode_plot = re.sub(regex_clean_tags_pattern, r"\1", episode_plot)
        episode_plot = bytes(episode_plot, "utf-8").decode().replace("''", "\"").strip()
        
        # Add each episode to season's dictionary
        wiki_episodes_list.append({
            "title": episode_title,
            "plot": episode_plot
        })
    
    return wiki_episodes_list