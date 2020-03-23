# watch-products

I want to know when products that I'm interested in become available on the REI used gear website. I'd like to apply this to other websites too, so this is a bit overly generalized.

This uses the BeautifulSoup library to parse web page data. Pages to scrape (representing the results of a product search on the website) and their human-readable labels are loaded from a CSV. Results are written to local files, so I can compare the products available now to the products available last time I ran the tool. The result of the comparison is printed in the console.

This is my first time web scraping, so I wrote [a little guide when making it](https://self.brockmuellers.com/software/2020/02/26/web-scraper-to-find-new-products.html). I like reading guides like this when I'm learning something new, so maybe it can help someone else. Plus, it was helpful in organizing my thought process.

I'm also dumping other experimental product scraping scripts in here.

TODOs: 
* Tests!! Ideally, download a page and mock the web call.
* Right now this doesn't take into account product color, condition, or any attribute that wasn't specifically in the search query. That would be helpful to add.
* Automate. Run on Lambda, deploy via AWS CLI? Maybe save result files to S3. This can be done with CloudWatch scheduled events <https://medium.com/blogfoster-engineering/running-cron-jobs-on-aws-lambda-with-scheduled-events-e8fe38686e20>/ Also I'll need to build a deployment package because I have dependencies. <https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/>
* Implement email alerts.
* Figure out better display for comparison results.
* Clear out old saved result files periodically.

