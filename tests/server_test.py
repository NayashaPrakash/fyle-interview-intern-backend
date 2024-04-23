import pytest
from marshmallow.exceptions import ValidationError

from core import app
from core.libs.exceptions import FyleError
from core.server import handle_error
from core.libs.assertions import base_assert, assert_auth, assert_true, assert_valid, assert_found

# Test for assertions.py

def test_base_assert():
    error_code = 500
    message = "Internal Server Error"
    with pytest.raises(FyleError) as exc_info:
        base_assert(error_code, message)
    assert exc_info.value.status_code == error_code
    assert exc_info.value.message == message

def test_assert_auth():
    with pytest.raises(FyleError) as exc_info:
        assert_auth(False)
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "UNAUTHORIZED"

    # No exception should be raised when condition is True
    try:
        assert_auth(True)
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly!")

def test_assert_true():
    with pytest.raises(FyleError) as exc_info:
        assert_true(False)
    assert exc_info.value.status_code == 403
    assert exc_info.value.message == "FORBIDDEN"

    # Test that no exception is raised when condition is True
    try:
        assert_true(True)
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly!")

def test_assert_valid():
    with pytest.raises(FyleError) as exc_info:
        assert_valid(False)
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "BAD_REQUEST"

    # Test that no exception is raised when condition is True
    try:
        assert_valid(True)
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly!")

def test_assert_found():
    with pytest.raises(FyleError) as exc_info:
        assert_found(None)
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "NOT_FOUND"

    # Test that no exception is raised when object is not None
    try:
        assert_found("object")
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly!")

# Test for server.py

def test_ready_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'
    assert 'time' in response.json

def test_handle_fyle_error(client):
    with app.test_request_context():
        # Correct the order of arguments passed to FyleError
        err = FyleError(status_code=404, message="Test error")
        response_body, response_status = handle_error(err)
        assert response_status == 404
        assert response_body.json == {'error': 'FyleError', 'message': 'Test error'}


def test_handle_validation_error(client):
    with app.test_request_context():
        err = ValidationError({'field': 'Invalid data'})
        response_body, response_status = handle_error(err)
        
        assert response_status == 400
        assert response_body.json == {'error': 'ValidationError', 'message': {'field': 'Invalid data'}}


def test_handle_integrity_error(client):
    with app.test_request_context():
        from sqlalchemy.exc import IntegrityError
        
        err = IntegrityError("Duplicate entry", params="dummy", orig=Exception("Unique constraint failed"))
        response_body, response_status = handle_error(err)
        
        assert response_status == 400
        assert response_body.json == {'error': 'IntegrityError', 'message': 'Unique constraint failed'}

def test_fyle_error_initialization():
    """Test that FyleError initializes correctly with a status code and message."""
    status_code = 404
    message = "Not Found"
    error = FyleError(status_code, message)
    
    assert error.message == message, "FyleError message does not match the initialization parameter."
    assert error.status_code == status_code, "FyleError status code does not match the initialization parameter."

def test_fyle_error_to_dict():
    """Test that the to_dict method returns the correct dictionary representation."""
    status_code = 500
    message = "Internal Server Error"
    error = FyleError(status_code, message)
    
    expected_dict = {'message': message}
    assert error.to_dict() == expected_dict, "to_dict method does not return the correct dictionary."
    