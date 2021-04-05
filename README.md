# Letterboxd Automated Local Backup Tool

Tool for locally backing up account data for [Letterboxd](https://letterboxd.com), a film-focussed social media site. Once set up, tool automatically scrapes your letterboxd account page at regular intervals to maintain an up to date backup of your account data locally. Data backed up includes list of watched films, along with rating, watch date, and review data when available, as well as any user-created lists. Allows for easy extracting of your film data from letterboxd, whether for backup purposes or for personal use.

## Current Version: v0.1.0

- **Project is currently in an incomplete initial development state.**  For a list of work to be done before reaching a viable complete state, please see the current task list [here](#task-todo-list).
- Most recent version notes available [here](/docs/CHANGELOG.md)

## Installation

Place `src` folder in directory of choice, leaving file structure as is. Note that Scrapy must be installed either system-wide, or in a python virtual environment in your chosen backup directory. For Scrapy install instructions see [here](https://docs.scrapy.org/en/latest/intro/install.html).

## Usage

- **Note:** Project is still in active development, and as such currently only manual backing up is available. Backup currently extracts a list of the user's watched films, with the title as well as the users rating if any and liked status if any, stored as a single .csv or JSON file.
- To generate a backup of account data, from the command line inside the directory containing the `src` folder, (as well as within the python virtual environment if using) run

```
scrapy crawl letterboxd -a user=your_username -O films.csv
```
with your letterboxd username as `your_username`, and a backup filename of your choice.

- To save backup as a JSON file instead of a .csv, simply replace the backup filename ending with `.json`

## Task Todo List

- [x] Finish repo setup (cleanup documentation, update .gitignore, branches)
- [x] Basic web scraper to scrape account data
- [ ] Automation script
- [ ] Finalize design planning
- [ ] Polish scraper (what data is and isnt collected, etc.)
- [ ] Finalize storage format
- [ ] Installation/initial setup script
- [ ] Testing, cleanup
- [ ] Update README

## Contributing

Pull requests always welcome, please push changes to dev branch, not main.

## License

Project is licensed under the MIT License - see [here](docs/LICENSE.txt) for full license.
