import urllib.request
import urllib.error
from urllib.request import urlopen
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd
import csv
import zipfile


def arg_parse():
    parser = argparse.ArgumentParser(description='CLI Tool for downloading customized URLHAUS lists', formatter_class=RawTextHelpFormatter)
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--database', help="Which database you want to download", choices=['all', 'recent', 'online'], required=False, default=None)
    parser.add_argument('-o', '--output', help="Output name", default='urlhaus_convert.csv')
    parser.add_argument('-c', '--check', choices=['all', 'recent', 'online'], help="Check the database(s) availability \n" "all = Entire database of URLHAUS \n""recent = Database of the last 30 days \n""online = Only entries that are marked online \n")
    parser.add_argument('-col', '--columns', help="Select the columns you want", default='urlhaus_convert.csv')
    parser.add_argument('-p', '--protocol', help="Remove protocol in url", action='store_true')
    parser.add_argument('-l', '--local', help="Path to local file, including file name(csv.txt), if you supply it")
    args = parser.parse_args()

    if not (args.check or args.database):
        parser.error("One of the options (-check/-database) is needed, either check availability or download a database")

    if (args.check and args.database):
        parser.error("Only one of the options at the time, either check (-c) or download (-d)")

    return args


def urlhaus_links():
    urlhaus_all = ("https://urlhaus.abuse.ch/downloads/csv/", "Database: All")
    urlhaus_recent = ("https://urlhaus.abuse.ch/downloads/csv_recent/", "Database: <30 days")
    urlhaus_online = ("https://urlhaus.abuse.ch/downloads/csv_online/", "Database: Verified online")
    return urlhaus_all, urlhaus_recent, urlhaus_online


def url_status(url, status, descr):
    if status == 200:
        print(descr + " [\u2713]")
    elif 400 <= status <= 511:
        print(descr + " [\u2A2F]" + "Error: " + status)

def urlcheck():
    urls = urlhaus_links()

    index = "Online: [\u2713], Offline: [\u2A2F]"
    print(index)

    for url, descr in urls:
        try:
            conn = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            # ...
            print('HTTPError: {}'.format(e.code) + ', ' + url)
            print(index)
            url_status(url, e.code, descr)
        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            # ...
            print('URLError: {}'.format(e.reason) + ', ' + url)
            url_status(url, e.reason, descr)
        else:
            # 200
            # ...
            url_status(url, conn.status, descr)
    exit(0)

def format_file(data):
    temp_file = open("csv.txt", "w+")
    for line in data:
        temp_file.write(str(line))

    with open('csv.txt', 'r') as urls_in:
        data = urls_in.read().splitlines(True)

    with open('urlhaus_temp.txt', 'w') as urls_out:
        urls_out.writelines(data[18:])

    temp_file.close()
    urls_in.close()
    urls_out.close()


def download(args):
    links = urlhaus_links()

    if args.check is not None:
        urlcheck()

    if args.database == 'all':
        url = links[0][0]
    elif args.database == 'recent':
        url = links[1][0]
    elif args.database == 'online':
        url = links[2][0]

    if args.local:
        path = args.local
        with open(path, 'r') as file:
            data = file.read().splitlines(True)
            with open('urlhaus_temp.txt', 'w') as urls_out:
                urls_out.writelines(data[18:])
                return


    if args.database == 'all':
        with urllib.request.urlopen(url) as dl_file:
            with open("all.zip", 'wb') as out_file:
                out_file.write(dl_file.read())
        archive = zipfile.ZipFile('all.zip', 'r')
        data = archive.read('csv.txt').decode('utf-8')
        format_file(data)
    else:
        text = urlopen(url)
        data = text.read().decode('utf-8')
        format_file(data)

        # with tempfile.NamedTemporaryFile(mode='w+b', delete=True) as tmp:
        #     for line in data:
        #         tmp.write(line.encode())
        #     tmp.seek(0)
        #
        #     with tempfile.NamedTemporaryFile(mode='w+b', delete=True) as tmp1:
        #         lines = tmp.readlines()[1:]
        #         for i in lines:
        #             i.decode('utf-8')
        #             tmp1.write(i)
        #
        #         print(tmp1.name)

def to_csv(args):
    dataframe = pd.read_csv('urlhaus_temp.txt', sep=",", header=None, engine='python', error_bad_lines=False)
    dataframe.columns = ["id", "dateadded", "url", "url_status", "threat", "tags", "urlhaus_link", "reporter"]
    dataframe.to_csv('urlhaus_first.csv')

    all_data = pd.read_csv("urlhaus_first.csv")
    splits = args.columns
    columns = splits.split(",")
    keep_columns = columns
    new_csv = all_data[keep_columns]

    pd.options.mode.chained_assignment = None

    if args.protocol:
        new_csv['url'] = new_csv['url'].apply(lambda x: '"' + str(x).replace("http://", "").replace("https://", "") + '"')
        final_csv = new_csv
        final_csv.drop_duplicates(subset=None, inplace=True)
        final_csv.to_csv(args.output, index=False, quoting=csv.QUOTE_NONE, quotechar='"', escapechar="\\")
    else:
        final_csv = new_csv
        final_csv.drop_duplicates(subset=None, inplace=True)
        final_csv.to_csv(args.output, index=False, quoting=csv.QUOTE_NONE, quotechar='"', escapechar="\\")


if __name__ == "__main__":
   arg = arg_parse()
   download(arg)
   to_csv(arg)
