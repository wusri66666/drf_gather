import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_gather.settings')
django.setup()

from app.models import Article


Article.objects.create(title='三国演义', content='三英战吕布，人民', author='罗贯中')
Article.objects.create(title='水浒传人民', content='梁山好汉', author='施耐庵,中华人民共和国')
Article.objects.create(title='红楼梦', content='大观园，共和国', author='曹雪芹')
Article.objects.create(title='西游记', content='孙悟空', author='吴承恩')
Article.objects.create(title='python入门到入土', content='人生苦短，我用python，国', author='吴正军')
Article.objects.create(title='中华人民共和国', content='人生苦短，我用python', author='吴正军')


# from elasticsearch import Elasticsearch
#
# client = Elasticsearch(["http://192.168.4.235:9200"])
#
# response = client.search(
#     index="test",
#     body={
#         "query": {
#             "match": {
#                 "title": "中华人民共和国"
#             }
#         }
#     }
# )
#
# print(response)
