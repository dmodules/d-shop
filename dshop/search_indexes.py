from django.conf import settings as config
from shop.search.documents import ProductDocument

settings = {
    'number_of_shards': 1,
    'number_of_replicas': 0,
}
for language, _ in config.LANGUAGES:
    ProductDocument(language=language, settings=settings)
