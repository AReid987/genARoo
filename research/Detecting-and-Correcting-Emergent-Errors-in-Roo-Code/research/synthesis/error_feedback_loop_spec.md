---
title: Implementation Specification for Dynamic System Prompt Enhancement
task_id: task_3.2
date: 2025-05-19
last_updated: 2025-05-19
status: DRAFT
owner: deep-research-agent
---

# Implementation Specification for Dynamic System Prompt Enhancement

## 1. Introduction

This document details the design for a system to dynamically enhance Roo Code's mode system prompts by feeding detected error patterns back as examples. The goal is to improve LLM performance and reduce error rates by providing concrete examples of undesirable outputs and preferred corrections. This builds upon previous analyses of Roo Code's mode configuration and error detection mechanisms.

## 2. Analysis of Roo Code's Current Prompt Management System

Roo Code's system prompt management architecture, as analyzed in `research/synthesis/mode_configuration_architecture_analysis.md` (Task 0.2), offers several mechanisms for modification, making it suitable for dynamic updates with error examples.

### 2.1 Key Architectural Features for Prompt Modification

*   **Centralized Prompt Generation:** A core function (referred to as `SYSTEM_PROMPT`) dynamically assembles system prompts from various components including role definitions, tool descriptions, rules, and custom instructions.
*   **File-Based Overrides:**
    *   The system supports overriding the main content of a system prompt for a specific mode using a dedicated file.
    *   The path for these files is determined by the `getSystemPromptFilePath(cwd: string, mode: Mode)` function, which resolves to `path.join(cwd, ".roo", \`system-prompt-${mode_slug}\`)`.
    *   These override files are loaded by `loadSystemPromptFile` and their content is combined with the mode's `roleDefinition` and `customInstructions`.
    *   This mechanism appears to be the most direct and flexible for injecting dynamic error examples, as changes to these files are likely picked up quickly by the `SYSTEM_PROMPT` function.
*   **`customInstructions` in Mode Configuration:**
    *   Each mode configuration (`ModeConfig`) allows for an optional `customInstructions` string. These configurations are defined in `Roo-Code/src/shared/modes.ts` for built-in modes and can be customized via `.roomodes` files (project-specific, highest precedence) or global settings.
    *   The `CustomModesManager` (defined in `Roo-Code/src/core/config/CustomModesManager.ts`) loads and merges these configurations.
    *   This field provides another avenue for adding error examples.
*   **`CustomModesManager` Caching and Updates:**
    *   `CustomModesManager` caches loaded mode configurations for a short period (10 seconds TTL).
    *   It possesses an `updateCustomMode` method, which could be leveraged to programmatically update a mode's configuration (including `customInstructions`) and potentially invalidate the cache for that mode.

### 2.2 Suitability for Dynamic Error Example Incorporation

*   **High Suitability via File-Based Overrides:** This is the preferred method. The `.roo/system-prompt-${mode_slug}` files can be programmatically managed by the error feedback system. Updates to these files are likely reflected in the next prompt generation for the respective mode without significant delay from caching mechanisms related to mode *configurations*.
*   **Good Suitability via `customInstructions`:** Modifying the `customInstructions` in `.roomodes` files (or other mode configuration sources) is also a strong option. The 10-second cache of `CustomModesManager` means updates might have a slight delay unless the `updateCustomMode` method is used to force a refresh.

## 3. Proposed Architecture for the Error Pattern Feedback Loop

The proposed system collects errors from various sources, processes them, and then updates the relevant mode system prompts with corrective examples.

```mermaid
graph TD
    subgraph "Error Sources"
        A1[Semantic Guardrails]
        A2[Consistency Checks]
        A3[User Corrections/Feedback]
        A4[Other Monitoring (e.g., Phase 1 & 2 outputs)]
    end

    A1 --> B[Error Collector Service]
    A2 --> B
    A3 --> B
    A4 --> B

    subgraph "Error Processing & Storage"
        B --> C{Error Formatter & Normalizer}
        C --> D[Error Database/Store]
        D --> E{Error Prioritizer & Selector}
        E --> F[Generalized Error Pattern Extractor (Optional)]
    end

    subgraph "Prompt Update Mechanism"
        F --> G[Prompt Enhancer Module]
        E --> G
        G --> H{Targeted Prompt File Updater}
        H --> I1[".roo/system-prompt-modeA.md"]
        H --> I2[".roo/system-prompt-modeB.md"]
        H --> J[CustomModesManager (.roomodes updater - Alternative)]
    end

    subgraph "Roo Code Core"
        K[SYSTEM_PROMPT Function] --> L[LLM]
        I1 --> K
        I2 --> K
        J -- Loads --> K
    end

    subgraph "Evaluation & Monitoring"
        L -- Output --> M[Error Detection (again)]
        M --> N[Performance Metrics Tracker]
        N --> O[Dashboard/Reporting]
        D -- Data for --> N
    end
```

