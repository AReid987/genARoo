---
title: Specification for Enhanced Task Isolation in Boomerang
task_id: task_2.1
date: 2025-05-19
last_updated: 2025-05-19
status: DRAFT
owner: deep-research-agent
---

# Specification for Enhanced Task Isolation in Boomerang

## Objective
This document specifies mechanisms for implementing stricter task boundaries and verification hooks within Roo Code's Boomerang task system. The goal is to prevent error propagation between parent, child, and sibling tasks, thereby enhancing the overall robustness and reliability of the system.

## Inputs
-   `research/synthesis/boomerang_task_system_analysis.md`: Provides an analysis of the current Boomerang architecture and identifies existing error propagation risks.
-   Research on task isolation techniques:
    -   Data validation and sanitization.
    -   Immutable task contexts and copy-on-write mechanisms.
    -   Resource sandboxing and limitations.
    -   Schema-defined contracts for task inputs and outputs.
-   Roo Code repository structure and conventions.

## Process

### 1. Analysis of Current Task Boundary Mechanisms in Boomerang

The Boomerang task system, as detailed in `boomerang_task_system_analysis.md`, primarily relies on the `Task` class (`src/core/task/Task.ts`) and the `new_task` tool (`src/core/tools/newTaskTool.ts`) to manage task creation, delegation, and communication.

**Current Boundary Implementations:**
-   **Task Encapsulation:** Each task runs within its own `Task` instance, holding its state, message history, and mode context.
-   **Mode Switching:** Tasks operate in specific modes, and the system attempts to restore the parent's mode upon child task completion. The `pausedModeSlug` property in the `Task` class stores the mode to return to.
-   **Explicit Communication Channel:** Child task results are passed back to the parent via the `resumePausedTask` method, which adds the result as a message (`[new_task completed] Result: ...`) to the parent's conversation history.

**Limitations and Weaknesses:**
-   **Implicit Data Contracts:** There are no formal schemas or contracts for the `message` passed to `new_task` or the `lastMessage` (result) returned by `resumePausedTask`. This means tasks rely on conventions or descriptive instructions, which can be misinterpreted or lead to malformed data exchange.
-   **Mutable Shared State (Potential):** While task instances are separate, the exact mechanism for passing complex context objects or data is not fully detailed in the analysis. If context objects are passed by reference and are mutable, a child task could inadvertently modify a parent's or sibling's state.
-   **No Resource Constraints:** Child tasks do not appear to have explicit resource limitations (CPU, memory, file access beyond mode restrictions). A misbehaving child task could potentially exhaust system resources.
-   **Limited Input/Output Validation:** Beyond basic parameter validation in `newTaskTool.ts` (e.g., mode existence), there's no systematic validation or sanitization of the content of task inputs or outputs. This can lead to errors if a task produces unexpected or malformed results.
-   **Error Propagation:** As identified in `boomerang_task_system_analysis.md` (Section 3), errors in task creation, pausing, resumption, or mode switching can propagate and impact parent tasks or lead to inconsistent states. For example, a failure in `resumePausedTask` could lead to lost results.

### 2. Proposed Mechanisms for Stricter Task Isolation

To address the identified limitations, the following mechanisms are proposed:

#### 2.1 Schema-Defined Task Contracts & Validation
-   **Concept:** Define explicit JSON Schemas for the inputs (`message` content) and outputs (`result` content) for different types of tasks or modes.
-   **Implementation:**
    -   Store schemas (e.g., in a `src/core/task/schemas/` directory).
    -   The `new_task` tool should validate the provided `message` against the relevant input schema for the target mode/task type before task creation.
    -   Before `resumePausedTask` integrates a child's result, the result (`lastMessage`) should be validated against the expected output schema for that child task.
-   **Benefit:** Enforces clear data contracts, prevents malformed data exchange, and allows for early detection of contract violations.

