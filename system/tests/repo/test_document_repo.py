import pytest
from unittest.mock import Mock, patch
from model.document_model import Document, DocumentStatus, DocumentComment
from repo.document_repo import DocumentRepository

@pytest.fixture
def mock_db_session():
    with patch('model.base_model.db.session') as mock:
        yield mock

@pytest.fixture
def document_repo():
    return DocumentRepository()

def test_create_document(mock_db_session, document_repo):
    # Setup
    document = Document()

    # Execute
    result = document_repo.create_document(document)

    # Assert
    mock_db_session.add.assert_called_once_with(document)
    mock_db_session.commit.assert_called_once()
    assert result is document

def test_update_document(mock_db_session, document_repo):
    # Setup
    document = Document()

    # Execute
    document_repo.update_document(document)

    # Assert
    mock_db_session.commit.assert_called_once()

def test_delete_document(mock_db_session, document_repo):
    # Setup
    document = Mock(spec=Document)
    document.id = 1

    # Execute
    result = document_repo.delete_document(document)

    # Assert
    mock_db_session.delete.assert_called_once_with(document)
    mock_db_session.commit.assert_called_once()
