from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn import metrics
from diagnostic_datamanager import DiagnosticDataFile
import numpy as np
from collections import Counter, defaultdict
import pickle
from random import shuffle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import torch
from rnn import RNN

def load_model(model_path):
    #model_path = 'linreg_length.pkl'
    diag_classifier_pkl = open(model_path, 'rb')
    diag_classifier = pickle.load(diag_classifier_pkl)
    return(diag_classifier)

def data_distribution(data):
    labels = [item[0].numpy()[0] for item in data]
    total = len(labels)
    counter = Counter(labels)
    counter_normalized = {label : counter[label] / total for label in counter.keys()}
    counter_out = {label : "%.2f" % round(counter_normalized[label], 2) for label in counter_normalized.keys()}
    return(counter_out)

def compute_mse(hypotheses, predictions):
    mse = metrics.mean_squared_error(hypotheses, predictions)
    return (mse)

def compute_mae(hypotheses, predictions):
    mae = metrics.mean_absolute_error(hypotheses, predictions)
    return(mae)

def compute_acc(hypotheses, predictions):
    # possibly also consider precision/recall/f1

    # for continuous outputs:
    # train_hyps = np.array([item[0].float().numpy() for item in train_data]).ravel()

    try:
        acc = metrics.accuracy_score(hypotheses, predictions)
    except:
        # round predictions
        pred_rounded = np.rint(predictions)
        acc = metrics.accuracy_score(hypotheses, pred_rounded)
    return (acc)

def plot_predictions(hypotheses, predictions, title, show_boxplot=True, show_violinplot=False, show_confmatrix=False):
    #plt.scatter(hypotheses, predictions, s=1, color='black')
    plt.plot(hypotheses, hypotheses, color='blue', linewidth=2)

    if show_boxplot or show_violinplot:
        box_data = defaultdict(list)

        for idx in range(len(hypotheses) - 1):
            true = hypotheses[idx]
            pred = predictions[idx]
            box_data[true] += [pred]

        box_data = dict(box_data)
        data = [np.array(preds) for preds in box_data.values()]
        pos = [np.array(position) for position in box_data.keys()]

        if show_boxplot:
            plt.boxplot(data, positions=pos, showfliers=False)
            title += 'box'
        if show_violinplot:
            plt.violinplot(data,
                   showmeans=False,
                   showmedians=True)
            title += 'violin'

    if show_confmatrix:
        # for pos tags:
        #pos_labels = ['bracket', 'noun', 'verb', 'quant', 'neg']



        # print(hypotheses)
        # print(predictions)
        conf = metrics.confusion_matrix(hypotheses, predictions)#, labels=pos_labels)
        # normalize
        conf = conf.astype('float') / conf.sum(axis=1)[:, np.newaxis]
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # cax = ax.matshow(confusion.numpy(), cmap='hot')
        cax = ax.matshow(conf, cmap='hot')

        fig.colorbar(cax)

        # Set up axes
        # ax.set_xticklabels([''] + rels, rotation=90)
        #ax.set_xticklabels([''] + pos_labels)
        #ax.set_yticklabels([''] + pos_labels)

        # Force label at every tick
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        title = 'Confusion ' + title

        #plot_name = 'conf_' + net.__class__.__name__

        #plt.savefig(plot_name)

    plt.xticks()
    plt.yticks()
    plt.title(title)

    plt.savefig(title)
    plt.close()

