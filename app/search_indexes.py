from haystack import indexes
from app.models import Article


# ArticleIndex:建立索引的表模型名+Index
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # document=True：根据自定义模版字段建立索引，字段可以有多个，document=True有且只能有一个；use_template=True：允许使用自定义模版，与document=True搭配使用
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    title = indexes.CharField(model_attr='title')
    # title = indexes.CharField(model_attr='title', analyzer="ik_max_word")
    content = indexes.CharField(model_attr='content')
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        # 从es中搜索，返回的数据从数据库获取
        return self.get_model().objects.all()