#### 2.2 Immutable Task Inputs (Contextual Data)
-   **Concept:** Ensure that any complex contextual data passed from a parent to a child task is treated as immutable by the child.
-   **Implementation:**
    -   When passing objects as part of the task `message`, use techniques to ensure immutability (e.g., deep cloning, using immutable data structures if available in the language, or by convention and enforcement through linters/reviews).
    -   Alternatively, implement a copy-on-write strategy for larger context objects. The child receives a reference, but any attempt to modify it triggers a deep copy specific to that child.
-   **Benefit:** Prevents child tasks from inadvertently modifying the parent's or sibling tasks' state, reducing side effects.

#### 2.3 Output Sanitization
-   **Concept:** Before a child task's result is integrated by the parent, sanitize it to remove any potentially harmful or unexpected elements that are not part of the defined output schema.
-   **Implementation:**
    -   Integrate a sanitization step in `resumePausedTask` after schema validation. This could involve stripping unknown properties or ensuring string lengths are within limits.
-   **Benefit:** Adds an extra layer of protection against malformed or malicious outputs.

#### 2.4 Resource Quotas and Sandboxing (Future Consideration)
-   **Concept:** For tasks that involve external tool execution or potentially resource-intensive operations, implement resource limits or execute them in a sandboxed environment.
-   **Implementation (More Complex):**
    -   This would require more significant architectural changes, potentially involving OS-level sandboxing (e.g., containers, separate processes with restricted permissions) or language-specific sandboxing libraries.
    -   Define resource quotas (CPU time, memory usage, network access) for certain task types.
-   **Benefit:** Prevents runaway tasks from destabilizing the system. This is a more advanced feature that could be phased in.

### 3. Design for Verification Hooks

Verification hooks are checkpoints in the Boomerang lifecycle to explicitly check boundary integrity and task output/input validity.

#### 3.1 Pre-Task-Creation Hook
-   **Placement:** Within `newTaskTool.ts`, before `provider.initClineWithTask()`.
-   **Function:**
    1.  **Input Schema Validation:** Validate the `message` (task input) against the defined input schema for the target mode/task type.
    2.  **Context Integrity Check (Optional):** If complex context is passed, verify its basic structure or presence of required fields.
-   **Action on Failure:** Reject task creation, log the error, and inform the calling (parent) task.

