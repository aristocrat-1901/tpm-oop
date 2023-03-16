import io
import pytest
from module import Shift


@pytest.mark.parametrize("line,key, enc",
                         [('abcd', 3, 'defg'), ('hello world', 27, '85ccf nfic4')])
def test_read_from(line, key, enc):
    obj = Shift()
    obj.read_from(key, line)

    assert obj.encrypt_line == enc


@pytest.mark.parametrize("enc_line,key",
                         [('defg', 3), ('85ccf nfic4', 27)])
def test_write_to(enc_line, key):
    obj = Shift()
    obj.encrypt_line = enc_line
    obj.key = key
    output = io.StringIO()
    obj.write_to(output)
    output.seek(0)
    test_output = io.StringIO(f'Key = {key}\nEncrypt message : {enc_line}\n')

    assert output.read() == test_output.read()
