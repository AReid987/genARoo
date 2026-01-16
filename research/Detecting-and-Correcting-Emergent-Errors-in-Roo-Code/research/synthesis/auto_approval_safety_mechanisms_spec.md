---
title: Implementation Specification for Conditional Auto-Approval in Roo Code
task_id: Task 3.1
date: 2025-05-19
last_updated: 2025-05-19
status: DRAFT
owner: deep-research-agent
---

## 1. Introduction

This document outlines the design for enhanced auto-approval safety mechanisms within Roo Code. The goal is to move beyond simple on/off toggles and implement a conditional auto-approval system that leverages various signals to determine whether an automated action can proceed safely or requires manual human intervention. This aligns with the project's objective to develop robust error correction and prevention strategies for Roo Code.

## 2. Analysis of Current Auto-Approval Mechanisms in Roo Code

Based on a review of the Roo Code codebase (primarily `Roo-Code/src/core/webview/webviewMessageHandler.ts`), the existing auto-approval functionalities are as follows:

*   **Global Auto-Approval Toggle (`autoApprovalEnabled`):**
    *   A boolean flag that acts as a master switch for all auto-approval functionalities. If `false`, all actions require manual approval unless overridden by a more specific "always allow" setting.
    *   Location: `Roo-Code/src/core/webview/webviewMessageHandler.ts` (lines 922-924).

*   **Per-Tool "Always Allow" Toggles for MCP Tools (`toggleToolAlwaysAllow`):**
    *   Users can pre-approve specific tools provided by MCP (Model Context Protocol) servers. This allows certain trusted tools to operate without repeated manual approval.
    *   Location: `Roo-Code/src/core/webview/webviewMessageHandler.ts` (lines 447-463).

*   **Global "Always Allow" Toggles for Action Categories:**
    *   Separate boolean flags exist for broader categories of actions, such as:
        *   `alwaysAllowReadOnly`
        *   `alwaysAllowReadOnlyOutsideWorkspace`
        *   `alwaysAllowWrite`
        *   `alwaysAllowWriteOutsideWorkspace`
        *   `alwaysAllowExecute`
        *   `alwaysAllowBrowser`
        *   `alwaysAllowMcp` (general MCP operations)
        *   `alwaysAllowModeSwitch`
        *   `alwaysAllowSubtasks`
    *   Location: `Roo-Code/src/core/webview/webviewMessageHandler.ts` (lines 132-167).

*   **Default Behavior (Manual Approval):**
    *   If an action is not covered by an active global auto-approval setting or a specific "always allow" toggle, Roo Code defaults to requiring explicit user approval before execution. This is often facilitated by an `askApproval` function that presents the proposed action (e.g., a diff for file changes) to the user.
    *   Reference: `Roo-Code/src/core/prompts/sections/tool-use.ts` (line 6).

**Limitations of the Current System:**

The current system provides basic control but lacks nuanced, context-aware decision-making for auto-approval. It does not incorporate dynamic factors such as:
*   Confidence levels of LLM-generated actions.
*   Assessed risk or potential impact of an action.
*   Feedback from other error detection and containment mechanisms developed in Phases 1 and 2 (e.g., semantic guardrails, task boundary checks, sandbox results, cost anomaly detection).

This task aims to address these limitations by designing a more sophisticated conditional auto-approval framework.

## 3. Design of Enhanced Safeguards and Conditional Auto-Approval Logic

The enhanced auto-approval system will introduce a layered approach to decision-making, moving beyond simple boolean flags to a more granular and context-sensitive process.

### 3.1. Core Principles
*   **Safety First:** The primary goal is to prevent errors and unintended consequences from automated actions.
*   **User Control & Transparency:** Users should understand why an action was auto-approved or flagged for review and have mechanisms to customize the system's behavior.
*   **Modularity & Extensibility:** The system should be designed to easily integrate new signals and adapt to evolving capabilities of Roo Code.
*   **Context-Awareness:** Decisions should be based on a comprehensive understanding of the proposed action, its potential impact, and signals from various monitoring components.

### 3.2. Key Components of the Conditional Auto-Approval System

#### 3.2.1. Risk Assessment Module
This module will be responsible for evaluating the potential risk associated with a proposed automated action. It will consider:
*   **Action Type:** (e.g., file read, file write, command execution, API call).
*   **Target Resource:** (e.g., critical system file, user data, external service, specific file paths, command patterns).
*   **Potential Impact:** (e.g., data loss, security vulnerability, high cost, system instability, irreversible changes).
    *   A predefined, configurable mapping of action types, target characteristics (e.g., regex for paths/commands), and known sensitive operations to risk levels (e.g., Low, Medium, High, Critical) will be used.
    *   This mapping should be user-configurable to adapt to specific project sensitivities.

