# common_crawl_archive_retrieval

The main part of this python crawler is `main.py`, which is based on the provided basic script from **code402**.
The `results.txt` contains all the selected URLs, categorized by the month of the `WET` file they belong to.

The crawler works by setting up correct HTTPS path to retrieve `WET` files from the web, and then analyze the 
webpages one by one. The reason we use the `WET` files instead of `WARC` files is because `WET` files are, after 
a fair amount of testing, more relevant to the contents of the page and can result in higher retrieval precision. 

We record a web page as long as it as at least 20 occurrences of *COVID* related keywords and 10 occurrences of
*economy* related keywords. We also conduct a pre-filtering to exclude all URLs that do not contain `.com` and 
all URLs that may contain excessive information and thus abuse our retrieval standards (e.g. pages from yahoo.news 
tend to do this as each of them contains lot of "side-information" that doesn't actually belong to the main content
of the webpage). The pre-filtering improves the retrieval accuracy significantly as well. 

Due to the time limit, more experiments could not be carried out. For example, we can design more elaborated 
boolean queries to achieve higher retrieval precision and get more relevant webpages, based on our ablations. The
current retrieval list is not ranked. We can use different metrics to order the retrieval results if that's wanted.
A simple metric would be the total number of occurrences of *COVID* related keywords plus *economy* related keywords.

To diversify the retrieval result, also to decrease retrieval time, we set an upper bound of documents that each 
month can contribute. An alternative way could be getting all the relevant documents first, and then rank them 
according to some universal standard, and take the top n documents.