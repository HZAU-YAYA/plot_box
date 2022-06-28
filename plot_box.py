#!/usr/bin/env python3
#-*- encoding=UTF-8 -*-
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import sys
import logging

LOG = logging.getLogger(__name__)
__version__ = "1.0.0"    #设置版本信息
__author__ = ("Boya Xu",)   #输入作者信息
__email__ = "xby@bioyigene.com"
__all__ = []
def add_help_args(parser): #帮助函数
    parser.add_argument('--sf',  default="", type=str, help='sf file')
    parser.add_argument('--tsv',  default="", type=str, help='tsv file')
    parser.add_argument('--out', '-o', type=str, default="", help="out put file")
    return parser
# sf = r"C:\Users\徐博雅\Desktop\物种丰度\species.2-sample_t-test.tsv"
# tsv = r"C:\Users\徐博雅\Desktop\物种丰度\species_lefse.tsv"
# fout = r"C:\Users\徐博雅\Desktop\物种丰度\out.tsv"
def run_fout(tsv, sf, out):
    #生成两个文件相匹配的out文件
    fin1 = open(tsv, "r")
    fin2 = open(sf, "r")
    fout = open(out, "w")
    n = 0
    a = 0
    dic = {}
    for i in fin2:
        if n == 0:
            n += 1
        else:
            s = i.strip().split("\t")
            dic[s[0]] = []
    for i in fin1:
        if a == 0:
            a += 1
            num = len(i.split("\t"))
            fout.write(i)
        s = i.split("\t")
        if s[0] in dic:
            fout.write(s[0]+"\t"+"\t".join(s[1:num]))


def group_name(file):
    #获取所有组名
    out = open(file, "r")
    n = 0
    dic = []
    s = []
    for i in out:
        if n == 0:
            n += 1
            s = i.strip().split("\t")
        else:
            break
    for i in s:
        if not i in dic:
            dic.append(i)
    group = dic[1:]
    return group


def group_all(out):
    #获取丰度文件离所有组名的列号
    file = open(out, "r")
    group = group_name(out)
    n = 0
    dic = {}
    for a in file:
        if n == 0:
            n += 1
            s = a.strip().split("\t")
            for b in group:
                dic[b] = [i for i, x in enumerate(s) if x == "{}".format(b)]
            return dic


def tiqu_1(file):
    #提取格式
    #组名：{种名：对应值}
    dic = group_all(file)
    eic = {}
    name = group_name(file)
    for b in name:
        fic = {}
        f = open(file, "r")
        n = 0
        for i in f:
            if n == 0:
                n += 1
            else:
                s = i.strip().split("\t")
                s[0] = s[0].replace(' ', '_')
                fic[s[0]] = []
                for c in dic[b]:
                    #if len(fic[s[0]]) < l:
                    fic[s[0]].append(s[c])
        eic[b] = fic
        f.close()
    #del eic['']
    return eic

def hangname(file):
    f = open(file, 'r')
    n = 0
    a = []
    for i in f:
        if n == 0:
            n = n+1
        else:
            s = i.strip().split("\t")
            s[0] = s[0].replace(' ', '_')
            a.append(s[0])
    f.close()
    return a
def mean(a):
    s = []
    for i in a:
        s.append(float(i/sum(a))*1000)
    return s

def tiqu(file):
    #另一种提取格式
    #组名：[组一：所有种的值].....
    dic = group_all(file)
    name = group_name(file)
    bic = {}
    for i in name:
        all = []
        bic[i] = []
        for a in dic[i]:
            s_1 = []
            n = 0
            f = open(file, 'r')
            for b in f:
                if n == 0:
                    n = n+1
                else:
                    s = b.strip().split("\t")
                    s_1.append(float(s[a]))
            f.close()
            #s_1 = mean(s_1)
            all.append(s_1)
        bic[i].append(all)
    return bic
def run(tsv, sf, out):
    run_fout(tsv, sf, out)
    p = {}
    p = tiqu(out)
    g_name = group_name(out)
    x1 = p[g_name[0]][0]
    x2 = p[g_name[1]][0]
    n = len(x1[0])
    x1 = np.array(x1)
    x2 = np.array(x2)
    x1[x1 == 0] = np.nan
    x2[x2 == 0] = np.nan
    x1 = np.log(x1)
    x2 = np.log(x2)
    fig = plt.figure(figsize=(25, 11))
    ax = plt.subplot()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #plt.rcParams["font.sans-serif"] = ["SimHei"]  # 正常显示中文标签
    #plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    bplot1 = plt.boxplot(x1, patch_artist=True, positions=[x + 1 + 0.20 for x in range(n)],
                         boxprops={'facecolor': 'lightcoral'}, vert = False)
    bplot2 = plt.boxplot(x2, patch_artist=True, positions=[x + 1 - 0.20 for x in range(n)],
                         boxprops={'facecolor': 'cornflowerblue'}, vert = False)
    #plt.grid(linestyle=":", color="red")
    #plt.title('boxplot')
    y_tick_label = hangname(out)
    plt.yticks([a + 1 for a in range(n)], y_tick_label)
    plt.legend(handles=[bplot1["boxes"][0], bplot2["boxes"][0]], labels=g_name, frameon=False)
    plt.show()
    plt.savefig("boxplot.png")
    plt.savefig("boxplot.pdf")
    
    
def main():   #主函数，执行函数
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=''' 
name:plotbox.py 
attention: .py --sf species.2-sample_t-test.tsv --tsv species_lefse.tsv --out out.tsv
version: %s
contact: %s <%s>\ 
''' % (__version__, ' '.join(__author__), __email__))
    args = add_help_args(parser).parse_args()
    run(args.tsv, args.sf, args.out)


if __name__ == "__main__":           #固定格式，使 import 到其他的 python 脚本中被调用（模块重用）执行
    main()
    
