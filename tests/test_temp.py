import temp


def test_temp(capsys):
    input_values = [2, 3]

    def mock_input(s):
        print(s, end='')
        return input_values.pop(0)

    temp.input = mock_input

    temp.main()

    out, err = capsys.readouterr()

    assert out == "".join([
        'First: ',
        'Second: ',
        'The result is 5\n',
    ])

    assert err == ''