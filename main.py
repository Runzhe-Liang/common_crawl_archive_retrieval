from warcio.archiveiterator import ArchiveIterator
import re
import requests


reg_econ = re.compile(" economic| Economic| economics| Economics| economy| Economy")
reg_covid = re.compile(" covid |Covid|COVID|COVID-19|Coronavirus|coronavirus|pandemic|Pandemic")
months = ["January 2020: \n\n", "\n\nFebruary 2020\n\n", "\n\nMarch/April 2020\n\n", "\n\nMay\June 2020\n\n",
          "\n\nJuly 2020\n\n", "\n\nAugust 2020\n\n", "\n\nSeptember 2020\n\n", "\n\nOctober 2020\n\n",
          "\n\nNovember/December 2020\n\n"]

path_header = "https://data.commoncrawl.org/"

month_counter = 0

def retrieve(file_name):
    stream = None
    entries = 0
    matching_entries = 0
    hits = 0

    global month_counter

    if file_name.startswith("http://") or file_name.startswith(
        "https://"
    ):
        stream = requests.get(file_name, stream=True).raw
    else:
        stream = open(file_name, "rb")

    for record in ArchiveIterator(stream):
        covid_cnt = 0
        econ_cnt = 0

        if record.rec_type == "warcinfo":
            continue

        if not ".com/" in record.rec_headers.get_header(
                "WARC-Target-URI"
        ):
            continue

        if "yahoo" in record.rec_headers.get_header(
                "WARC-Target-URI"
        ):
            continue

        entries = entries + 1

        contents = (
            record.content_stream()
            .read()
            .decode("utf-8", "replace")
        )

        find_covid = reg_covid.search(contents)
        find_econ = reg_econ.search(contents)

        if (find_covid and find_econ):
            hits = hits + 1
            covid_cnt += 1
            econ_cnt += 1
            find_covid = reg_covid.search(contents, find_covid.end())
            find_econ = reg_econ.search(contents, find_econ.end())


        while find_covid:
            find_covid = reg_covid.search(contents, find_covid.end())
            hits = hits + 1
            covid_cnt += 1

            if (covid_cnt >= 20):
                break

        while find_econ:
            find_econ = reg_econ.search(contents, find_econ.end())
            hits = hits + 1
            econ_cnt += 1

            if (econ_cnt >= 10):
                break

        if (covid_cnt >= 20 and econ_cnt >= 10):
            f = open('results.txt', 'a')
            f.write(record.rec_headers.get_header("WARC-Target-URI") + '\n')
            f.close()
            matching_entries = matching_entries + 1
            month_counter += 1


    print(
        "Python: "
        + str(hits)
        + " matches in "
        + str(matching_entries)
        + "/"
        + str(entries)
    )

def main():
    for i in range(9):
        file = open('results.txt', 'a')
        file.write(months[9 - i])
        file.close()

        global month_counter

        month_counter = 0

        file = open('wet.paths' + str(9 - i), 'r')
        paths = file.readlines()

        for path in paths:
            file_name = path_header + path[:-1]
            print(file_name)
            retrieve(file_name)

            if (month_counter >= 200):
                break

        file.close()




main()