### 3.1 Component Descriptions

1.  **Error Sources:** Existing and future mechanisms that detect or report errors (e.g., semantic guardrails, consistency checkers, direct user feedback, outputs from Phase 1 & 2 tasks).
2.  **Error Collector Service:** A centralized service or set of listeners to receive and initially standardize error reports.
3.  **Error Formatter & Normalizer:** Structures raw error data, including timestamp, error source, mode, original input, erroneous output, corrected output (if available), and error type. Normalizes similar errors.
4.  **Error Database/Store:** Persists formatted error instances, allowing for querying, aggregation, and analysis.
5.  **Error Prioritizer & Selector:** Selects the most valuable errors for feedback based on criteria like frequency, severity, recency, user flagging, and diversity. Manages the number of examples per prompt.
6.  **Generalized Error Pattern Extractor (Optional but Recommended):** Generalizes specific error instances into broader, more concise patterns (e.g., "Used outdated syntax" instead of "Used 'var' for 'let'").
7.  **Prompt Enhancer Module:** Formats selected/generalized error patterns into instructional text suitable for system prompts.
8.  **Targeted Prompt File Updater:** The primary component responsible for modifying system prompts. It will identify the relevant mode(s) and update the corresponding `.roo/system-prompt-${mode_slug}` files. An alternative pathway could involve updating `customInstructions` in `.roomodes` files via `CustomModesManager.updateCustomMode`.
9.  **Roo Code Core (SYSTEM_PROMPT Function & LLM):** The existing Roo Code components that will utilize the enhanced prompts.
10. **Performance Metrics Tracker & Reporting:** Monitors the effectiveness of the feedback loop by tracking error rates and other relevant metrics over time.

## 4. Methods for Collecting, Formatting, Prioritizing, and Integrating Error Examples

This section details the operational aspects of the error feedback loop, from capturing errors to injecting them as learning examples into system prompts.

### 4.1 Error Collection

Errors will be collected from multiple sources within the Roo Code ecosystem. The Error Collector Service will provide standardized APIs or listen for events from:

*   **Semantic Guardrails:** When a guardrail (developed in Phase 1) detects a semantic violation, it will emit an error event including the violating content, the specific guardrail triggered, and context about the task and mode.
*   **Consistency Checks:** Automated checks (potentially from Phase 1 or other monitoring tools) that identify inconsistencies in outputs will report these discrepancies.
*   **User Corrections/Feedback:**
    *   Explicit user feedback (e.g., "thumbs down" on a response, manual correction of an output).
    *   Implicit feedback (e.g., user re-rolling a response multiple times, or abandoning a task after a particular output). This requires careful interpretation.
    *   A dedicated UI element could allow users to flag an output as erroneous and optionally provide a corrected version or reason.
*   **Outputs from Phase 1 & 2:** Data from Semantic Drift Detection and Error Containment mechanisms (e.g., sandbox violations, cost anomalies if they correlate with output quality issues) can serve as indirect error indicators.
*   **Automated Testing Failures:** Failures in unit, integration, or end-to-end tests that are attributable to LLM output quality can be channeled into this system.

The Error Collector Service will aggregate these reports, ensuring each contains minimal necessary metadata like timestamp, source, mode, and the raw error data.

### 4.2 Error Formatting

Once collected, errors will be normalized by the Error Formatter & Normalizer into a standardized JSON schema. This ensures consistency for storage, analysis, and processing.

**Proposed Error Instance Schema:**

