
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.app.main import app

client = TestClient(app)


def test_ask_question():
    fake_result = {
        "answer": "LSTM is a type of recurrent neural network.",
        "sources": []
    }

    with patch(
        "backend.app.main.ask_question",
        return_value=fake_result
    ) as mock_ask:

        response = client.post(
            "/ask",
            json={
                "question": "What is LSTM?",
                "chat_history": []
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == fake_result["answer"]
    assert data["sources"] == []

    mock_ask.assert_called_once_with(
        "What is LSTM?",
        []
    )
    
def test_ask_question_rag_error():
    with patch(
        "backend.app.main.ask_question",
        side_effect=RuntimeError("RAG pipeline failed")
    ):
        response = client.post(
            "/ask",
            json={
                "question": "What is LSTM?",
                "chat_history": []
            }
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "RAG pipeline failed"
    
    
    
def test_ask_question_empty():
    with patch(
        "backend.app.main.ask_question"
    ) as mock_ask:

        response = client.post(
            "/ask",
            json={
                "question": "   ",
                "chat_history": []
            }
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Question cannot be empty."

    mock_ask.assert_not_called()