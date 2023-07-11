"""
    This file contains the parameters of the project.
"""
import torch

from tokenizers import get_tokenizer
from load_dataset import load_dataset
from utils import build_vocab

SRC_LANGUAGE = "fixed"  # source language
TGT_LANGUAGE = "buggy"  # target language

# Place-holders
token_transform = {}  # tokenization
vocab_transform = {}  # numericalization

token_transform[
    SRC_LANGUAGE
] = get_tokenizer  # get_tokenizer is a function that tokenizes the source code
token_transform[
    TGT_LANGUAGE
] = get_tokenizer  # get_tokenizer is a function that tokenizes the source code

# Define special symbols and indices
UNK_IDX, PAD_IDX, BOS_IDX, EOS_IDX = 0, 1, 2, 3  # indices for special tokens
# Make sure the tokens are in order of their indices to properly insert them in vocab
special_symbols = ["<unk>", "<pad>", "<bos>", "<eos>"]  # special tokens

X_train, y_train, X_val, y_val, X_test, y_test = load_dataset()

build_vocab(X_train, y_train)

SRC_VOCAB_SIZE = len(vocab_transform[SRC_LANGUAGE])  # source vocabulary size
TGT_VOCAB_SIZE = len(vocab_transform[TGT_LANGUAGE])  # target vocabulary size

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # device

text_transform = {}  # text transforms
