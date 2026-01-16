---
title: Community Error Pattern Library Specification
task_id: Task 4.2
date: 2025-05-19
last_updated: 2025-05-19
status: DRAFT
owner: deep-research-agent
---

## 1. Introduction and Goals

### 1.1. Objective
The primary objective of the Roo Code Community Error Pattern Library is to create a collaboratively maintained, comprehensive, and easily accessible knowledge base of common error patterns encountered when using Roo Code. This library aims to:
*   Empower users to quickly identify and resolve common issues.
*   Reduce redundant troubleshooting efforts within the community.
*   Provide a structured way to share solutions and best practices.
*   Offer insights into frequent error types, informing future Roo Code development and documentation.
*   Foster a collaborative environment for improving the Roo Code user experience.

### 1.2. Scope
This library will focus on error patterns directly related to the usage of Roo Code, including but not limited to:
*   Errors originating from specific Roo modes.
*   Issues related to prompt construction leading to unexpected LLM behavior.
*   Problems with tool usage or configuration within Roo Code.
*   Misinterpretations of Roo Code's capabilities or limitations.

The library will not primarily focus on:
*   General programming errors unrelated to Roo Code.
*   Bugs within the underlying LLMs (though patterns of LLM misbehavior *as observed through Roo Code* are in scope).
*   Issues specific to individual user environments unless they represent a common pattern.

## 2. Standardized Error Pattern Format

To ensure consistency and searchability, all community contributions should adhere to the following standardized format. Submissions will likely be made through a web form or a structured template (e.g., a GitHub issue template).

```yaml
# Error Pattern Entry

# --- Basic Information ---
error_id: # Auto-generated or assigned during moderation (e.g., ROO-ERR-YYYYMMDD-NNN)
title: "A concise, descriptive title for the error pattern (e.g., 'Unexpected HTML Output in Code Mode when Requesting JSON')"
date_reported: YYYY-MM-DD # Date of initial submission
last_updated: YYYY-MM-DD # Date of last modification
version: 1.0 # Version of this error pattern entry
status: # [Reported, Verifying, Accepted, NeedsMoreInfo, Rejected, Deprecated] - Managed by moderators

# --- Error Details ---
description: |
  A clear and detailed description of the error.
  What happened? What was the user trying to achieve?
modes_affected:
  - code # List all Roo Code modes where this error has been observed (e.g., code, architect, ask)
  - research
keywords_tags:
  - code-generation
  - json-output
  - html-entities
  - unexpected-format
  - prompt-engineering

# --- Reproduction ---
example_prompt_input: |
  # Provide the exact or a representative prompt/input that triggered the error.
  # For multi-turn conversations, include relevant preceding turns if necessary.
  "Please generate a JSON object representing a user with fields: name, email, and id."
observed_erroneous_output: |
  # The actual output received that demonstrates the error.
  # Include code blocks or verbatim text.
  "<div>{</div>
  <div>  \"name\": \"Test User\",</div>
  <div>  \"email\": \"test@example.com\",</div>
  <div>  \"id\": 123</div>
  <div>}</div>"
expected_correct_output: |
  # The output the user expected or what would be considered correct.
  # (Optional, but highly recommended)
  {
    "name": "Test User",
    "email": "test@example.com",
    "id": 123
  }

# --- Analysis and Solution ---
potential_cause_analysis: |
  An analysis of why the error might be occurring.
  This could involve:
  - Ambiguity in the prompt.
  - LLM misinterpreting the request format.
  - Mode-specific processing issues.
  - Known limitations of the underlying model.
  "The LLM in Code Mode, when not explicitly constrained, sometimes defaults to generating HTML-like structures, especially if the prompt is slightly ambiguous or if it has recently processed HTML-related requests. It might be trying to 'wrap' the JSON in a displayable format."
suggested_correction_strategy: |
  Actionable steps or strategies to correct or work around the error.
  This could include:
  - Prompt refinement techniques.
  - Specific instructions to give Roo.
  - Tool usage adjustments.
  - Configuration changes.
  "1. Explicitly state the desired output format: 'Generate a **raw JSON object**...'
   2. Add a constraint: 'Do not include any HTML tags or formatting.'
   3. If the error persists, try switching to a different model or a mode less prone to this behavior for this specific task, if applicable."
workaround_available: Yes # [Yes, No, Partial]
workaround_description: |
  # If a full correction isn't available, describe any workarounds.
  "Manually removing the HTML tags post-generation."

# --- Community Interaction ---
reported_by: "CommunityUsername / Anonymous (if telemetry-sourced)"
verified_by: # List of usernames who verified this pattern
verification_date: YYYY-MM-DD
related_issues: # Links to related GitHub issues, forum discussions, or other error patterns
  - "#1234"
  - "ROO-ERR-XXXXXX"
comments: |
  # Space for moderator notes or community discussion summaries.

# --- Telemetry Link (Optional) ---
telemetry_event_ids: # If sourced or correlated with telemetry data
  - "event_id_abc"
  - "event_id_xyz"
frequency_telemetry: High # [Low, Medium, High] - Based on telemetry if available
```

