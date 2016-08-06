from vim_matlab import python_vim_utils

def strip_comments(line):
    pattern = python_vim_utils.PythonVimUtils.comment_pattern
    return pattern.sub(r"\1", line).strip()

def test_comment_pattern():
    assert "hello" == strip_comments("hello")
    assert "hello" == strip_comments("hello %")
    assert "hello" == strip_comments("hello %%")
    assert "disp('%')" == strip_comments("disp('%') % ")
    assert "disp('%')" == strip_comments("disp('%')")
    assert "disp('')" == strip_comments("disp('')")
    assert "disp('')" == strip_comments("disp('')% ")
    assert "disp('')" == strip_comments("disp('') % ")
    assert "disp('')" == strip_comments("disp('') %%")
    assert "disp('%');disp('%')" == strip_comments("disp('%');disp('%')%disp('')")
    assert "A = sqrtm(B) \ C.';" == strip_comments("A = sqrtm(B) \ C.'; % foo")
    assert "disp('100%');A = sqrtm(B) \ C.';" == strip_comments("disp('100%');A = sqrtm(B) \ C.';% foo")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% '")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% ''")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% '''")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% '.''")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% ' '")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% ' ' %")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% ' %' ")
    assert "disp('%');C.'" == strip_comments("disp('%');C.'% ' %' %")
    assert "disp('% ''');C.';" == strip_comments("disp('% ''');C.'; % ' %' %")
    assert "disp('% .''');C.';" == strip_comments("disp('% .''');C.'; % ' %' %")
