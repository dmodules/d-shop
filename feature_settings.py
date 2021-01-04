
from dshop.models import FeatureList

features = FeatureList.objects.all()

for feature in features:
    exec("%s = %s" % (feature.feature_name, feature.is_enabled))
