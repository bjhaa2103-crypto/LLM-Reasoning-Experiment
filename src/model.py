import time
from google import genai

MODEL_NAME = "gemini-3.8-flash"


def generate_response(client, question, method, max_retries=4):
    total_start_time = time.perf_counter()

    # Create the prompt based on the selected method
    if method == "Direct":
        prompt = f"""
Solve the following question.
Provide only the final answer.

Question: {question}
"""

    elif method == "Structured":
        prompt = f"""
Solve the following question using a structured approach.
Break the problem into clear steps.
Perform the necessary calculations or reasoning.
Check the result and provide the final answer.

Question: {question}
"""

    else:
        raise ValueError("Method must be Direct or Structured.")

    # Retry if the API temporarily fails
    for attempt in range(max_retries):
        try:
            start_time = time.perf_counter()

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            elapsed_time = time.perf_counter() - start_time

            usage = response.usage_metadata

            return {
    "response": response.text or "",

    # Time taken by the successful API request
    "response_time_seconds": round(elapsed_time, 3),

    # Total time, including retries and waiting
    "total_elapsed_seconds": round(
        time.perf_counter() - total_start_time, 3
    ),

    # Token usage
    "input_tokens": (
        getattr(usage, "prompt_token_count", None)
        if usage else None
    ),
    "output_tokens": (
        getattr(usage, "candidates_token_count", None)
        if usage else None
    )
}

        except Exception as error:

            # Retry temporary server errors and rate limits
            error_message = str(error)
            retryable = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
                or "500" in error_message
                or "INTERNAL" in error_message
            )

            if not retryable or attempt == max_retries - 1:
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Temporary API error. "
                f"Retrying in {wait_time} seconds "
                f"(attempt {attempt + 1}/{max_retries})..."
            )

            time.sleep(wait_time)