#### 3.2.2. Confidence Aggregation Module
This module will gather and weigh confidence scores and safety signals from various sources. The aggregation logic could involve weighted averages or a rules-based system.
*   **LLM Output Confidence:** If the LLM provides a confidence score for its generated action/tool use, this will be a primary input. (Requires LLM to support this).
*   **Semantic Guardrail Output (Task 1.1):** Boolean flags or numerical scores indicating potential semantic drift or policy violations.
*   **Consistency Check Output (Task 1.2):** Signals (e.g., anomaly scores) regarding deviations from expected behavior or patterns.
*   **Task Boundary Check Output (Task 2.1):** Boolean flags indicating if an action is attempting to operate outside its defined scope.
*   **Sandbox Execution Results (Task 2.3):** Categorical results (Success, SuccessWithWarnings, Failure) from a trial run in a sandboxed environment.
*   **Cost Anomaly Detection (Task 2.2):** Flags or scores for actions predicted to incur unusually high costs or exceed budget thresholds.
*   **Action History & User Feedback:** Past approval/rejection rates for similar actions or by the same agent/mode could be a factor.

#### 3.2.3. User Preference & Configuration Layer
Users will be able to define their risk tolerance and configure auto-approval behavior through settings:
*   **Global Risk Tolerance Setting:** An enum (e.g., `Conservative`, `Balanced`, `Permissive`). This will influence the thresholds used in the decision logic.
    *   `Conservative`: Favors manual review for most non-trivial actions.
    *   `Balanced`: Aims for a mix of automation and safety, requiring review for higher-risk or lower-confidence actions.
    *   `Permissive`: Allows more auto-approval, reserving manual review for critical risks or very low confidence.
*   **Per-Action Type Overrides:** Allow users to specify stricter or more lenient auto-approval rules for specific types of actions (e.g., "always require manual approval for `execute_command` on system paths identified by a regex").
*   **Per-Tool Overrides (Extending existing MCP functionality):** More granular control over individual tools, potentially including thresholds for confidence or risk specific to that tool.
*   **Confidence Thresholds:** User-defined minimum confidence scores (overall or per signal type) required for auto-approval at different risk levels.
*   **"Cool-down" Periods:** After a certain number of auto-approved actions or a high-risk manual intervention, the system might temporarily increase scrutiny or require manual approval for subsequent actions.

#### 3.2.4. Decision Engine
The core logic that determines whether an action is auto-approved, requires manual review, or is outright rejected.
*   It will take inputs from the Risk Assessment Module, Confidence Aggregation Module, and User Preference Layer.
*   The logic will use a configurable, potentially weighted, scoring system or a decision tree/ruleset.
*   **Example Decision Logic (Illustrative):**
    1.  `IF current_global_auto_approval_setting IS false AND NOT (per_tool_always_allow IS true) THEN require_manual_approval` (respect existing global off switch)
    2.  `Calculate overall_confidence_score based on weighted inputs from Confidence Aggregation Module.`
    3.  `Determine action_risk_level from Risk Assessment Module.`
    4.  `Retrieve user_risk_tolerance and specific_overrides.`
    5.  `IF action_risk_level IS Critical THEN require_manual_approval`
    6.  `ELSE IF action_risk_level IS High:`
        *   `IF overall_confidence_score < user_threshold_high_risk_confidence OR semantic_guardrail_flag IS severe OR sandbox_result IS Failure THEN require_manual_approval`
        *   `ELSE IF user_risk_tolerance IS Conservative THEN require_manual_approval`
        *   `ELSE auto_approve`
    7.  `ELSE IF action_risk_level IS Medium:`
        *   `IF overall_confidence_score < user_threshold_medium_risk_confidence OR task_boundary_violation IS true THEN require_manual_approval`
        *   `ELSE IF user_risk_tolerance IS Conservative AND overall_confidence_score < (user_threshold_medium_risk_confidence + 0.1) THEN require_manual_approval`
        *   `ELSE auto_approve`
    8.  `ELSE IF action_risk_level IS Low:`
        *   `IF overall_confidence_score < user_threshold_low_risk_confidence THEN require_manual_approval`
        *   `ELSE auto_approve`
    9.  `IF any_override_rule_triggers_manual_review THEN require_manual_approval`