```json
{
  "errorId": "unique_error_identifier", // UUID
  "timestamp": "ISO_8601_datetime",
  "sourceSystem": "e.g., semantic_guardrail_v1, user_feedback_ui, consistency_checker_alpha",
  "sourceIdentifier": "e.g., guardrail_id_123, user_id_abc, check_name_xyz",
  "modeSlug": "slug_of_the_mode_active_during_error",
  "taskId": "optional_task_identifier_if_applicable",
  "originalInput": { // Input that led to the error
    "promptToLlm": "Full prompt or significant parts",
    "userInput": "User's request if distinct from promptToLlm",
    "contextSnippets": ["brief context provided to LLM"]
  },
  "erroneousOutput": "The problematic output generated by the LLM",
  "correctedOutput": "Optional: The corrected version, if provided by user or system",
  "errorCategory": "e.g., factual_inaccuracy, formatting_issue, tool_misuse, harmful_content, incomplete_response, style_violation, custom_instruction_ignored",
  "errorSubCategory": "Optional: More granular classification",
  "severity": "low | medium | high | critical", // Assessed by source or later prioritization
  "reasonForError": "Optional: Explanation why it's an error (from guardrail, user, etc.)",
  "detectionMetadata": { // Additional data from the detection source
    // source-specific fields
  },
  "feedbackLoopStatus": "new | prioritized | generalized | integrated | archived",
  "version": "1.0"
}
```

This schema allows for rich data collection, facilitating effective prioritization and pattern extraction.

### 4.3 Error Prioritization and Selection

The Error Prioritizer & Selector module will determine which errors are most beneficial to include in system prompts. This is crucial to keep prompts concise and effective.

*   **Frequency of Updates to Prompts:**
    *   **Batched Updates:** Initially, updates could be batched (e.g., daily or every few hours). This allows for accumulation of errors and more stable analysis before modifying prompts.
    *   **Near Real-time (for critical/high-frequency errors):** A mechanism for "hot-patching" prompts with highly critical or rapidly emerging frequent errors could be implemented. This would require careful thresholds to avoid excessive prompt churn.
    *   The update frequency should be configurable.

*   **Number of Examples per Prompt:**
    *   A limited number of examples (e.g., 3-5) should be included per mode-specific prompt to avoid making prompts overly long, which can degrade LLM performance or increase token costs significantly.
    *   A **sliding window** approach can be used, where older or less relevant examples are rotated out as new, higher-priority ones emerge.
    *   The number should be configurable per mode, as some modes might benefit from more or fewer examples.
    *   Ensure diversity in the selected examples to cover different types of common mistakes for that mode.

*   **Prioritization Algorithm:**
    A scoring system can be used to rank errors:
    *   `Score = (w1 * Frequency) + (w2 * Severity) + (w3 * Recency) + (w4 * UserImpact) + (w5 * Generalizability)`
    *   **Frequency:** How often this error (or a very similar one) occurs. Calculated from the Error Database.
    *   **Severity:** Impact of the error (e.g., `critical` > `high` > `medium` > `low`). Assigned by the error source or an automated classifier.
    *   **Recency:** More recent errors might be given slightly higher weight.
    *   **User Impact/Feedback:** Errors explicitly flagged by users or leading to repeated corrections get higher weight.
    *   **Generalizability:** (If the Generalization module is used) Errors that can be abstracted into broader patterns that cover multiple instances might be prioritized.
    *   Weights (w1-w5) would need to be tuned.
    *   The system will select the top N errors based on this score for each mode.

### 4.4 Error Generalization (Recommended)

The Generalized Error Pattern Extractor module aims to convert specific error instances into more abstract and broadly applicable negative constraints or corrective patterns. This makes the feedback more potent.

*   **Techniques:**
    *   **LLM-based Generalization:** Use an LLM (potentially a smaller, specialized one) to summarize an error instance and its correction into a general rule or pattern.
        *   *Prompt Example for Generalizer LLM:* "Given this error: [erroneousOutput], and this correction: [correctedOutput], and reason: [reasonForError]. Describe a general principle or pattern the original LLM should follow or avoid in the future for mode [modeSlug]."
    *   **Rule-Based Systems:** For common, well-defined error types (e.g., code syntax, specific formatting), rules can be developed to extract patterns.
    *   **Clustering:** Cluster similar error instances (e.g., using embeddings of the erroneous outputs) and then derive a common pattern for each cluster.
*   **Output:** A generalized pattern like: "In [mode_slug], avoid using informal language when discussing technical specifications." or "Ensure all code blocks are correctly triple-backticked with the language identifier."
*   **Storage:** Generalized patterns can be stored and linked to the specific error instances they cover. This helps in prioritizing patterns that address multiple underlying errors.

### 4.5 Integration into System Prompts

The primary method for integrating these error examples will be by updating the mode-specific system prompt override files.

*   **Targeted Prompt File Updater:** This module will:
    1.  Receive the prioritized and formatted (and possibly generalized) error examples from the Prompt Enhancer Module.
    2.  Identify the target mode(s) for each example.
    3.  Read the current content of the corresponding `.roo/system-prompt-${mode_slug}.md` file.
    4.  Inject the error examples into a designated section of the prompt file (see Section 5 for presentation strategies). This might involve finding a placeholder comment (e.g., `<!-- ERROR_EXAMPLES_START -->` and `<!-- ERROR_EXAMPLES_END -->`) or appending to a specific section.
    5.  Write the updated content back to the file.
