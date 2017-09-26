from __future__ import print_function
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

class tRNN(nn.Module):
    """
    tree-shaped recurrent neural network
    """

    def __init__(self, vocab, rels, word_dim, cpr_dim):
        super().__init__()
        self.word_dim = word_dim # dimensionality of word embeddings
        self.cpr_dim = cpr_dim # output dimensionality of comparison layer
        self.num_rels = len(rels) # number of relations (labels)
        self.voc_size = len(vocab)

        # vocabulary matrix
        self.voc = nn.Linear(self.voc_size, self.word_dim)

        # composition matrix
        self.cps = nn.Linear(2 * self.word_dim, self.word_dim)

        # comparison matrix
        self.cpr = nn.Linear(2 * self.word_dim, self.cpr_dim)

        # matrix to softmax layer
        self.sm = nn.Linear(self.cpr_dim, self.num_rels)

        self.word_dict = {}
        for word in vocab:
            # create one-hot encodings for words in vocabulary
            self.word_dict[word] = Variable(torch.zeros(self.voc_size))
            self.word_dict[word][vocab.index(word)] = 1

        # activation functions
        self.relu = nn.LeakyReLU() # cpr layer, negative slope is 0.01, which is standard
        self.tanh = nn.Tanh() # cps layers

    def forward(self, inputs):
        """

        :param inputs: list of lists of form [left_tree, right_tree], to support minibatch of size > 1
        :return: outputs, tensor of dimensions batch_size x num_classes
        """

        # handles multiple inputs, inserted as list
        outputs = Variable(torch.rand(len(inputs), self.num_rels))

        for idx, input in enumerate(inputs):

            left = input[0]
            right = input[1]
            left_cps = self.compose(left)
            right_cps = self.compose(right)
            apply_cpr = self.cpr(torch.cat((left_cps, right_cps)))
            activated_cpr = self.relu(apply_cpr)
            to_softmax = self.sm(activated_cpr).view(1, self.num_rels)
            output = F.softmax(to_softmax)
            outputs[idx,:] = output

        return(outputs) # size batch_size x num_classes


    def compose(self, tree):
        if tree.label() == '.': # leaf nodes
            word_onehot = self.word_dict[tree[0]]
            return self.voc(word_onehot) # get word embedding
        else:
            cps = self.cps(torch.cat((self.compose(tree[0]), self.compose(tree[1]))))
            activated_cps = self.tanh(cps)
            return activated_cps

