__author__ = 'Haohan Wang'

import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve,auc

from matplotlib import pyplot as plt
import matplotlib
model='group'
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 18}

matplotlib.rc('font', **font)

modelNum = 5
colors = ['b', 'r','g','c','b']#'b', 'b','r','g', 'm', 'm', 'm','m','g','c','c', 'c', 'c', 'c','g']
modelNames = ['lmmn-g','lmm-g','group','lmmn-lasso','lmmm-lasso']#'TrSLMM-SCAD', 'TrSLMM-MCP', 'TrSLMM-Lasso','TrSLMM-t','TrSLMM-g',  'SLMM-SCAD', 'SLMM-MCP', 'SLMM-Lasso','SLMM-T','SLMM-G', 'SCAD', 'MCP','Lasso','tree','group']
style = ['-', '-', '-','-','--']

def rescale(x):
    maxi = np.max(np.abs(x))
    if maxi == 0:
        return x
    return x/maxi

def roc(beta, beta_true):
    beta = beta.flatten()
    beta = abs(beta)
    beta = rescale(beta)
    beta_true[beta_true != 0] = 1
    beta_true = beta_true.flatten()
    fpr, tpr, f = roc_curve(beta_true, beta)
    fp_prc, tp_prc, f_prc=precision_recall_curve(beta_true,beta)
    roc_auc = auc(fpr, tpr)
    return roc_auc,fp_prc,tp_prc,fpr,tpr

def loadResult(n, p, d, g, sig, sigC,k,str1,we, g_num,seedNum):
    L = []
    P = [[] for i in range(modelNum)]
    B = [[] for i in range(modelNum)]

    for seed in range(seedNum):
        if model == 'tree':
            fileHead = '../result/synthetic/tree/'
        else:
            fileHead = '../result/synthetic/group/'
        if str1=='2':
            fileHead = fileHead + '2_'+str(n) + '_' + str(p) + '_' + str(g) + '_' + str(d) + '_' + str(k) + '_' + str(sig) + '_' + str(sigC) + '_' +str(we)+'_'+str(g_num)+ '_'+str(seed) + '_'
        elif str1=='3':

            fileHead = fileHead + '3_'+str(n) + '_' + str(p) + '_' + str(g) + '_' + str(d) + '_' + str(k) + '_' + str(sig) + '_' + str(sigC) + '_' +str(we)+'_'+str(g_num)+ '_'+str(seed) + '_'
        else:
            fileHead = fileHead + 'n_'+str(n) + '_' + str(p) + '_' + str(g) + '_' + str(d) + '_' + str(k) + '_' + str(sig) + '_' + str(sigC) + '_' +str(we)+'_'+str(g_num)+ '_'+str(seed) + '_'
        #causal = np.load('../result/synthetic/causal' + pathTail)
        print fileHead
        label= np.load(fileHead + 'beta1.npy')
        results = np.load(fileHead + 'beta2.npy')
        #[N, p] = results.shape
        # label = np.zeros(p)
        # for (i, effect) in causal:
        #     label[i.astype(int)] = 1
        # L.extend(label)
        # print label.shape
        # print results.shape
        #label[label!=0] = 1
        L.extend(label.flatten())
        for i in range(5):
            beta = results[i].flatten()#[i, :]
            predict = np.zeros_like(beta)
            predict[beta != 0] = 1
            B[i].extend(beta.tolist())
            P[i].extend(predict.tolist())
    return L, P, B

def evaluation(L, R):
    a = np.array(L)
    b = np.array(R)
    # print  np.max(np.abs(a)),'s'
    # print  np.max(np.abs(b)),'m'
    # if np.max(np.abs(a))==0:
    #     pass
    # else:
    #     a = a/np.max(np.abs(a))
    # if np.max(np.abs(b))==0:
    #     pass
    # else:
    #     b = a/np.max(np.abs(b))

    return np.mean(np.square(np.abs(a-b)))

# def evaluation(L, R):
#     fpr, tpr, t = roc_curve(L, R)
#     return fpr, tpr, t
#     # p, r, t = precision_recall_curve(L, R)
#     # return r, p, t


def evaluationScore(L, R):
    return roc_auc_score(L, R)


