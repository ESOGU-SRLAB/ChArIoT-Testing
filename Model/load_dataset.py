def load_dataset():
    X_train = open('data/train/fixed.txt', 'r').read().splitlines()
    y_train = open('data/train/buggy.txt', 'r').read().splitlines()
    X_val = open('data/val/fixed.txt', 'r').read().splitlines()
    y_val = open('data/val/buggy.txt', 'r').read().splitlines()
    X_test = open('data/test/fixed.txt', 'r').read().splitlines()
    y_test = open('data/test/buggy.txt', 'r').read().splitlines()
    
    return X_train, y_train, X_val, y_val, X_test, y_test