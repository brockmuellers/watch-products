# watch-products

I want to know when products that I'm interested in become available on the REI used gear website. I'd like to apply this to other websites too.

I wrote [a little tutorial when making it](https://self.brockmuellers.com/software/2020/02/26/web-scraper-to-find-new-products.html).

TODO: right now this doesn't take into account product color, condition, or any attribute that wasn't specifically in the search query. That would be helpful to add.

TODO: run on lambda, deploy via AWS CLI? Maybe save result files to S3. This can be done with CloudWatch scheduled events <https://medium.com/blogfoster-engineering/running-cron-jobs-on-aws-lambda-with-scheduled-events-e8fe38686e20>/ Also I'll need to build a deployment package because I have dependencies. <https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/>

TODO: figure out better display for comparison results.

TODO: clear out old saved result files periodically.

TODO: tests would be nice, if this tool lasts.

There are also some experimental web scraper scripts in here.
