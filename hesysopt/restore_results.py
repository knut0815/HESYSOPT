# -*- coding: utf-8 -*-
"""
This module is used to configure the plotting. At the momemt it reads for
the default all results path  and creates a multiindex dataframe. This is
used by the different plotting-modules. Also, colors are set here.

Note: This is rather ment to illustrate, how hesysopt results can be plotted,
than to depict a complete plotting ready to use library.

"""
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def restore(scenarios=['1HBP', '2HBP', '4HBP']):
    homepath = os.path.expanduser('~')

    main_df = pd.DataFrame()
    for s in scenarios:
        resultspath = os.path.join(homepath, 'hesysopt_simulation', s, 'results',
                                   'all_results.csv')
        tmp = pd.read_csv(resultspath)
        tmp['Scenario'] = s
        main_df = pd.concat([main_df, tmp])

    # restore orginial df multiindex
    main_df.set_index(['Scenario', 'bus_label', 'type', 'obj_label', 'datetime'],
                       inplace=True)

    # set colors
    colors = {}
    components = main_df.index.get_level_values('obj_label').unique()
    colors['components'] = dict(zip(components,
                             sns.color_palette("coolwarm_r", len(components))))
    colors['scenarios'] = dict(zip(scenarios,
                          sns.color_palette("muted", len(components))))
    return main_df, scenarios, colors