def train(train_data, classifier, hypothesis, print_train_distribution=False, plot_pred=True):

    if print_train_distribution:
        print('Train distribution:')
        print(data_distribution(train_data))

    if classifier == 'logreg':
        diag_classifier = LogisticRegression()
        # diag_classifier = LogisticRegression(class_weight='balanced',verbose=0)
    elif classifier == 'linreg':
        diag_classifier = LinearRegression()

    train_hiddens = np.array([item[1].numpy() for item in train_data])
    train_hyps = np.array([item[0].numpy() for item in train_data]).ravel()

    diag_classifier.fit(train_hiddens, train_hyps)

    train_pred = diag_classifier.predict(train_hiddens)

    print('Training MSE score:')
    print(compute_mse(train_hyps, train_pred))
    print('Training MAE score:')
    print(compute_mae(train_hyps, train_pred))

    plot_name = 'Training results ' + hypothesis
    if plot_pred:
        plot_predictions(train_hyps, train_pred, plot_name)

    # save model

    model_path = classifier + '_' + hypothesis + '.pkl'
    model_pkl = open(model_path, 'wb')
    pickle.dump(diag_classifier, model_pkl)
    model_pkl.close()
    return(diag_classifier)

def test(test_data, diag_classifier, hypothesis, plot=True):

    # test
    test_hiddens = np.array([item[1].numpy() for item in test_data])
    test_hyps = np.array([item[0].numpy() for item in test_data]).ravel()
    test_pred = diag_classifier.predict(test_hiddens)

    print('Test distribution:')
    print(data_distribution(test_data))

    print('Testing MSE score:')
    print(compute_mse(test_hyps, test_pred))
    print('Testing MAE score:')
    print(compute_mae(test_hyps, test_pred))

    plot_name = 'Testing results ' + hypothesis
    if plot:
        plot_predictions(test_hyps, test_pred, plot_name)

if False:
    data_file = '/Users/mathijs/Documents/Studie/MoL/thesis/mol_thesis/diagnose/data/diagnostic_gru_2dets4negs_brackets.txt'
    #data_file = '/Users/mathijs/Documents/Studie/MoL/thesis/mol_thesis/diagnose/data/diagnostic_gru_2dets4negs_pos.txt'
    #data_file = '/Users/mathijs/Documents/Studie/MoL/thesis/mol_thesis/diagnose/data/length_small.txt'

    d = DiagnosticDataFile(data_file)
    train_data, test_data = d.split(0.8)
    print(str(len(train_data)) + ' train instances')
    print(str(len(test_data)) + ' test instances')
    hypothesis = 'brackets'
    classifier = train(train_data, 'logreg', hypothesis)
    #classifier = load_model('logreg_brackets.pkl')
    test(test_data, classifier, hypothesis)



    exit()

    vocab = ['(', ')', 'Europeans', 'Germans', 'Italians', 'Romans', 'all', 'children', 'fear', 'hate', 'like',
                 'love', 'not', 'some']
    rels = ['#', '<', '=', '>', '^', 'v', '|']

    word_dim = 25
    n_hidden = 128
    cpr_dim = 75

    model_path = '/Users/mathijs/Documents/Studie/MoL/thesis/mol_thesis/models/rnns/gru/GRUbinary_2dets_4negs_train_ada_nodrop_3.pt'
    net = RNN('GRU', vocab, rels, word_dim, n_hidden, cpr_dim)
    net.load_state_dict(torch.load(model_path))

    sentences = ['( ( some Italians  ) ( ( not love ) ( some Romans ) ) )','( ( all Europeans  ) ( ( not love ) ( all ( not Italians ) ) ) )',
                 '( ( all ( not Germans )  ) ( love ( some Europeans ) ) )', '( ( ( not all ) ( not Europeans )  ) ( love ( some Europeans ) ) )',
                '( ( some Europeans  ) ( ( not hate ) ( all Europeans ) ) )', '( ( ( not all ) Romans  ) ( love ( some Romans ) ) ) ']

    for sentence in sentences:
        s = [sentence.split()]
        print(s)

        _, hidden_vectors = net.rnn_forward(s, 1, hypothesis='length')

        test_hiddens = np.array(hidden_vectors[0])
        hyps = np.array([i for i in range(len(test_hiddens))])
        y_pred = diag_classifier.predict(test_hiddens)

        print('MAE:')
        print(compute_mae(hyps, y_pred))