def test_uppercase():
    assert "foo".upper() == "FOO"


def test_reversed():
    assert list(reversed([1, 2, 3])) == [3, 2, 1]


def test_some_primes():
    assert 37 in {
        num
        for num in range(2, 50)
        if not any(num % i == 0 for i in range(2, num))
    }