from typing import Optional, Dict, Any

from fastapi import HTTPException, status
from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standardized error response model"""
    message: str
    error_type: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: str = datetime.utcnow().isoformat() + "Z"
    code: Optional[str] = None


def raise_http(
        status_code: int,
        message: str,
        error_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
) -> HTTPException:
    """Raise standardized HTTP exceptions with consistent error format.

    Args:
        status_code: HTTP status code
        message: Human-readable error message
        error_type: Technical error type/category
        details: Additional error context
        error_code: Application-specific error code
        headers: Optional HTTP headers

    Returns:
        HTTPException with standardized error format
    """
    error_response = ErrorResponse(
        message=message,
        error_type=error_type,
        details=details,
        code=error_code
    )

    return HTTPException(
        status_code=status_code,
        detail=error_response.model_dump(exclude_none=True),
        headers=headers
    )

class DatabaseError(HTTPException):
    """Custom exception for database-related errors"""

    def __init__(
            self,
            detail: str = "Database operation failed",
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            original_error: Exception = None
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )
        self.original_error = original_error

    @classmethod
    def from_exception(cls, exc: Exception) -> "DatabaseError":
        """Create a DatabaseError from an existing exception"""
        return cls(
            detail=f"Database error: {str(exc)}",
            original_error=exc
        )
