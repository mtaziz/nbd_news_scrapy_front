# coding:utf-8
import datetime
from haystack import indexes
from front.models import Articles


class KeywordResultIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # when user_template true ,you must set template_names
    # template_names = ['search/indexes/%s/%s_%s.txt' % (app_label, model_name, self.instance_name)]
    article_title = indexes.CharField(model_attr='article_title')
    article_for_crawl_media = indexes.CharField(model_attr='article_for_crawl_media')

    def get_model(self):
        return Articles

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(article_updated_at__lte=datetime.datetime.now())
