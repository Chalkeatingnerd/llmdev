import pytest
from authenticator import Authenticator

def test_register_success():
    """1. ユーザーが正しく登録されるかをテスト"""
    auth = Authenticator()
    auth.register("test_user", "password123")
    assert auth.users["test_user"] == "password123"

def test_register_duplicate_error():
    """2. すでに存在するユーザー名で登録した場合に例外が発生するかテスト"""
    auth = Authenticator()
    auth.register("test_user", "password123")
    
    with pytest.raises(ValueError) as excinfo:
        auth.register("test_user", "new_password")
    
    assert str(excinfo.value) == "エラー: ユーザーは既に存在します。"

def test_login_success():
    """3. 正しいユーザー名とパスワードでログインできるかをテスト"""
    auth = Authenticator()
    auth.register("user01", "pass01")
    
    result = auth.login("user01", "pass01")
    assert result == "ログイン成功"

def test_login_failure():
    """4. 誤ったパスワードでログインして例外が発生するかテスト"""
    auth = Authenticator()
    auth.register("user01", "pass01")
    
    with pytest.raises(ValueError) as excinfo:
        auth.login("user01", "wrong_pass")
    
    assert str(excinfo.value) == "エラー: ユーザー名またはパスワードが正しくありません。"