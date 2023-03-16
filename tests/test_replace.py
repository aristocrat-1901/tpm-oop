import io
import pytest
from module import Replace


@pytest.mark.parametrize("line,enc",
                         [('abcdef', '987654'), ('It is secret message', '1q 1r r57s5q x5rr935')])
def test_read_from(line, enc):
    obj = Replace()
    obj.read_from(line)

    assert obj.encrypt_line == enc


@pytest.mark.parametrize("enc_line",
                         ['987654', '1q 1r r57s5q x5rr935'])
def test_write_to(enc_line):
    obj = Replace()
    obj.encrypt_line = enc_line
    output = io.StringIO()
    obj.write_to(output)
    output.seek(0)
    test_output = io.StringIO(f'Encrypt message: {enc_line}\n')
    
    assert output.read() == test_output.read()