### 3.3. Information Flow
1.  Roo proposes an automated action (e.g., a tool use).
2.  The action details (tool name, parameters, target) are passed to the **Risk Assessment Module**. It outputs an `action_risk_level`.
3.  Relevant signals (LLM confidence, guardrail outputs, sandbox results, cost estimates, boundary checks, consistency scores) are collected by the **Confidence Aggregation Module**. It outputs an `overall_confidence_score` and individual signal statuses.
4.  User preferences (global risk tolerance, overrides, thresholds) are retrieved from the **User Preference & Configuration Layer**.
5.  The **Decision Engine** evaluates `action_risk_level`, `overall_confidence_score`, individual signals, and user preferences based on its rule set.
6.  The Decision Engine outputs one of three decisions:
    *   **Auto-Approve:** The action proceeds automatically. A log entry is made detailing the reasons for auto-approval (e.g., high confidence, low risk).
    *   **Require Manual Review:** The action is flagged. The UI presents the proposed action, the assessed risk, key confidence signals (especially any that were low or concerning), and the specific rule(s) that triggered the manual review. The user can then approve or reject.
    *   **Reject (Optional but Recommended for Critical Failures):** For actions that fail critical safety checks (e.g., severe semantic guardrail violation on a high-risk action, sandbox failure indicating definite harm), the system might automatically reject the action and inform the user with a clear explanation.

## 4. Criteria for Triggering Manual Review vs. Auto-Approval

Manual review will be triggered under the following general conditions, refined by user configuration:

1.  **High-Risk Actions:**
    *   Actions classified as "Critical" risk by the Risk Assessment Module will always require manual review, regardless of confidence scores (unless explicitly overridden by a user setting for a very specific, understood scenario).
    *   Actions classified as "High" risk will require manual review if confidence scores are below a user-defined threshold for high-risk actions, or if specific negative signals (e.g., sandbox failure, severe guardrail warning) are present.

2.  **Low Confidence Scores:**
    *   If the aggregated confidence score from the Confidence Aggregation Module falls below a user-defined threshold for the action's risk level (Low, Medium, High).
    *   If a critical individual signal (e.g., LLM confidence, if available and reliable) is exceptionally low.

3.  **Negative Safety Signals:**
    *   **Semantic Guardrail Violation (Task 1.1):** A "severe" violation, or a "moderate" violation on a Medium/High-risk action.
    *   **Consistency Check Anomaly (Task 1.2):** A high anomaly score, particularly for actions that modify state or interact with external systems.
    *   **Task Boundary Violation (Task 2.1):** Any detected attempt to operate outside defined task boundaries.
    *   **Sandbox Execution Failure (Task 2.3):** If a sandboxed dry-run of the action results in errors or unintended side effects. "SuccessWithWarnings" might also trigger review for Medium/High-risk actions.
    *   **Cost Anomaly Detected (Task 2.2):** If the action is predicted to exceed cost thresholds or shows anomalous cost patterns, especially if not previously approved for similar costs.

4.  **User-Defined Rules & Overrides:**
    *   If the action matches a user-defined rule that explicitly requires manual approval (e.g., "all `apply_diff` operations on `*.config` files require review").
    *   If the user's global risk tolerance is set to "Conservative," leading to lower thresholds for triggering manual review.

5.  **Ambiguity or Insufficient Information:**
    *   If the Risk Assessment Module or Confidence Aggregation Module cannot confidently assess the risk or gather sufficient signals for a reliable decision.

6.  **First-Time Complex Actions:**
    *   For novel combinations of tools, parameters, or targets that haven't been frequently auto-approved successfully in the past, the system might default to manual review initially, learning from user approvals.

7.  **"Cool-down" Period Trigger:**
    *   If a recent series of actions involved manual intervention due to errors, or if a high number of actions were auto-approved in a short period, the system might temporarily increase scrutiny.

**Conversely, auto-approval is favored when:**
*   Risk level is Low or Medium.
*   Aggregated confidence is high (above user-defined thresholds for that risk level).
*   No significant negative safety signals are present from guardrails, boundary checks, sandbox, or cost analysis.
*   The action aligns with user's "Permissive" or "Balanced" risk tolerance (for Medium risk actions).
*   The action type and target have a history of successful auto-approvals.

## 5. Integration Strategy with Roo Code Workflow (including Boomerang Task System)

