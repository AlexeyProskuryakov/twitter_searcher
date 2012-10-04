__author__ = '4ikist'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def visualise(points, x=lambda x:x['x'], y=lambda x:x['y'], header='vis', x_title='X', y_title='Y', spec_symbols = None):
    """
    points must be a list of dicts like that {'x':some_value,'y':some_value}
    """
    x_line = []
    y_line = []
    for point in points:
        x_line.append(float(x(point)))
        y_line.append(float(y(point)))

    plt.plot(x_line, y_line, 'ro')

    if spec_symbols:
        for spec_symbol_el in spec_symbols:
            plt.plot(spec_symbol_el['x'], spec_symbol_el['y'], 'g^')

    plt.xlabel(x_title)
    plt.ylabel(y_title)
    
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    points = [
            {'y': 20, 'x': 1.4991384107263104, 'user': u'@LiveTubeDotCom'},
            {'y': 20, 'x': 1.5030655816766587, 'user': u'@gayHotMovies'},
            {'y': 12, 'x': 1.6432034223221204, 'user': u'@_6982439375591'},
            {'y': 20, 'x': 2.0868280370924746, 'user': u'@sniganna'},
            {'y': 20, 'x': 2.241280419929893, 'user': u'@90kama'},
            {'y': 20, 'x': 2.3176176418325016, 'user': u'@pornfindr'},
            {'y': 20, 'x': 2.3731730341285338, 'user': u'@Strayk24'},
            {'y': 20, 'x': 2.6852879244326155, 'user': u'@limoshkaaaaa'},
            {'y': 20, 'x': 2.775494491093861, 'user': u'@IndividualkiPit'},
            {'y': 3, 'x': 2.8302831563470794, 'user': u'@jim79616761'},
            {'y': 20, 'x': 2.837388786650144, 'user': u'@etxt_ru'},
            {'y': 20, 'x': 2.885355447859755, 'user': u'@itm_rostov'},
            {'y': 20, 'x': 2.9480972682318027, 'user': u'@FreeAmateurVids'},
            {'y': 20, 'x': 2.9584880616839806, 'user': u'@ProstitutkaMosk'},
            {'y': 18, 'x': 2.970792081426378, 'user': u'@alemapimeon'},
            {'y': 20, 'x': 2.9863173323466405, 'user': u'@pornear'},
            {'y': 20, 'x': 3.0124676317959262, 'user': u'@PornoBesplatno'},
            {'y': 20, 'x': 3.0267842857659595, 'user': u'@xxxadult_ru'},
            {'y': 20, 'x': 3.054258025110534, 'user': u'@ElektriSa'},
            {'y': 20, 'x': 3.077773216121245, 'user': u'@MissisSexy'},
            {'y': 19, 'x': 3.0938459433266243, 'user': u'@dkhflkktureyu'},
            {'y': 17, 'x': 3.170868187690805, 'user': u'@Pshottah'},
            {'y': 20, 'x': 3.191543810433292, 'user': u'@yaomtv'},
            {'y': 20, 'x': 3.2138261243141533, 'user': u'@refpro04'},
            {'y': 20, 'x': 3.2726402320709034, 'user': u'@Rimsskii'},
            {'y': 20, 'x': 3.3244435903163847, 'user': u'@dzhekercom'},
            {'y': 2, 'x': 3.385872283436453, 'user': u'@JuliaSinai'},
            {'y': 19, 'x': 3.413054855518405, 'user': u'@Elithatka'},
            {'y': 13, 'x': 3.4137203254207553, 'user': u'@Rozakhudyakova'},
            {'y': 7, 'x': 3.4544272538662337, 'user': u'@iStoreRussia'},
            {'y': 18, 'x': 3.534464696576809, 'user': u'@sonedas'},
            {'y': 20, 'x': 3.534758220752947, 'user': u'@masterokst'},
            {'y': 2, 'x': 3.5858022206241715, 'user': u'@joellaxa'},
            {'y': 2, 'x': 3.6211315682268133, 'user': u'@Dating_Advice_'},
            {'y': 1, 'x': 3.7606383450036343, 'user': u'@0760805129'},
            {'y': 2, 'x': 3.8301260740362477, 'user': u'@sharobi0591'},
            {'y': 1, 'x': 3.9856263633521567, 'user': u'@natasha6242'},
            {'y': 1, 'x': 4.1355933079274845, 'user': u'@emmanueladuvaga'},
            {'y': 1, 'x': 4.88557414136177, 'user': u'@BiBee13'},
    ]
    visualise(points, header='test', x_title='XX', y_title='YY')