*   **Atomicity:** File write operations should be atomic to prevent corruption. Write to a temporary file first, then rename.
*   **Versioning/Rollback (Consideration):** For safety, a simple versioning system for these prompt files could be considered, allowing rollback if a prompt update leads to performance degradation.
*   **Alternative - `CustomModesManager`:** If updating `.roomodes` files directly for the `customInstructions` field:
    1.  The updater would parse the `.roomodes` JSON/YAML.
    2.  Modify the `customInstructions` for the target mode.
    3.  Save the `.roomodes` file.
    4.  Potentially call an API endpoint or trigger a mechanism that invokes `CustomModesManager.updateCustomMode(modeSlug, newModeConfig)` to force a cache refresh and propagate changes. This is more complex due to file parsing and potential interactions with the running Roo Code extension. The file-based override is simpler and more decoupled.

## 5. Strategies for Presenting Error Examples Effectively Within Prompts

The way error examples are presented to the LLM is crucial for their effectiveness. The language should be clear, direct, and instructive. The goal is to guide the LLM away from undesirable behaviors and towards correct ones, leveraging in-context learning principles.

### 5.1 General Principles for Presenting Examples

*   **Clarity and Conciseness:** Examples should be easy to understand and to the point. Avoid overly verbose explanations.
*   **Actionable Guidance:** Clearly state what to avoid and, if possible, what to do instead.
*   **Contextual Relevance:** Examples should ideally be relevant to the mode's typical tasks.
*   **Placement:** Error examples should be placed in a dedicated section within the system prompt override file (`.roo/system-prompt-${mode_slug}.md`) or within the `customInstructions` if that method is chosen. This section should be clearly demarcated.
*   **Consistency:** Use a consistent format for all error examples.

### 5.2 Proposed Formats for Error Examples

A dedicated section, clearly marked, should house these examples. For instance, within the `.roo/system-prompt-${mode_slug}.md` file:

```markdown
---
(other prompt frontmatter if any)
---

(Main body of system prompt override)

---
## Error Avoidance Guidance: Learning from Past Mistakes

Based on analysis of previous interactions, please pay close attention to the following patterns to avoid:

---
```

Below are several formats for presenting individual error examples within this section. The `Prompt Enhancer Module` will be responsible for constructing these.

**Format A: Simple Negative Example**

```markdown
**Pattern to Avoid:** [Brief, generalized description of the error pattern, e.g., "Using informal tone for technical explanations."]
*   **Erroneous Output Example:** "[Quote or summary of the bad output]"
*   **Reason (Optional but Recommended):** "[Brief explanation why this is wrong, e.g., 'Violates professional communication standards for this mode.']"
```

**Format B: Negative and Positive Example (Few-Shot Style)**

```markdown
**Error Pattern:** [Brief, generalized description, e.g., "Incorrectly formatting lists."]
*   **AVOID (Erroneous Output):**
    ```
    [Multi-line erroneous output example if applicable]
    ```
*   **INSTEAD, PREFER (Corrected Output / Desired Behavior):**
    ```
    [Multi-line corrected output example]
    ```
*   **Guidance:** "[Optional: Brief explanation of the key difference or principle, e.g., 'Ensure all list items start with a hyphen and a space.']"
```

**Format C: Rule-Based Negative Constraint**

```markdown
**Rule to Follow:** [A direct instruction derived from an error pattern, e.g., "DO NOT use deprecated function `old_function()`. Always use `new_function()` instead."]
*   **Context/Reason:** "[Optional: Why this rule is important, e.g., '`old_function()` can lead to security vulnerabilities.']"
```

**Format D: Question-Answer Style for Clarification**

This can be useful if errors stem from misinterpreting ambiguous instructions.

```markdown
**Scenario/Question:** "[Ambiguous situation or query that previously led to an error]"
*   **Incorrect Interpretation/Output:** "[Erroneous response]"
*   **Correct Interpretation/Guidance:** "[Clarification or desired response/approach]"
```

### 5.3 Dynamic Content and Placeholders

The `Prompt Enhancer Module` will dynamically populate these formats using data from the `Error Database/Store`.

