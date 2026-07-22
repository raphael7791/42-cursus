"""Pydantic models for function calling data."""

from pydantic import BaseModel
from typing import Any


class FunctionParameter(BaseModel):
    """A single function parameter with its type."""

    type: str


class FunctionDefinition(BaseModel):
    """Definition of a callable function."""

    name: str
    description: str
    parameters: dict[str, FunctionParameter]
    returns: FunctionParameter


class FunctionCalling(BaseModel):
    """A user prompt to be mapped to a function call."""

    prompt: str


class Output(BaseModel):
    """Result of a function call extraction."""

    prompt: str
    name: str
    parameters: dict[str, Any]
