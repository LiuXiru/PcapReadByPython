import os.path
import re
import numpy as np
from sklearn.preprocessing import Imputer


# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s\%s' % (filepath, allDir))
        if os.path.isfile(child):
            readFile(child)
            #             print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
            continue
        eachFile(child)


# 遍历出结果 返回文件的名字
def readFile(filenames):
    a = filenames.split('\\')
    b = a[1].split('_')
    rownum = 1
    with open(filenames, 'r') as fopen:
        while rownum < 2:
            fopen.readline()
            rownum = rownum + 1
        for line in fopen.readlines():
            # if rownum < 3:
            raw = line.split(',')
            row = raw[5:]
            row.pop(1)
            rownum = rownum + 1
            row[-1] = str(strings_to_numbers(b[0]))
            mylist.append(row)
            # mydata = np.array(mylist, dtype=float)

    # fopen = open(filenames, 'r')  # r 代表read
    # fileread = fopen.read()
    # fopen.close()
    # t = re.search(r'Timestamp', fileread)
    # if t:
    #     arr.append(filenames)


def z_ScoreNormalization(x, mu, sigma):
    if sigma != 0:
        x = (x - mu) / sigma
    return x


def MaxMinNormalization(x, Max, Min):
    if Max > Min:
        x = (x - Min) / (Max - Min)
    return x


def strings_to_numbers(argument):
    switcher = {
        'BROWSING': 0,
        'MAIL': 1,
        'CHAT': 2,
        'AUDIO': 3,
        'VIDEO': 4,
        'FILE-TRANSFER': 5,
        'VOIP': 6,
        'P2P': 7
    }
    return switcher.get(argument, "nothing")


if __name__ == "__main__":
    w = open('Torcsv/nonTor_120s_Layer2.csv', 'w')
    # w = open('Torcsv/Tor_120s_Layer2_tidy_train.csv', 'w')
    # wt = open('Torcsv/Tor_120s_Layer2_tidy_test.csv', 'w')
    filenames = 'Torcsv/TidyByPython'  # refer root dir
    mylist = []
    count = 0
    rownum = 0
    eachFile(filenames)
    mydata = np.array(mylist, dtype=float)
    print(mydata.shape)
    # for j in mydata:
    #     print(rownum)
    #     if j[2] <= 10 and j[3] <= 10:
    #         mydata = np.delete(mydata, rownum, axis=0)
    #         rownum = rownum - 1
    #     rownum = rownum + 1
    # print(mydata.shape)
    mydata = Imputer().fit_transform(mydata)
    print(mydata.shape)
    for i in range(len(mydata[0]) - 1):
        col = mydata[:, i]
        ave = np.average(col)
        std = np.std(col)
        maxnum = np.max(col)
        minnum = np.min(col)
        for x in range(len(col)):
            # col[x] = z_ScoreNormalization(col[x], ave, std)
            col[x] = MaxMinNormalization(col[x], maxnum, minnum)
    for row in mydata:
        count = count + 1
        # if count % 10 == 0:
        #     for i in range(77):
        #         wt.write(str(row[i]))
        #         wt.write(',')
        #     wt.write(str(int(row[-1])))
        #     wt.write('\n')
        # else:
        for i in range(len(mydata[0]) - 1):
            w.write(str(row[i]))
            w.write(',')
        w.write(str(int(row[-1])))
        w.write('\n')
    w.close()
    # wt.close()