*   `[Brief, generalized description of the error pattern]`: From the `Generalized Error Pattern Extractor` or derived from `errorCategory` and `reasonForError`.
*   `[Quote or summary of the bad output]`: From `erroneousOutput`.
*   `[Brief explanation why this is wrong]`: From `reasonForError`.
*   `[Multi-line corrected output example]`: From `correctedOutput`.

### 5.4 Placement within the Prompt File

The section for error examples should ideally be placed after the main role definition and core instructions but before highly dynamic content like user input, if the prompt structure allows such separation in the override files. If the override file *is* the main prompt, then a logical section break (like `---`) should be used.

**Example structure within `.roo/system-prompt-coder_mode.md`:**

```markdown
You are Coder Mode, an expert software development assistant...
(Core instructions for Coder Mode)

---
## Error Avoidance Guidance: Learning from Past Mistakes

Based on analysis of previous interactions, please pay close attention to the following patterns to avoid:

**Error Pattern:** Using `var` for variable declarations in JavaScript.
*   **AVOID (Erroneous Output):**
    ```javascript
    var x = 10;
    ```
*   **INSTEAD, PREFER (Corrected Output / Desired Behavior):**
    ```javascript
    let x = 10;
    // or
    const y = 20;
    ```
*   **Guidance:** "`var` is function-scoped and can lead to unexpected behavior. Prefer `let` for block-scoped variables that can be reassigned, and `const` for block-scoped variables that should not be reassigned."

**Pattern to Avoid:** Forgetting to include import statements for used libraries.
*   **Erroneous Output Example:** "The code uses `axios.get()` but `axios` is not defined."
*   **Reason:** "Code will fail at runtime due to missing dependency."
---

(Rest of the prompt override, if any)
```

### 5.5 Considerations