def visualize(cat,str1):
    n = 100
    p = 500
    d = 0.05
    g = 10
    k = 50
    sig = 0.001
    sigC=0.1
    we=0.05
    g_num = 3

    if cat == 'n':
        valueList = [50 ,100,500]#[100, 500, 1000, 2000, 5000][1:4]
        name = 'n'
    elif cat == 'p':
        valueList = [200,500,800]#[1000, 2000, 5000, 10000, 20000][1:4]
        name = 'p'
    elif cat=='k':
        valueList = [20,50,100]
        name = 'k'
    elif cat == 'd':
        valueList = [0.03,0.05, 0.06]#[0.005, 0.01, 0.05, 0.1, 0.5][1:4]
        name = 'd'
    elif cat == 'g':
        valueList =[ 5,10, 20]# [2, 5, 10, 20, 50][1:4]
        name = 'G'
    elif cat=='gn':
        valueList= [ 2,3,5]
        name='gn'
    elif cat == 's':
        valueList = [0.0005, 0.001, 0.01]#[0.01, 0.05, 0.1, 0.5, 1][1:4]
        name = r'$\sigma_e$'
    elif cat=='c':
        valueList = [0.05, 0.1,1]#[0.1, 0.5, 1, 5, 10][1:4]
        name = r'$\sigma_r$'
    elif cat=='we':
        valueList =[0.01 , 0.05,0.1]
        name='we'
    if cat == 'n':
        fig = plt.figure(dpi=100, figsize=(20, 8))
    else:
        fig = plt.figure(dpi=100, figsize=(20, 5))
    #axs = [0 for i in range(3)]
    error_matrix=np.zeros((len(valueList),5))
    for i in range(3):
        # if cat == 'n':
        #     #axs[i] = fig.add_axes([0.05 + (i) * 0.32, 0.12, 0.30, 0.5])
        #     axs[i] = fig.add_axes([0.05 + (i) * 0.18, 0.12, 0.15, 0.5])
        # else:
        #     #axs[i] = fig.add_axes([0.05 + (i) * 0.32, 0.12, 0.30, 0.8])
        #     axs[i] = fig.add_axes([0.05 + (i) * 0.18, 0.12, 0.15, 0.8])
        if cat == 'n':
            n = valueList[i]
            v = valueList[i]
        elif cat == 'p':
            p = valueList[i]
            v = valueList[i]
        elif cat == 'd':
            d = valueList[i]
            v = valueList[i]
        elif cat == 'g':
            g = valueList[i]
            v = valueList[i]
        elif cat == 's':
            sig = valueList[i]
            v = valueList[i]
        elif cat=='c':
            sigC = valueList[i]
            v = valueList[i]
        elif cat=='k':
            k= valueList[i]
            v = valueList[i]
        elif cat=='gn':
            g_num=valueList[i]
            v = valueList[i]
        elif cat=='we':
            we=valueList[i]
            v = valueList[i]


        L, P, B = loadResult(n, p, d, g, sig, sigC, k,str1,we,g_num,5)
    #     for j in range(modelNum):
    #         s,fp_prc,tp_prc,fpr,tpr = roc(np.array(B[j]),np.array( L))
    #         print modelNames[j],":",s
    #         axs[i].plot(fpr, tpr, color=colors[j], label=modelNames[j], ls=style[j])
    #         if i!=0:
    #             axs[i].get_yaxis().set_visible(False)
    #     axs[i].title.set_text(name + ' = ' + str(v))
    #     axs[i].set_xlabel('FPR')
    #     axs[i].set_xlim(-0.01,1.01)
    #     axs[i].set_ylim(-0.01,1.01)
    #     print "--------------"
    # axs[0].set_ylabel('TPR')
    # if cat == 'n':
    #     plt.legend(loc='upper center', bbox_to_anchor=(-0.6, 1.7),
    #                ncol=3, fancybox=True, shadow=True)
    # plt.savefig('./pic/'+str1+'_'+cat+"_beta_error.png")
    # plt.show()
        for j in range(modelNum):
            print modelNames[j], evaluation(L, B[j])
            error_matrix[i,j]=evaluation(L, B[j])
    plt.figure(facecolor=(1, 1, 1))
    x = [i for i in range(len(valueList))]

    labels= valueList
    # if cat=='p':
    #     plt.ylim([0.001, 10])
    # else:
    plt.ylim([1e-4, 1e9])
    for i in range(5):
        plt.semilogy(x, error_matrix[:,i], color=colors[i], label=modelNames[i], ls=style[i])
    # line, = plt.plot([1,5,2,4], '-')
    # line.set_dashes([8, 4, 2, 4, 2, 4])
    plt.xticks(x, labels, rotation='vertical')
    plt.margins(0.2)
    # plt.legend(loc='lower right')
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel(cat+' number')
    plt.ylabel('Mean of Error')
    plt.savefig('./pic/'+str1+'_'+cat+"_beta_error.png")
    # plt.show()


if __name__ == '__main__':
    str1='3'
    cat = 'n'
    visualize(cat,str1)
    print "============",cat
    cat = 'p'
    visualize(cat,str1)
    print "============",cat
    cat = 'k'
    visualize(cat,str1)
    print "============",cat
    cat = 'g'
    visualize(cat,str1)
    print "============",cat
    cat = 'gn'
    visualize(cat,str1)
    print "============",cat
    cat = 'we'
    visualize(cat,str1)
    print "============",cat
    cat = 's'
    visualize(cat,str1)
    print "============",cat
    cat = 'c'
    visualize(cat,str1)
    print "============",cat

    str1='2'
    cat='n'
    visualize(cat,str1)
    print "============",cat
    cat = 'p'
    visualize(cat,str1)
    print "============",cat
    cat = 'k'
    visualize(cat,str1)
    print "============",cat
    cat = 'g'
    visualize(cat,str1)
    print "============",cat
    cat = 'gn'
    visualize(cat,str1)
    print "============",cat
    cat = 'we'
    visualize(cat,str1)
    print "============",cat
    cat = 's'
    visualize(cat,str1)
    print "============",cat
    cat = 'c'
    visualize(cat,str1)
    print "============",cat

    str1='n'
    cat = 'n'
    visualize(cat,str1)
    print "============",cat
    cat = 'p'
    visualize(cat,str1)
    print "============",cat
    cat = 'k'
    visualize(cat,str1)
    print "============",cat
    cat = 'g'
    visualize(cat,str1)
    print "============",cat
    cat = 'gn'
    visualize(cat,str1)
    print "============",cat
    cat = 'we'
    visualize(cat,str1)
    print "============",cat
    cat = 's'
    visualize(cat,str1)
    print "============",cat
    cat = 'c'
    visualize(cat,str1)
    print "============",cat

