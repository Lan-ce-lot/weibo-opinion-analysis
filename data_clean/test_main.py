from data_clean.main import delete_stopwords


def test_delete_stopwords():

    # code to test delete_stopwords function

    # test cases
    sourcedata = [['a', 'b', 'c','的'], ['d', 'e', 'f','和']]
    # dir_path = './stopwords'
    dir_path = './example'
    # expected result
    expected = [['a', 'b', 'c'], ['d', 'e', 'f']]
    # actual result
    actual = delete_stopwords(sourcedata, dir_path)
    # assert
    print(actual)
    assert actual == expected