*   **Token Count:** The number and length of examples must be carefully managed to stay within token limits and avoid excessive costs. The `Error Prioritizer & Selector` plays a key role here.
*   **LLM Sensitivity:** Different LLMs might respond differently to various negative example formats. Some experimentation might be needed to find the most effective presentation style for Roo Code's target LLMs.
*   **Avoid Over-Constraint:** While providing negative examples is helpful, the prompt should not become so restrictive that it stifles the LLM's creativity or ability to handle novel situations.
```

## 6. Integration Plan for Roo Code

This section outlines how the proposed Error Pattern Feedback Loop system will be integrated into the existing Roo Code architecture and workflow.

### 6.1 Interaction with Existing Error Detection Mechanisms

*   **Semantic Guardrails (Phase 1):**
    *   Guardrails that detect errors will need to be enhanced to send a structured error report (matching the schema in 4.2) to the `Error Collector Service`. This might involve adding a new callback or event emission to the guardrail framework.
*   **Consistency Checks (Phase 1):**
    *   Similar to guardrails, consistency checking mechanisms will report detected inconsistencies to the `Error Collector Service`.
*   **User Feedback Mechanisms:**
    *   The Roo Code UI (webview) will need enhancements to allow users to:
        1.  Flag an LLM response as incorrect/problematic.
        2.  Optionally provide a corrected version of the response.
        3.  Optionally provide a brief reason for the error.
    *   These user-submitted reports will be sent from the webview to an extension-side handler, which then forwards them to the `Error Collector Service`.
*   **Outputs from Phase 1 & 2 (Semantic Drift, Error Containment):**
    *   Mechanisms for Semantic Drift Detection and Error Containment (e.g., sandbox violations, cost anomalies if indicative of quality issues) will be reviewed. If they produce actionable error signals relevant to prompt quality, they will be adapted to feed into the `Error Collector Service`.

### 6.2 Deployment of New Services/Modules

The Error Pattern Feedback Loop introduces several new logical components. Their deployment strategy will depend on their complexity and resource requirements:

*   **Error Collector Service:**
    *   Could be implemented as a lightweight service running locally alongside the Roo Code VS Code extension (e.g., a simple HTTP endpoint or a message queue listener if Roo Code uses an internal bus).
    *   Alternatively, for more robust collection, especially if aggregating data from multiple users (with consent and privacy considerations), this could be a cloud-hosted microservice. For a single-user, local-first approach, a local service is sufficient.
*   **Error Formatter & Normalizer, Error Prioritizer & Selector, Generalized Error Pattern Extractor, Prompt Enhancer Module, Targeted Prompt File Updater:**
    *   These modules primarily involve data processing and logic. They can be implemented as part of a single, periodically run background process or script within the Roo Code extension's environment or as a separate local agent.
    *   This "Feedback Loop Agent" would:
        1.  Poll the `Error Collector Service` or its data store.
        2.  Process new errors through formatting, normalization, prioritization, and generalization.
        3.  Generate the enhanced prompt snippets.
        4.  Update the `.roo/system-prompt-${mode_slug}.md` files.
*   **Error Database/Store:**
    *   For a local-first approach, this could be a local file-based database (e.g., SQLite, or even structured JSON/CSV files managed within the user's workspace, perhaps in the `.roo` directory).
    *   SQLite is a good candidate for structured querying capabilities without requiring a separate server.
    *   The path to this database should be configurable.

### 6.3 Workflow for Prompt Updates

1.  **Error Collection:** Errors are continuously collected and stored in the Error Database.
2.  **Periodic Processing:** The Feedback Loop Agent runs on a schedule (e.g., every few hours, or on Roo Code startup, or triggered manually).
3.  **Error Selection & Enhancement:** The agent queries the Error Database, applies prioritization and generalization, and generates the new set of error examples for each relevant mode.
4.  **Prompt File Update:** The agent updates the `.roo/system-prompt-${mode_slug}.md` files.
    *   It should ensure that the "Error Avoidance Guidance" section is clearly demarcated and that existing content in the override files (if any, outside this section) is preserved.
    *   If the section doesn't exist, it should be created.
5.  **Prompt Reloading:**
    *   As established in Section 2, the `SYSTEM_PROMPT` function in Roo Code likely reads the override files when generating a prompt for a mode. Thus, changes should be picked up automatically when a mode is next used or its prompt is regenerated.
    *   No explicit action might be needed to "push" these updates to the core prompt generation logic, other than modifying the files themselves.

### 6.4 Configuration

*   **Enable/Disable Switch:** A global setting in Roo Code to enable or disable the entire error feedback loop.
*   **Update Frequency:** Configurable schedule for the Feedback Loop Agent.
*   **Number of Examples:** Configurable limit for error examples per prompt.
*   **Prioritization Weights:** (Advanced) Allow tuning of weights in the prioritization algorithm.
*   **Error Database Location:** Path to the local error database.

### 6.5 Security and Privacy Considerations

*   **Local Data:** If all components run locally and store data within the user's workspace (e.g., in `.roo/`), user data (prompts, outputs) remains local.
*   **Generalization:** The generalization step can help anonymize specific details from user inputs/outputs before they are stored as patterns, though the raw errors would still be in the local database.
*   **No External Transmission (Default):** The default design should assume no external transmission of error data unless explicitly configured for a centralized/shared error reporting system (which would require user consent and clear privacy policies).

### 6.6 Phased Rollout (Recommended)

1.  **Phase 1 (Core Implementation):**
    *   Implement Error Collector, Formatter, basic Database (e.g., JSON file), Prioritizer (frequency-based), Prompt Enhancer, and File Updater.
    *   Focus on one or two key error sources (e.g., a specific guardrail and manual user flagging).
    *   Basic presentation format for errors in prompts.
2.  **Phase 2 (Enhancements):**
    *   Implement more sophisticated prioritization and selection.
    *   Introduce the Error Generalization module.
    *   Expand to more error sources.
    *   Refine prompt presentation formats based on initial results.
    *   Implement robust metrics tracking.
3.  **Phase 3 (Advanced Features):**
    *   Consider near real-time updates for critical errors.
    *   Explore UI for managing/reviewing error examples.
    *   Tune LLM sensitivity to different example formats.

## 7. Proposed Metrics for Evaluating the System's Effectiveness

To assess whether the error feedback loop is achieving its goal of reducing error rates and improving LLM performance, a combination of quantitative and qualitative metrics should be tracked by the `Performance Metrics Tracker` module.

### 7.1 Quantitative Metrics

These metrics will be primarily derived from the `Error Database/Store` and logs from error detection systems.

1.  **Overall Error Rate:**
    *   Definition: Total number of detected errors / Total number of LLM interactions (or tasks processed).
    *   Granularity: Tracked globally and per mode.
    *   Goal: Downward trend over time.

2.  **Error Rate per Category/Type:**
    *   Definition: Number of errors of a specific category (e.g., `factual_inaccuracy`, `tool_misuse` from schema in 4.2) / Total interactions.
    *   Granularity: Tracked per mode and globally.
    *   Goal: Reduction in rates for categories targeted by feedback examples.

3.  **Frequency of Specific Error Patterns:**
    *   Definition: How often a particular error pattern (that has been added to prompts) is still detected.
    *   Goal: Significant reduction for patterns actively being fed back. If a pattern persists, it may indicate the feedback is ineffective or the pattern needs refinement.

4.  **Guardrail Trigger Rate:**
    *   Definition: Number of times specific semantic guardrails are triggered / Total interactions.
    *   Granularity: Per guardrail, per mode.
    *   Goal: Reduction in triggers for guardrails whose corresponding error types are being addressed by the feedback loop.

5.  **User Correction Rate:**
    *   Definition: Number of times users explicitly correct or flag an LLM output / Total LLM interactions.
    *   Goal: Downward trend, indicating increased output quality and user satisfaction.

6.  **Task Completion Rate / Success Rate:**
    *   Definition: Percentage of tasks completed successfully without requiring error-related retries or user intervention.
    *   Goal: Upward trend. This is a more holistic measure of LLM utility.

7.  **Average Number of Retries/Re-rolls per Task:**
    *   Definition: Average number of times a user needs to re-roll or re-prompt to get a satisfactory response.
    *   Goal: Downward trend.

8.  **Time to Successful Task Completion:**
    *   Definition: Average time taken to complete a task successfully.
    *   Goal: Reduction, as fewer errors should lead to faster task resolution.

### 7.2 Qualitative Metrics & Evaluation Methods

1.  **Manual Review of LLM Outputs:**
    *   Periodically sample LLM outputs (especially for modes with active feedback) and manually assess their quality against criteria like accuracy, coherence, adherence to instructions, and style.
    *   Compare samples before and after feedback loop implementation or significant updates.

2.  **User Satisfaction Surveys/Feedback:**
    *   Collect qualitative feedback from users regarding perceived improvements in LLM reliability and output quality for different modes.
    *   Specific questions about whether the LLM seems to be avoiding common pitfalls.

3.  **A/B Testing (Advanced):**
    *   If feasible, conduct A/B tests where one group of users (or one instance of Roo Code) operates with the error feedback loop active, and another operates without it (or with an older set of examples).
    *   Compare quantitative metrics between the two groups. This provides a more controlled way to measure impact.

4.  **Analysis of "Stubborn" Errors:**
    *   Investigate error patterns that persist despite being included in feedback. This can provide insights into:
        *   Ineffective prompt wording for the feedback.
        *   LLM limitations in understanding certain negative constraints.
        *   Need for more fundamental changes to the mode's role definition or tools.

### 7.3 Data Collection and Reporting

*   The `Performance Metrics Tracker` module will be responsible for:
    *   Aggregating data from the `Error Database/Store` and other relevant logs (e.g., telemetry from Roo Code interactions).
    *   Calculating the defined metrics periodically.
*   A **Dashboard** (can be a simple report generated periodically or a more interactive UI) should display trends for these metrics over time. This allows for ongoing monitoring of the feedback loop's effectiveness.
*   The dashboard should allow filtering by mode to understand mode-specific improvements.

By tracking these metrics, the development team can understand the impact of the dynamic prompt enhancements, identify areas where the feedback is most/least effective, and make data-driven decisions to further refine the system.

## 8. Examples of Enhanced System Prompts

This section provides illustrative examples of how a mode's system prompt override file (`.roo/system-prompt-${mode_slug}.md`) might look after being enhanced with error examples by the `Targeted Prompt File Updater`. These examples assume the use of the presentation strategies outlined in Section 5.

### Example 1: Enhanced `system-prompt-code_mode.md`

Suppose `code_mode` has exhibited issues with:
1.  Incorrectly using `var` instead of `let`/`const` in JavaScript.
2.  Generating Python code that misses `self` in class methods.
3.  Providing incomplete file paths when asked to list project files.

The `.roo/system-prompt-code_mode.md` might be updated to include:

```markdown
---
title: Roo Code - Coder Mode System Prompt Override
base_role_definition_slug: code # Indicates this augments the built-in code mode
version: 1.1
last_error_update: 2025-05-19T14:30:00Z
---

