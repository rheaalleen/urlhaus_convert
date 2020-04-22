# urlhaus_convert

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)   [![Version 1.0](https://img.shields.io/badge/Version-1.0-blue)]()      [![Pthon 3.7](https://img.shields.io/badge/Python-3.7-brightgreen)]()

CLI Tool for downloading customized URLHAUS databases/lists

Fetches an entire database and customizes it according to your wishes. Please note that if you need less than 1000 entries abuse.ch already offers an API (https://urlhaus-api.abuse.ch/) but reduced to the newest.


Allows for following:
- Checking availability of every database (All, <30 days, URLs Online)
- Downloading a specific database
- Selecting columns you need (id,dateadded,url,url_status,threat,tags,urlhaus_link,reporter)
- Removing protocols from URL (http:// | https://)
- Editing local databases you downloaded in case you need to work offline

![CLI](https://i.imgur.com/otQM8xO.png "CLI")

Current bugs:
- Last line of file is deleted because CRLF gets lost during editing
- When selecting tags as column the tags get split over multiple columns instead of staying in their original column

Upcoming:
- Fixes & Improvments
- Integrating parts of the API into the functionality to look up certain urls or threats

## Feel free to request features or report bugs
