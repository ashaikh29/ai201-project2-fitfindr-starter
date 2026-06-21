# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
search_listings takes a user's input and goes through listings.json to find close matches to the user input. It filters through the sizes and max_prices of listings to find an item that has a description similar to the user input. 

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): keywords that describe what the user is looking for
- `size` (str): size of clothing to filter by
- `max_price` (float): the maximum price a user is willing to pay

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
The tools returns a dictionary of matching listings, sorted by relevance (most relevant are towards the top). The fields of the results include: id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand, platform

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
If no listings match, the agent returns an empty list and suggests changing either the description, size, or max price to find matches. If this happens, the agent won't proceed to the next steps, which are using tools 2 and 3.

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
suggest_outfit takes a particular piece of clothing and the user's wardrobe to suggest 1-2 outfit ideas. If the user doesn't provide their wardrobe, this tool can also provide general styling tips for the piece of clothing.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): The listed item that the user is considering buying
- `wardrobe` (dict): Wardrobe items. Contains an items key which has a list of wardrobe item dicts

**What it returns:**
<!-- Describe the return value -->
The tool returns 1-2 outfit suggestions. These suggestions can include color combinations, weather suggestions, clothing combinations, and more. 

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
If the wardrobe parameter is empty, the tool returns general styling tips for the new_item parameter; this can be clothes, colors, textures, or anything else that pairs well with the item. If this happens, the agent won't proceed to the next step, which is using tool 3.

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
The create_fit_card tool takes a complete outfit and creates a 2-4 sentence social-media-worthy caption for it.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (str): Selected outfit from suggest_outfit
- `new_item` (dict): The dict for the listed item the user is considering buying

**What it returns:**
<!-- Describe the return value -->
The tool returns a 2-4 sentence fit card for social media. The fit card should be in natural, casual language and should contain the name of the item, the price, and the platform it was bought from. The caption shouldn't be generalized, but should capture the specific vibe of the outfit.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
If no outfit is provided or the outfit is incomplete, the agent will let the user know to select a complete outfit.

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->
N/A

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->
The planning loop is sequential:
1. A new session is initialized
2. The user's input will be parsed using regex to get the parameters description, size, and max_price. The parsed result will be stored in session["parsed].
3. The tool search_listings() is called with the parsed input. The results will be stored in session["search_results]. If the results are empty, set session["error"] to a helpful error message; return the session early and do not call suggest_outfit.
4. Store the top result of the search result in session["selected_item"]
5. The tool suggest_outfit() is called with the selected item and user wardrobe as inputs. The result is stored in session["outfit_suggestion"]
6. The tool create_fit_card() is called with the inputs of the outfit suggestion and selected item. The result is stored in session["fit_card"]
7. Return the session

---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->
The outputs from each tool are saved in session state to be used as inputs by the next tool.
The following data is tracked:
- user's parsed input: description, size, and max_price
- search results from search_listings
- error message for when there are no search results from search_listings
- the chosen search result from search_listings
- generated outfit recommendations from suggest_outfit
- fit card from create_fit_card

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | Suggest broader search terms in either description, size, or max_price |
| suggest_outfit | Wardrobe is empty | Provide general styling advice |
| create_fit_card | Outfit input is missing or incomplete | Ask user to provide a complete outfit |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     Use ASCII art or a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html).
     Do NOT embed an image — graders need to read your diagram directly in the file;
     an embedded image or screenshot cannot be evaluated.
     You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->
```mermaid
flowchart TD
    A[User Query] --> B[Planning Loop]

    B --> C[Parse user request]
    C --> D[search_listings(description, size, max_price)]

    D --> E{Results found?}
    E -->|No| F[Return error: No listings found]
    F --> B

    E -->|Yes| G[Store selected_item = results[0] in session]

    G --> H[suggest_outfit(selected_item, wardrobe)]
    H --> I{Wardrobe available?}

    I -->|No| J[Generate general styling advice]
    I -->|Yes| K[Generate personalized outfit suggestion]

    J --> L[Store outfit_suggestion in session]
    K --> L

    L --> M[create_fit_card(outfit_suggestion, selected_item)]

    M --> N{Fit card created?}
    N -->|No| O[Return error: missing outfit data]
    O --> B

    N -->|Yes| P[Store fit_card in session]
    P --> Q[Return final session to user]
```



---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**
I plan to use Claude. As input, I will give the following sections from planning.md: search_listings(), suggest_outfit(), and create_fit_card() (the description, the parameters, the expected output, and the failure plan for each tool). I expect Claude to produce Python implementations of each tool. I plan to work on one tool at a time, testing each as I go. I'll test search_listings with 3 queries, suggest_outfit with a full wardrobe and an empty wardrobe, and create_fit_card with a complete outfit and an incomplete outfit. 

**Milestone 4 — Planning loop and state management:**
I plan to give Claude my planning loop, state handling, error handling, and archicture diagram sections from planning.md. I also plan to give it my code implementations of all 3 tools. I expect it to produce a Python implementation of a planning loop, state manager in a logical way. I plan to test by fully going through the agent to ensure the tools are being called in the right order, that errors are being handled appropriately, and that the state is being passed accurately. 

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

FitFindr needs to create a fit card for social media. It does this by taking an input of a particular item from the user and finding that item. From there, it creates a wardrobe with similar items and suggests a caption for the user to post the outfit on social media. 

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
Using the input, ("vintage graphic tee", size=none, max_price=30.0), the agent uses the tool search_listings to search for any listings similar to the description. After filtering out price and size, it scores each listing based on the relevance and returns a list with the highest scores ranking first. If there are no matches, the agent doesn't return anything (thus, the next steps won't happen).

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
Now, the tool suggest_outfit is called: (new_item=<vintage tee> , wardrobe=<user's wardrobe>). The agent uses one of the listings the user is considering buying and the user's wardrobe to return suggestions on outfits. If the user doesn't have a wardrobe, the tool returns some general styling advice for the listing. 

**Step 3:**
<!-- Continue until the full interaction is complete -->
Finally, the tool create_fit_card is called: (outfit=<suggestion> , new_item=<vintage tee>). The tool uses one of the outfits the user picks as well as the same listing the user is considering buying to generate a 2-4 sentence caption for social media. If the outfit field is blank, the tool returns an error message. 

**Final output to user:**
<!-- What does the user actually see at the end? -->
"the 2000's are calling and they want their fashion back. this super cute vintage tee was thrifted from depop and makes me sooo happy. more deets on my story"