#### 3.2 Post-Task-Execution / Pre-Result-Integration Hook
-   **Placement:** Within `Task.ts`, at the beginning of `resumePausedTask(lastMessage)`, before the result is added to the conversation history or mode is restored.
-   **Function:**
    1.  **Output Schema Validation:** Validate the `lastMessage` (child task's result) against the defined output schema for that child task.
    2.  **Output Sanitization:** Sanitize the `lastMessage` based on the schema or predefined rules.
    3.  **Criticality Check (Optional):** Assess if the result indicates a critical failure in the child task that should prevent parent resumption or trigger specific error handling.
-   **Action on Failure:**
    -   Log the validation/sanitization error.
    -   Decide on a strategy:
        -   Attempt to use a "safe" default or error placeholder as the result.
        -   Propagate a specific error status to the parent task instead of the malformed result.
        -   Place the parent task into an error state.

#### 3.3 Pre-Mode-Restoration Hook
-   **Placement:** Within `Task.ts`, in `resumePausedTask`, just before the original mode (`this.pausedModeSlug`) is restored.
-   **Function:**
    1.  **Verify Mode Integrity:** Check if `this.pausedModeSlug` is valid and known.
    2.  **Check for Mode-Specific Cleanup (from child):** If the child task's mode required specific cleanup actions that should be confirmed before the parent's mode is restored.
-   **Action on Failure:** Log the error. Attempt to restore to a default safe mode or escalate the error if mode restoration is critical and fails.

### 4. Specific Recommendations for Enhancing Task Boundaries in Roo Code

Based on `boomerang_task_system_analysis.md` and the proposed mechanisms:

1.  **Modify `src/core/tools/newTaskTool.ts`:**
    *   Integrate the "Pre-Task-Creation Hook."
    *   Implement input schema validation for the `message` parameter based on the target `mode`.
    *   Ensure deep cloning or copy-on-write for any complex objects passed within the `message` to enforce immutability from the child's perspective.

2.  **Modify `src/core/task/Task.ts`:**
    *   **In `resumePausedTask()`:**
        *   Integrate the "Post-Task-Execution / Pre-Result-Integration Hook."
        *   Implement output schema validation and sanitization for `lastMessage`.
        *   Integrate the "Pre-Mode-Restoration Hook."
    *   **Task Input Handling:** When a task starts (e.g., in `initiateTaskLoop` or equivalent), if it receives complex input, ensure it operates on a copy or treats the input as immutable.

3.  **Develop a Schema Management System:**
    *   Create a dedicated directory (e.g., `src/core/task/schemas/`) for JSON schemas defining task inputs and outputs.
    *   Schemas could be organized by mode or task type (e.g., `research_mode_input.schema.json`, `code_mode_output.schema.json`).
    *   Implement utility functions for loading and validating against these schemas.

4.  **Update Orchestrator Mode (`src/shared/modes.ts`):**
    *   Ensure the orchestrator is aware of and provides inputs conforming to the defined schemas when using `new_task`.
    *   Update its logic to handle potential schema validation failures from child tasks (e.g., if a child task returns a malformed result that fails validation in `resumePausedTask`).

5.  **Logging and Error Reporting:**
    *   Enhance logging around task boundaries to record validation successes/failures.
    *   Ensure that boundary violation errors are clearly reported and traceable.

### 5. Examples of Error Propagation Prevention

#### Example 1: Malformed Child Task Output
-   **Scenario (Current):** A child 'code-generation' task is expected to return a JSON string with a `code` field. Due to a bug, it returns an XML string or a JSON string missing the `code` field. The parent task, expecting the JSON, tries to parse it or access `result.code` and crashes or behaves unpredictably.
-   **Prevention (Enhanced):**
    -   The "Post-Task-Execution Hook" in `resumePausedTask` validates the child's output against `code_generation_output.schema.json`.
    -   Validation fails. The system logs the error.
    -   Instead of passing the malformed XML/JSON to the parent, it might pass a standardized error object (e.g., `{ "error": "Invalid output format from child task X", "details": "Schema validation failed" }`) or a default safe value.
    -   The parent task can then handle this specific error gracefully instead of crashing.

#### Example 2: Child Task Corrupting Shared Context
-   **Scenario (Potential Current):** A parent task passes a configuration object by reference to multiple child tasks. Child Task A mistakenly modifies a property in this configuration object that Child Task B relies on, leading to incorrect behavior in Child Task B.
-   **Prevention (Enhanced):**
    -   With "Immutable Task Inputs," Child Task A receives a deep copy of the configuration object (or the object itself is immutable).
    -   Any modifications Child Task A makes are to its own copy and do not affect the original configuration object used by the parent or Child Task B.

#### Example 3: Invalid Input to Child Task
-   **Scenario (Current):** The orchestrator instructs a 'file-writing' task to write content to a path, but mistakenly provides a number instead of a string for the `filePath` parameter within the `message`. The `file-writing` task attempts to use the number as a path and fails at runtime, potentially with an unhandled exception.
-   **Prevention (Enhanced):**
    -   The "Pre-Task-Creation Hook" in `newTaskTool.ts` validates the `message` against `file_writing_input.schema.json`.
    -   The schema specifies `filePath` must be a string. Validation fails.
    -   Task creation is rejected, and the orchestrator is notified of the invalid input, preventing the `file-writing` task from even starting with bad data.

## Dependencies
-   Clear definition and implementation of a schema validation library/utility within Roo Code.
-   Agreement on the structure and location of task input/output schemas.
-   Modifications to core task management files (`Task.ts`, `newTaskTool.ts`).

## Next Actions
-   Refine the proposed schema structure and choose a validation library.
-   Prototype the verification hooks in `newTaskTool.ts` and `Task.ts`.
-   Develop initial schemas for a few key task types/modes as a proof of concept.
-   Update the memory system with these findings and proposals.