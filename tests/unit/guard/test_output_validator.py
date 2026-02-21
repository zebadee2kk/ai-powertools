from pydantic import BaseModel

from powertools.guard import OutputValidator


class TaskResult(BaseModel):
    task: str
    status: str


def test_extract_json_object_from_plain_json():
    payload = OutputValidator.extract_json_object('{"task":"build","status":"ok"}')
    assert payload["task"] == "build"


def test_extract_json_object_from_markdown_block():
    text = """Response:\n```json
    {"task": "build", "status": "ok"}
    ```"""
    payload = OutputValidator.extract_json_object(text)
    assert payload["status"] == "ok"


def test_validate_required_fields_reports_missing():
    result = OutputValidator.validate_json_text(
        '{"task":"build"}',
        required_fields=["task", "status"],
    )
    assert result.valid is False
    assert "Missing required field: status" in result.errors


def test_validate_with_pydantic_model():
    result = OutputValidator.validate_json_text(
        '{"task":"build","status":"ok"}',
        model_cls=TaskResult,
    )
    assert result.valid is True
    assert result.data == {"task": "build", "status": "ok"}
