import pandas as pd
import matplotlib.pyplot as plt


dtype = {'timept': int, 'category': str, 'freeze': bool, 'utime': int, 
         'stime': int, 'cutime': int, 'cstime': int, 'min_flt': int,
         'maj_flt': int, 'cmin_flt': int, 'cmaj_flt': int, 'vsz': int,
         'rss': int, 'gen0': int, 'gen1': int, 'gen2': int, 'perm_count': int}


# rss/vsz (box plot)
def plot_memory_usage(title='Memory Usage (rss/vsz)', ylabel='VSZ'):
    df = pd.read_csv('../Py310/reduction.csv', dtype=dtype, converters={'freeze': lambda x: x == 'True'})

    y1 = df[(df['freeze'] == False) & (df['timept'] == 0)].loc[:, 'rss']
    y2 = df[(df['freeze'] == True) & (df['timept'] == 0)].loc[:, 'rss']


    plt.boxplot([y1, y2])
    plt.xticks([1, 2], ['w/o freeze', 'w/ freeze'])
    plt.title = title
    plt.ylabel = ylabel
    plt.show()


# faults 
def plot_memory_faults(x, y):
    return


# utime/stime 
def plot_exec_time(x, y):
    return



if __name__ == "__main__":

    plot_memory_usage(ylabel='RSS')

