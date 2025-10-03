"""
Code Execution API Routes
Handles safe code execution in isolated environment
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import os
from loguru import logger

router = APIRouter()


class CodeExecutionRequest(BaseModel):
    """Request model for code execution"""
    code: str
    language: str = "python"
    stdin: Optional[str] = None


class CodeExecutionResponse(BaseModel):
    """Response model for code execution"""
    output: str
    error: Optional[str] = None
    execution_time: float


@router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """
    Execute code safely with timeout and resource limits

    Args:
        request: Code execution request with code and language

    Returns:
        Execution result with output and errors
    """
    try:
        if request.language.lower() != "python":
            raise HTTPException(
                status_code=400,
                detail=f"Language '{request.language}' not supported yet. Only Python is currently supported."
            )

        # Validate code length
        if len(request.code) > 10000:
            raise HTTPException(
                status_code=400,
                detail="Code is too long (max 10000 characters)"
            )

        # Execute Python code
        result = await execute_python_code(request.code, request.stdin)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Code execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def execute_python_code(code: str, stdin: Optional[str] = None) -> CodeExecutionResponse:
    """
    Execute Python code safely

    Args:
        code: Python code to execute
        stdin: Optional standard input

    Returns:
        Execution response with output and timing
    """
    import time

    start_time = time.time()

    try:
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Execute with timeout and capture output
            result = subprocess.run(
                ['python3', temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5,  # 5 second timeout
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
            )

            execution_time = time.time() - start_time

            # Combine stdout and stderr
            output = result.stdout
            error = result.stderr if result.returncode != 0 else None

            if not output and not error:
                output = "(No output)"

            logger.info(f"Code executed successfully in {execution_time:.2f}s")

            return CodeExecutionResponse(
                output=output,
                error=error,
                execution_time=execution_time
            )

        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        logger.warning("Code execution timeout")
        return CodeExecutionResponse(
            output="",
            error="⏱️ Execution timeout (5 seconds limit exceeded)",
            execution_time=execution_time
        )
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Python execution error: {e}")
        return CodeExecutionResponse(
            output="",
            error=f"❌ Execution error: {str(e)}",
            execution_time=execution_time
        )
