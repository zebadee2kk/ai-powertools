from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Type

from pydantic import BaseModel, ValidationError


@dataclass
class ValidationResult:
    """Outcome of a validation check."""

    valid: bool
    errors: List[str] = field(default_factory=list)
    data: Optional[Dict[str, Any]] = None


class OutputValidator:
    """
    Lightweight output validation utility for LLM responses.

    Supports:
    - extracting JSON from raw text or ```json fenced blocks
    - required-field checks
    - optional pydantic model validation
    """

    JSON_BLOCK_PATTERN = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)

    @classmethod
    def extract_json_object(cls, text: str) -> Dict[str, Any]:
        stripped = text.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            return json.loads(stripped)

        match = cls.JSON_BLOCK_PATTERN.search(text)
        if not match:
            raise ValueError("No JSON object found in the text")

        return json.loads(match.group(1))

    @classmethod
    def validate_required_fields(
        cls,
        payload: Dict[str, Any],
        required_fields: Sequence[str],
    ) -> ValidationResult:
        missing = [field for field in required_fields if field not in payload]
        if missing:
            return ValidationResult(
                valid=False,
                errors=[f"Missing required field: {field}" for field in missing],
                data=payload,
            )
        return ValidationResult(valid=True, data=payload)

    @classmethod
    def validate_model(
        cls,
        payload: Dict[str, Any],
        model_cls: Type[BaseModel],
    ) -> ValidationResult:
        try:
            model = model_cls.model_validate(payload)
            return ValidationResult(valid=True, data=model.model_dump())
        except ValidationError as exc:
            return ValidationResult(
                valid=False,
                errors=[error["msg"] for error in exc.errors()],
                data=payload,
            )

    @classmethod
    def validate_json_text(
        cls,
        text: str,
        *,
        required_fields: Optional[Sequence[str]] = None,
        model_cls: Optional[Type[BaseModel]] = None,
    ) -> ValidationResult:
        try:
            payload = cls.extract_json_object(text)
        except (ValueError, json.JSONDecodeError) as exc:
            return ValidationResult(valid=False, errors=[str(exc)])

        if required_fields:
            field_check = cls.validate_required_fields(payload, required_fields)
            if not field_check.valid:
                return field_check

        if model_cls:
            return cls.validate_model(payload, model_cls)

        return ValidationResult(valid=True, data=payload)
