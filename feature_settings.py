
from settings import FEATURES

ALL_FEATURES = [
    'QUOTATION',
    'FEATURE1',
    'FEATURE2'
]

for feature in ALL_FEATURES:
    exec("%s = %s" % (feature, False))

features = FEATURES.split(',')
for feature in features:
    exec("%s = %s" % (feature, True))
