# ollama-function-calling
This proejct demonstrates use of function calling using Ollama modelss
The Python code demonstrates a comprehensive workflow for utilizing function calling with Ollama's AsyncClient to perform tasks like categorizing grocery items, fetching price and nutrition data, and generating recipes for categorized food items. Here's an enhanced explanation:
 
The Python code demonstrates a comprehensive workflow for utilizing function calling with Ollama's AsyncClient to perform tasks like categorizing grocery items, fetching price and nutrition data, and generating recipes for categorized food items. Here's an enhanced explanation:

**Workflow Breakdown**

**1\. Preparing the System**

- **Loading Data**: The grocery list is loaded from a text file, ensuring non-empty and valid entries.
- **Defining Tools**: A dictionary of functions (tools) is prepared, each with:
  - **Name**: Identifier for the tool.
  - **Description**: Brief on its purpose (e.g., fetch price, fetch recipe).
  - **Parameters**: Specification of required input arguments (name, type, etc.).

Example:  
fetch_price_and_nutrition accepts an item name and returns mock price and nutrition data.

```
# Function to fetch price and nutrition data for an item
async def fetch_price_and_nutrition(item):
    print(f"Fetching price and nutrition data for '{item}'...")
    # Replace with actual API calls
    # For demonstration, we'll return mock data
    await asyncio.sleep(0.1)  # Simulate network delay
    return {
        "item": item,
        "price": f"${random.uniform(1, 10):.2f}",
        "calories": f"{random.randint(50, 500)} kcal",
        "fat": f"{random.randint(1, 20)} g",
        "protein": f"{random.randint(1, 30)} g",
    }
```


**2\. Categorizing Grocery Items**

- **Prompt Creation**:  
    A detailed prompt instructs the model to categorize items into a JSON structure with categories as keys and items as values. The prompt is explicit to ensure output validity and proper formatting.
```
    categorize_prompt = f"""
You are an assistant that categorizes grocery items.

**Instructions:**

- Return the result **only** as a valid JSON object.
- Do **not** include any explanations, greetings, or additional text.
- Use double quotes (`"`) for all strings.
- Ensure the JSON is properly formatted.
- The JSON should have categories as keys and lists of items as values.

**Example Format:**

{{
  "Produce": ["Apples", "Bananas"],
  "Dairy": ["Milk", "Cheese"]
}}

**Grocery Items:**

{', '.join(grocery_items)}
"""
```
- **First API Call**:
  - Send the prompt and tools to the model using client.chat.
  - Append the model's response to the **messages list** for maintaining context.
- **Parsing Response**:  
    Parse the model's JSON response to extract categorized grocery items. Handle parsing errors gracefully.

**3\. Fetching Price and Nutrition Data**

- **Dynamic Function Calling**:
  - A new prompt instructs the model to fetch price and nutrition data for each grocery item using the fetch_price_and_nutrition function.
  - The **Second API Call** includes this prompt, tools, and updated messages.
- **Tool Invocation**:
  - Check if the model's response contains "tool_calls".
  - Identify the tool (fetch_price_and_nutrition) and invoke it with the required arguments using await.
  - Append function responses to both the **messages list** and an **item details list**.

**4\. Fetching Recipes**

- **Category Selection**:  
    Randomly choose a category from the categorized items for recipe generation.
- **Dynamic Recipe Generation**:
  - Prompt the model to fetch a recipe for the selected category using the fetch_recipe function.
  - Perform the **Third API Call** and handle tool calls in the same way as before.

**5\. Finalizing the Response**

- **Consolidation**:  
    Append all responses (including function outputs) to the **messages list**.
- **Final API Call**:  
    Generate a cohesive, assistant-style summary based on all preceding interactions.

**Key Features of the Implementation**

1. **Asynchronous Execution**:
    - Functions like fetch_price_and_nutrition and fetch_recipe simulate real-world API calls, leveraging asyncio for non-blocking operations.
2. **Dynamic Decision-Making**:
    - The model autonomously decides which tools to invoke, based on contextual prompts.
3. **Robust Context Management**:
    - The **messages list** ensures every response builds on prior interactions, maintaining continuity and context.
4. **Error Handling**:
    - JSON parsing errors are caught, and fallback mechanisms ensure smooth execution.
5. **Scalability**:
    - The workflow can be expanded to accommodate additional tools or more complex tasks.
