# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def train(train_data):
    """
    INPUT
        train_data; n-length list of k-length lists,
            where the ith element of the jth list is the ith keystroke measurement of the jth password entry
    OUTPUT
        centroid; the Euclidean centroid of the train_data
        mean; mean of the log of the Euclidean norms between training data and centroid
        std; standard deviation of the log of the Euclidean norms between training data and centroid
    """

