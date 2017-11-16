import torch
from trnn import tRNN
from trntn import tRNTN
from sumnn import sumNN
import datamanager as dat
from test import compute_accuracy
#from visualize import confusion_matrix

vocab = ['Europeans', 'Germans', 'Italians', 'Romans', 'all', 'children', 'fear', 'hate', 'like', 'love', 'not', 'some']
#vocab = ['Europeans', 'Germans', 'Italians', 'Romans', 'all', 'children', 'fear', 'hate', 'like', 'love', 'not', 'some', 'two']
rels = ['#', '<', '=', '>', '^', 'v', '|']
#rels = ['#', '<', '=', '>', '|']
word_dim = 25
cpr_dim = 75
bound_layers = None
bound_embeddings = None

# to load model:
# trnn_det1 = tRNN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
# trnn_det1.load_state_dict(torch.load('models/trnn/tRNNbinary1_neg_det1_train.pt'))
#
# trnn_verb = tRNN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
# trnn_verb.load_state_dict(torch.load('models/trnn/tRNNbinary1_neg_verbtrain.pt'))
#
# trntn_det1 = tRNTN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
# trntn_det1.load_state_dict(torch.load('models/trntn/tRNTNbinary1_neg_det1_train.pt'))
#
# trntn_verb = tRNTN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
# trntn_verb.load_state_dict(torch.load('models/trntn/tRNTNbinary1_neg_verb_train.pt'))
#

# sumnn_det1 = sumNN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
# sumnn_det1.load_state_dict(torch.load('models/sumnn/sumNNbinary1_neg_verb_train.pt'))

# sumnn_verb = sumNN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
# sumnn_verb.load_state_dict(torch.load('models/sumnn/sumNNbinary1_neg_verb_train.pt'))

sumnn = sumNN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
sumnn.load_state_dict(torch.load('models/sumnn/sumNNbinary_2dets_4negs_train.pt'))


trnn = tRNN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
trnn.load_state_dict(torch.load('models/trnn/tRNNbinary_2dets_4negs_train.pt'))


trntn = tRNTN(vocab, rels, word_dim=word_dim, cpr_dim=cpr_dim,bound_layers=bound_layers, bound_embeddings=bound_embeddings)
trntn.load_state_dict(torch.load('models/trntn/tRNTNbinary_2dets_4negs_train.pt'))

test_data_file = '/Users/Mathijs/Documents/School/MoL/thesis/thesis_code/data/binary/2dets_4negs/binary_2dets_4negs_test.txt'
test_data = dat.SentencePairsDataset(test_data_file)
test_data.load_data()

for net in [sumnn,trnn,trntn]:
    final_acc = compute_accuracy(test_data, rels, net, print_outputs=False, confusion_matrix=True)
    print(final_acc)