## 3. Submission, Verification, and Moderation Process

### 3.1. Submission Channels
1.  **GitHub Issues:** A dedicated GitHub repository (or a specific label within the main Roo Code repository) using an issue template based on the standardized format.
2.  **Web Form:** A dedicated form on the Roo Code documentation website, which would then create a structured entry (e.g., a pending GitHub issue or a database entry).
3.  **Directly from Roo Code (Future):** A potential feature where users can flag an interaction and initiate an error pattern submission pre-filled with context from their session.

### 3.2. Initial Triage (Automated/Moderator-Lite)
*   **Completeness Check:** Ensure all mandatory fields in the submission are filled.
*   **Duplicate Check:** Basic keyword-based search for existing similar patterns. (More advanced semantic similarity could be explored later).
*   **Sanitization:** Check for and remove any sensitive information if accidentally included by the submitter (though submitters will be advised against including PII).

### 3.3. Verification Process
This process aims to ensure accuracy, reproducibility, and relevance.
1.  **Community Review (Optional but Encouraged):**
    *   Submitted patterns (e.g., as new GitHub issues) are open for community members to comment, confirm reproducibility, suggest improvements, or note variations.
    *   A "thumbs up" or "can reproduce" reaction system could gauge community validation.
2.  **Moderator/Maintainer Review:**
    *   A designated team of moderators (community volunteers and/or Roo Code maintainers) will be responsible for the final verification.
    *   **Reproducibility:** Moderators attempt to reproduce the error based on the provided information.
    *   **Accuracy:** Verify the description, observed output, and potential cause.
    *   **Clarity:** Ensure the submission is well-written and easy to understand.
    *   **Relevance:** Confirm the error pattern is relevant to Roo Code and not an isolated incident or user error unrelated to Roo Code's behavior.
    *   **Categorization:** Assign appropriate tags, keywords, and affected modes.
3.  **Status Updates:** The status of the submission (e.g., `Reported`, `Verifying`, `NeedsMoreInfo`, `Accepted`, `Rejected`) is updated and visible to the submitter and community.

### 3.4. Moderation Actions
*   **Accept:** The pattern is added to the official library.
*   **Request More Information:** If the submission is unclear or lacks details for reproduction, moderators will request clarification from the submitter.
*   **Merge/Link:** If the pattern is very similar to an existing one, it might be merged, or linked as a variation.
*   **Reject:** If the pattern is out of scope, not reproducible, or deemed not a valid error pattern for Roo Code. A reason for rejection should be provided.
*   **Edit/Refine:** Moderators may edit submissions for clarity, formatting, or to add additional insights before acceptance.
*   **Deprecate:** If a pattern becomes obsolete due to Roo Code updates, it can be marked as deprecated.

### 3.5. Contributor Recognition
Consider a system to acknowledge active and helpful contributors (e.g., badges, mentions in release notes, a leaderboard on the documentation site).

## 4. Library Structure and Access

### 4.1. Structure
The library could be structured in several ways, potentially offering multiple views/filters:
1.  **By Roo Code Mode:**
    *   `/code_mode/`
    *   `/architect_mode/`
    *   `/ask_mode/`
    *   `/research_mode/`
    *   `/general/` (for errors not specific to one mode)
2.  **By Error Type/Category:** (Based on keywords/tags)
    *   `/output_formatting/`
    *   `/prompt_misinterpretation/`
    *   `/tool_errors/`
    *   `/unexpected_behavior/`
3.  **By LLM (If Applicable and Identifiable):**
    *   If certain patterns are strongly correlated with specific underlying LLMs that Roo Code might use.
4.  **Flat Structure with Robust Tagging/Filtering:** All entries in a single collection, relying heavily on the `keywords_tags` and other metadata for searching and filtering. This is often the most flexible approach for web-based UIs.

A combination is likely best: a primary organization (e.g., by mode or a flat list) with strong faceted search capabilities.

### 4.2. Access and Search
1.  **Documentation Website:**
    *   A dedicated section on the official Roo Code documentation website (e.g., `docs.roocode.ai/error-patterns`).
    *   **Search Bar:** Prominent search functionality supporting keyword search across all fields (title, description, prompt, tags, etc.).
    *   **Faceted Filters:** Allow users to filter by `modes_affected`, `keywords_tags`, `status`, `date_reported`, etc.
    *   **Browseable Categories:** If a hierarchical structure is used, allow browsing by those categories.
    *   Each error pattern would have its own page displaying all information from the standardized format.
2.  **Integrated Roo Code Feature (Future):**
    *   A command or UI element within Roo Code (e.g., `/find_error_pattern <keywords>`) that allows users to search the library directly from their Roo Code interface.
    *   Potentially, Roo Code could proactively suggest relevant error patterns if an interaction matches known problematic signatures (linking to the telemetry system).