The conditional auto-approval system will be integrated as a distinct step in the action execution lifecycle within Roo Code, particularly before any tool with potential side-effects is used.

1.  **Hook into Action/Tool Invocation:**
    *   When Roo's core logic (e.g., `presentAssistantMessage` or the part of `Cline` that handles tool use) is about to execute a tool, it will first pass the proposed tool call (tool name, parameters) to the Conditional Auto-Approval (CAA) service.

2.  **CAA Service Execution:**
    *   The CAA service will perform the Risk Assessment, Confidence Aggregation, and consult User Preferences.
    *   It will then use the Decision Engine to determine the outcome: Auto-Approve, Require Manual Review, or Reject.

3.  **Handling "Auto-Approve":**
    *   If "Auto-Approve," the CAA service returns a success status, and the original tool execution proceeds as planned.
    *   A detailed log entry is made, including the factors that led to auto-approval (e.g., `risk: Low, confidence: 0.95, guardrail_status: OK`).

4.  **Handling "Require Manual Review":**
    *   If "Require Manual Review," the CAA service halts the direct execution of the tool.
    *   It then triggers the existing user approval mechanism (e.g., `cline.ask(...)` or a similar UI interaction).
    *   The information presented to the user for manual approval will be enhanced to include:
        *   The proposed action (as currently done, e.g., diff view).
        *   The assessed risk level (Low, Medium, High, Critical).
        *   Key signals that contributed to flagging the review (e.g., "Low LLM confidence: 0.6", "Semantic Guardrail: Moderate warning - potential policy deviation", "Sandbox: SuccessWithWarnings - minor unexpected console output").
        *   A brief explanation of why manual review is requested (e.g., "High-risk action with moderate confidence").
    *   The user's decision (approve/reject) is then processed. If approved, the tool executes. If rejected, the action is cancelled, and Roo is informed to potentially try an alternative.

5.  **Handling "Reject":**
    *   If the CAA service decides to "Reject" an action (e.g., critical risk with clear failure signals), the tool execution is cancelled.
    *   A message is sent to the user explaining the rejection and the critical reasons. Roo is informed to reconsider its approach.

6.  **Integration with Boomerang Task System:**
    *   **Subtask Creation:** When the Orchestrator mode creates a subtask, the CAA settings relevant to that subtask's scope or the specialist mode's capabilities could be considered or even passed as part of the task context if granular control is needed.
    *   **Action within Subtasks:** Actions performed by specialist modes within a subtask will go through the same CAA process.
    *   **Boomerang Return:** If a specialist mode's action is flagged for manual review, this review process must complete before the task can be considered "done" and boomerang back. The outcome of the manual review (approved/rejected) will influence the subtask's result.
        *   If an action critical to the subtask is rejected by the user (or the CAA system), the subtask might fail or require re-planning by the specialist mode or escalation back to the Orchestrator.
    *   The `boomerang-state.json` could potentially log key CAA decisions or manual intervention points related to tasks.

7.  **Configuration Management:**
    *   User preferences for the CAA system (risk tolerance, thresholds, overrides) will be managed through the existing Roo Code settings UI and stored appropriately (e.g., in global state or configuration files).
    *   The Risk Assessment Module's mappings (action type to risk) should also be configurable, potentially with a base set of defaults.

8.  **Logging:**
    *   All CAA decisions (auto-approved, manual review triggered, rejected), along with the primary contributing factors (risk score, confidence scores, specific signals), will be logged for audit, debugging, and system improvement purposes. This will be part of the standard Roo Code logging.

## 6. Examples of Scenarios and Prevented Errors

*(This section will be populated with concrete examples after further refinement of the logic.)*

### Scenario 1: Preventing Incorrect File Deletion
*   **Proposed Action:** `execute_command` with `rm -rf /critical/system/path` (generated due to LLM misinterpretation).
*   **CAA Process:**
    *   Risk Assessment: Identifies `rm -rf` on a root-level path as "Critical" risk.
    *   Decision Engine: `IF risk_level IS Critical THEN require_manual_approval`.
*   **Outcome:** Action flagged for manual review. User sees the dangerous command and rejects it.
*   **Error Prevented:** Accidental deletion of critical system files.

