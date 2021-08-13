BOT_NAME = 'blog'

SPIDER_MODULES = ['blog.spiders']
NEWSPIDER_MODULE = 'blog.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'blog.pipelines.BlogPipeline': 300,
}
