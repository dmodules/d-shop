
from django.core.management.base import BaseCommand
from dshop.models import FeatureList

class Command(BaseCommand):

    def handle(self, **options):

        print("In Feature command")
        while True:
            print('+========================================================+')
            inp = ''
            features = FeatureList.objects.all().order_by('id')
            for feature in features:
                if feature.is_enabled:
                    format = ';'.join([str(6), str(32), str(40)])
                    f = '\x1b[%sm %s \x1b[0m' % (format, 'True ')
                else:
                    format = ';'.join([str(5), str(31), str(40)])
                    f = '\x1b[%sm %s \x1b[0m' % (format, 'False')
                data = [str(feature.id), feature.feature_name, f]
                print('|{:<8s}{:<33s}{:>5s}        |'.format(data[0], data[1], data[2]))
                print('+--------------------------------------------------------+')

            while True:
                inp = input("Enter Feature ID to Toggle (c to cancle): ") 
                if inp == 'c':
                    break
                try:
                    if inp.isdigit():
                        feature = FeatureList.objects.get(id=int(inp))
                        if feature.is_enabled:
                            feature.is_enabled=False
                        else:
                            feature.is_enabled=True
                        feature.save()
                        break
                except Exception as e:
                    print('Enter Valid Choice')
            
            if inp == 'c':
                break
