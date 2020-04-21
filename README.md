# urlhaus_convert
CLI Tool for downloading customized URLHAUS databases/lists

Fetches an entire database and customizes it according to your wishes. Please note that if you need less than 1000 entries abuse.ch already offers an API (https://urlhaus-api.abuse.ch/) but reduced to the newest.



Allows for following:
- Checking availability of every database (All, <30 days, URLs Online)
- Downloading a specific database
- Selecting columns you need (id,dateadded,url,url_status,threat,tags,urlhaus_link,reporter)
- Removing protocols from URL (http:// | https://)
- Editing local databases you downloaded in case you need to work offline

Current bugs:
- Last line of file is deleted because CRLF gets lost during editing
- When selecting tags as column the tags get split over multiple columns instead of staying in their original column

Upcoming:
- Fixes & Improvments
- Integrating parts of the API into the functionality to look up certain urls or threats