3.  **API Access (Future):**
    *   An API could allow third-party tools or advanced users to programmatically access the library data.

## 5. Integration with Error Telemetry System (Task 4.1)

The error telemetry system can significantly inform and benefit the community error pattern library:
1.  **Identifying Candidate Patterns:**
    *   The telemetry system can identify frequently occurring anonymous error reports or negative feedback signals (e.g., high number of "thumbs down" on certain types of interactions, common error codes/messages if Roo Code emits them).
    *   These frequently reported anonymous issues can be flagged as candidates for formal documentation in the community library. Moderators or community members could then investigate these trends and create a detailed error pattern entry.
2.  **Populating `frequency_telemetry` Field:**
    *   For patterns that have a corresponding signature in the telemetry data, the `frequency_telemetry` field in the error pattern entry can be updated (e.g., "High," "Medium," "Low") to indicate how often this type of error is being anonymously reported. This helps prioritize which errors are most impactful.
3.  **Correlating User Reports with Telemetry:**
    *   If a user submits an error pattern, and they have opted into telemetry, it might be possible (with privacy considerations) to correlate their specific session/event IDs (`telemetry_event_ids`) with the broader anonymous telemetry data to understand the context better.
4.  **Feedback Loop for Telemetry Signatures:**
    *   Once a community-verified solution or workaround is documented for an error pattern, the telemetry system could potentially learn from this. For example, if Roo Code detects an interaction matching a pattern with a known effective prompt refinement, it might subtly guide the user or adjust its internal strategy (advanced feature).
5.  **Measuring Solution Effectiveness:**
    *   If the telemetry system can track the application of suggested solutions (e.g., user tries a refined prompt suggested by the library), it could provide data on how effective different solutions are, further enriching the library.

## 6. Example Error Pattern Entry

```yaml
# Error Pattern Entry

# --- Basic Information ---
error_id: ROO-ERR-20250519-001
title: "Code Mode generates Python list comprehension with incorrect variable scope"
date_reported: 2025-05-19
last_updated: 2025-05-19
version: 1.0
status: Reported

# --- Error Details ---
description: |
  When asking Code Mode to generate a Python list comprehension that filters based on an external variable, the generated code sometimes incorrectly tries to use a new local variable within the comprehension's conditional part as if it were the external variable, leading to NameError or incorrect filtering.
modes_affected:
  - code
keywords_tags:
  - python
  - list-comprehension
  - variable-scope
  - nameerror
  - code-generation

# --- Reproduction ---
example_prompt_input: |
  "I have a list of numbers: `my_numbers = [1, 2, 3, 4, 5, 6]`
  And a threshold variable: `threshold = 3`
  Generate a Python list comprehension that creates a new list containing only numbers from `my_numbers` that are greater than `threshold`."
observed_erroneous_output: |
  # Sometimes generates:
  # my_numbers = [1, 2, 3, 4, 5, 6]
  # threshold = 3
  # filtered_numbers = [x for x in my_numbers if number > threshold] # 'number' should be 'x'
  # or
  # filtered_numbers = [x for x in my_numbers if y > threshold] # 'y' is undefined
expected_correct_output: |
  my_numbers = [1, 2, 3, 4, 5, 6]
  threshold = 3
  filtered_numbers = [x for x in my_numbers if x > threshold]
  # Result: [4, 5, 6]

# --- Analysis and Solution ---
potential_cause_analysis: |
  The LLM might be getting confused with variable naming within the concise structure of a list comprehension, especially when an external variable is involved in the condition. It might be attempting to introduce a new placeholder variable for the conditional part without correctly linking it to the iteration variable.
suggested_correction_strategy: |
  1. **Be explicit about the variable in the condition:** "Generate a Python list comprehension... ensuring the condition `x > threshold` uses the iterated variable `x`."
  2. **Break down the request:** Ask for the loop and conditional logic separately, then ask to convert it to a list comprehension.
  3. **Provide an example of a correct list comprehension with a similar structure in the prompt.**
workaround_available: Yes
workaround_description: |
  Manually correct the variable name in the generated list comprehension's conditional statement.

# --- Community Interaction ---
reported_by: "UserExample123"
verified_by:
verification_date:
related_issues:
comments: |
  Initial submission. Awaiting verification.

# --- Telemetry Link (Optional) ---
telemetry_event_ids:
frequency_telemetry:
```

## 7. Future Considerations
*   **Versioning of Error Patterns:** As Roo Code evolves, patterns and their solutions might change.
*   **Localization:** Supporting submissions and viewing in multiple languages.
*   **Advanced Search:** Semantic search or "more like this" functionality.
*   **Gamification:** Points or rewards for contributions and verifications.
*   **Automated Suggestion of Patterns:** Roo Code itself suggesting relevant patterns during user interaction.