You are Roo, an expert AI programmer. Your primary function is to assist users with coding tasks, including writing new code, debugging, refactoring, and explaining code across various programming languages. Adhere to best practices and provide clean, efficient, and well-documented code.

(Other core instructions for Coder Mode, tool usage guidelines, etc., would typically be here if this file fully overrides the base prompt. If it only augments, this part might be minimal, relying on the base role definition.)

---
## Error Avoidance Guidance: Learning from Past Mistakes

Based on analysis of previous interactions, please pay close attention to the following patterns to avoid:

---

**Error Pattern:** Using `var` for variable declarations in modern JavaScript.
*   **AVOID (Erroneous Output Example):**
    ```javascript
    function exampleScope() {
      if (true) {
        var x = 10;
      }
      console.log(x); // x is 10, which can be unexpected
    }
    ```
*   **INSTEAD, PREFER (Corrected Output / Desired Behavior):**
    ```javascript
    function exampleScope() {
      if (true) {
        let x = 10; // or const x = 10;
      }
      // console.log(x); // This would be a ReferenceError, x is not defined here
    }
    ```
*   **Guidance:** "`var` is function-scoped and can lead to hoisting issues and unexpected behavior. Prefer `let` for block-scoped variables that can be reassigned, and `const` for block-scoped variables that should not be reassigned."

