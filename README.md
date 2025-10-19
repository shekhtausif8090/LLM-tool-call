
---

# Multi-Step Arithmetic Tool Agent

This project demonstrates a robust pattern for using large language models (LLMs) to perform complex, multi-step tasks by chaining function calls (tools). The agent is designed to break down arithmetic problems into sequential steps, calling specific Python functions (tools) to solve each step before proceeding to the next.

## 1. Project Goal

The primary goal is to solve the complex mathematical expression:
**"First calculate $3+4$, then multiply the result by $2$, then raise that new result to the power of $2$."**

This requires the LLM to successfully execute three chained tool calls:
1.  `get_sum(3, 4)` → Result: 7
2.  `get_multiply(7, 2)` → Result: 14
3.  `get_pow(14, 2)` → Result: 196

## 2. Code Structure

The code is organized into three main components:

### 2.1 Tool Function Definitions

These are the actual Python functions that perform the arithmetic.

| Function Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_sum` | Returns the addition of two numbers. | `number1`, `number2` |
| `get_multiply` | Returns the product of two numbers. | `number1`, `number2` |
| `get_pow` | Returns the first number raised to the power of the second. | `number1`, `number2` |

### 2.2 Tool JSON Schemas (`tools` list)

This list provides the structured description (schema) for the LLM, informing it exactly how to call each function (name, description, required arguments, and their data types).

**💡 Critical Correction:** In the original schema, the `get_multiply` tool was incorrectly named `"get_multipy"`. This has been corrected to `"get_multiply"` to match the Python function definition.

### 2.3 The Core Execution Loop

The heart of the agent is a `while True` loop that manages the conversation flow:

1.  **Request:** The agent sends the current `history` (including the user prompt and any previous tool results) to the LLM.
2.  **Response Handling:**
    *   **If the LLM responds with `tool_calls`:** The agent executes the specified Python functions using the arguments provided by the model. The results of these functions are formatted as "tool" messages and appended to the `history`. The loop then repeats, prompting the model to take the next step based on the new results.
    *   **If the LLM responds with a final text message (no `tool_calls`):** This is considered the final answer. The message content is printed, and the loop breaks.

## 3. Key Concepts Demonstrated

### Chain of Thought & Tool Chaining
The script demonstrates the model's ability to implicitly follow a plan:
1.  Read the user's multi-step request.
2.  Identify the first necessary tool (`get_sum`).
3.  Execute `get_sum` and get the result (7).
4.  Identify the second necessary tool (`get_multiply`), using the result from the previous step (7).
5.  Execute `get_multiply` and get the result (14).
6.  Identify the final tool (`get_pow`), using the new result (14).
7.  Execute `get_pow` and get the final numerical result (196).
8.  Formulate the final human-readable answer.

### Robust Multi-Step Conversation
Unlike a single-turn conversation, the `while` loop ensures the conversation continues until the model explicitly provides a final answer, allowing for several rounds of tool execution and reasoning.

## 4. How to Run the Code

### Prerequisites
1.  **Python:** Ensure Python is installed.
2.  **OpenAI Library:** Install the required library:
    ```bash
    pip install openai
    ```

### Setup
1.  **API Key:** You must set your OpenAI API key. The provided code includes a placeholder line:
    ```python
    client = OpenAI(api_key="YOUR_API_KEY_HERE")
    ```
    Replace `"YOUR_API_KEY_HERE"` with your actual key.

### Execution
Simply run the Python script:
```bash
python your_file_name.py
```

### Expected Output Flow

The console output will show the iterative process:

```
--------------------
Sending request to model with history:
Tool 'get_sum' called with: 3, 4
--------------------
Sending request to model with history:
Tool 'get_multiply' called with: 7, 2
--------------------
Sending request to model with history:
Tool 'get_pow' called with: 14, 2
--------------------
Sending request to model with history:

===== FINAL ANSWER =====
The final result of the calculation (3+4) * 2^2 is 196.
```
