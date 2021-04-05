# Changelog

- All notable changes to this project are documented in this file.
- This document format is based on the style guidelines at [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- **IMPORTANT:** This project is still in an initial development state, and accordingly cannot be guaranteed to be stable currently.

## [Unreleased]

For upcoming features see the current task list [here](/README.md#task-todo-list).

## [0.1.0] - 2021-04-05

### Added

- Scrapy setup and file structure in `src` directory
- `letterboxd_spider.py` in `src/src/spiders/`
  - main Scrapy spider to crawl letterboxd user's films page
  - extracts film data of all films user has listed as watched
    - data extracted: film title, user rating and liked status if available

### Changed

- Repo readme
  - Updated to v0.1.0
  - Added installation instructions
  - Added usage instructions
- Changelog
  - Added v0.1.0 change notes

## [0.0.0] - 2021-03-04

### Added

- Initial repo creation and setup
- Documentation written:
  - Repo readme
  - Directory readme's
  - This changelog
  - License