---

**Pattern to Avoid:** Omitting `self` as the first parameter in Python instance methods.
*   **Erroneous Output Example:**
    ```python
    class MyClass:
        def my_method(value): # Missing self
            print(value)
    ```
*   **Reason:** Python instance methods require `self` to refer to the instance.
*   **Correct Approach:**
    ```python
    class MyClass:
        def my_method(self, value):
            print(self, value)
    ```

---

**Rule to Follow:** When asked to list files or provide file paths, always provide full paths relative to the project root, or clearly state the assumed base directory if providing relative paths. Do not provide ambiguous or incomplete paths.
*   **Context/Reason:** Incomplete paths are not actionable and require clarification, slowing down the user.
*   **Erroneous Output Example (if asked for 'main.py' in 'src/app'):** "Found main.py"
*   **Correct Output Example:** "Found `src/app/main.py` (relative to project root)."

---

(Any further sections of the prompt override file)
```

### Example 2: Enhanced `system-prompt-research_mode.md`

Suppose `research_mode` has shown tendencies to:
1.  Provide overly long summaries from a single source.
2.  Not clearly attributing factual claims.

The `.roo/system-prompt-research_mode.md` might be updated:

```markdown
---
title: Roo Code - Deep Research Mode System Prompt Override
base_role_definition_slug: deep-research-agent
version: 1.0
last_error_update: 2025-05-19T15:00:00Z
---

You are Roo, a Deep Information Discovery and Analysis Specialist. Your core capabilities include comprehensive research methodology, analytical framework application, and knowledge integration. You conduct structured, multi-phase research.

(Other core instructions for Research Mode)

---
## Error Avoidance Guidance: Learning from Past Mistakes

Based on analysis of previous interactions, please pay close attention to the following patterns to avoid:

---

**Pattern to Avoid:** Creating summaries that are too long or closely paraphrase a single source.
*   **Erroneous Output Example:** (If a source said "The quick brown fox jumps over the lazy dog near the river bank.") "A speedy, auburn-colored fox was observed leaping above a lethargic canine in the vicinity of the watercourse's edge."
*   **Reason:** This is too close to the original and too lengthy for a concise summary point. Summaries should be transformative and brief.
*   **Correct Approach:** "A fox was seen jumping over a dog by the river." (And ensure this is one of potentially several points from different sources, not the sole content).
*   **Guidance:** Summaries from a single source should be NO MORE THAN 2-3 SENTENCES and use substantially different wording. Integrate information from multiple sources for comprehensive answers.

---

**Rule to Follow:** All factual claims or specific data points must be clearly attributed to their source. If a direct quote is used, it must be under 25 words and enclosed in quotation marks, followed by citation.
*   **Context/Reason:** Maintaining academic integrity and allowing users to verify information is paramount.
*   **Erroneous Output Example:** "Studies show that 75% of users prefer dark mode." (Missing citation)
*   **Correct Output Example:** "According to a study by ExampleCorp (2023), '75% of users prefer dark mode'." OR "A study by ExampleCorp (2023) found that three-quarters of users opt for dark mode interfaces."

---
```

### Notes on Examples:

*   The `---` separators are used for clarity and to demarcate the dynamically inserted error guidance section. The `Targeted Prompt File Updater` would manage the content between these markers.
*   The examples use a mix of the formats proposed in Section 5.
*   The `last_error_update` timestamp in the frontmatter is a suggestion for tracking when the error examples were last refreshed.
*   These examples are illustrative. The actual content would be dynamically generated based on the prioritized errors in the `Error Database/Store`.
*   The initial part of the override file might contain mode-specific instructions that are not part of the base `roleDefinition` but are considered more static than the error examples. The error examples section should be appended to or inserted into a designated part of this file.

---
*This document is a living draft and will be updated as research progresses.*