### Scenario 2: Intervening on a Costly API Call
*   **Proposed Action:** `use_mcp_tool` for a data analysis service with parameters that would result in processing a massive, unintended dataset.
*   **CAA Process:**
    *   Cost Anomaly Detection (Task 2.2): Flags the action for potentially high cost.
    *   Risk Assessment: May classify as "Medium" or "High" risk due to cost.
    *   Confidence Aggregation: Receives high cost warning.
    *   Decision Engine: Triggers manual review due to cost anomaly signal and risk level.
*   **Outcome:** User is alerted to the potential high cost before execution and can modify or reject the action.
*   **Error Prevented:** Unexpectedly large bill from an API service.

### Scenario 3: Auto-Approving a Safe, High-Confidence Code Refactor
*   **Proposed Action:** `apply_diff` to a non-critical source file, changing a variable name consistently. LLM confidence is high (e.g., 0.95).
*   **CAA Process:**
    *   Risk Assessment: Classifies as "Low" risk (localized code change, non-critical file).
    *   Semantic Guardrails: OK.
    *   Consistency Checks: OK.
    *   Sandbox (if applicable for diffs): OK.
    *   Confidence Aggregation: Overall confidence high.
    *   Decision Engine: `IF risk_level IS Low AND overall_confidence > user_threshold_low_risk THEN auto_approve`.
*   **Outcome:** Action is auto-approved.
*   **Benefit:** Streamlined workflow for routine, safe changes.

### Scenario 4: Catching Semantic Drift in Generated Text
*   **Proposed Action:** `write_to_file` with content for a user-facing document. The LLM has subtly introduced biased language.
*   **CAA Process:**
    *   Risk Assessment: "Medium" risk (user-facing content).
    *   Semantic Guardrails (Task 1.1): Flags the content for potential bias (e.g., "moderate warning").
    *   Confidence Aggregation: Receives semantic guardrail warning.
    *   Decision Engine: Triggers manual review due to guardrail warning on Medium risk content.
*   **Outcome:** User reviews the content, spots the bias, and corrects it before the file is written.
*   **Error Prevented:** Publishing inappropriate or biased content.

### Scenario 5: Preventing Out-of-Scope File Modification
*   **Proposed Action:** `write_to_file` attempting to modify a file outside the explicitly defined project directory for the current task.
*   **CAA Process:**
    *   Task Boundary Check (Task 2.1): Flags the action as an out-of-bounds write attempt.
    *   Risk Assessment: "High" risk (modifying unexpected file system locations).
    *   Decision Engine: Triggers manual review (or potentially auto-rejects) due to boundary violation on a high-risk action.
*   **Outcome:** User is alerted and prevents modification of unrelated files.
*   **Error Prevented:** Accidental damage to files outside the intended scope of work.

## 7. Updating the Memory System

After the design and initial conceptualization of these auto-approval safety mechanisms, the following information will be recorded/updated in the memory system (e.g., `memory-agent-sql`):

*   **New Concepts/Mechanisms:**
    *   `Conditional Auto-Approval (CAA) System`: Overall architecture, including Risk Assessment, Confidence Aggregation, User Preferences, and Decision Engine.
    *   `Risk-Based Approval Logic`: The principle of tying approval decisions to assessed action risk.
    *   `Confidence-Weighted Decision Making`: Using aggregated confidence from multiple sources.
    *   `Integration of Safety Signals`: How outputs from guardrails, boundary checks, sandbox, and cost monitoring feed into CAA.
*   **Proposed Safety Mechanisms:**
    *   Detailed descriptions of the Risk Assessment Module (criteria: action type, target, potential impact).
    *   Detailed descriptions of the Confidence Aggregation Module (inputs: LLM confidence, guardrails, consistency, boundary, sandbox, cost).
    *   User-configurable risk tolerance levels (`Conservative`, `Balanced`, `Permissive`).
    *   User-configurable overrides per action type/tool and confidence thresholds.
*   **Conditional Auto-Approval Logic Examples:**
    *   Specific rule examples (e.g., `IF risk IS Critical THEN manual_review`).
    *   How different combinations of risk, confidence, and user settings lead to different outcomes.
*   **Examples of Prevented Errors (as listed in Section 6):**
    *   Incorrect file deletion.
    *   Costly API calls.
    *   Semantic drift in text.
    *   Out-of-scope file modifications.
*   **Keywords for Future Retrieval:**
    *   "Roo Code auto-approval", "conditional approval", "AI safety mechanisms", "human-in-the-loop AI", "risk-based automation", "AI action validation", "automated decision safeguards".

This update will ensure that future research or development tasks related to AI safety, automation control, or error prevention in Roo Code can leverage these designed concepts.