---
title: Decision Framework for Human Intervention in Roo Code
task_id: Task 5.1
date: 2025-05-19
last_updated: 2025-05-19
status: DRAFT
owner: deep-research-agent
---

## 1. Introduction

This document outlines a decision framework for integrating strategic human intervention points within Roo Code workflows. The goal is to optimize human-in-the-loop (HITL) patterns, enhancing Roo Code's reliability, user trust, and overall effectiveness by ensuring human oversight at critical junctures. This framework draws upon previous project phase outputs (Phases 0-4), general research on HITL AI, and specific analysis of Roo Code's architecture and user interaction patterns.

## 2. Analysis of Roo Code Workflows and User Interaction Points

Roo Code operates through a series of user-initiated tasks, processed by specialized modes, utilizing a range of tools, and often involving iterative refinement (e.g., Boomerang Task System). Existing user interaction points provide natural loci for enhanced human verification.

### Key Workflow Stages & Existing Interaction Points:

*   **Task Definition & Initiation:** Users specify goals.
    *   *Current Interaction:* Initial prompt.
*   **Mode & Configuration Selection:** Users choose how Roo operates.
    *   *Current Interaction:* Mode selection UI/commands.
*   **Sub-task/Phase Completion (Boomerang Logic):** Segments of work are completed.
    *   *Current Interaction:* Implicit returns, potential for explicit review points.
*   **Tool Usage:** Roo requests permission to use tools (e.g., file system access, command execution).
    *   *Current Interaction:* Explicit approval prompts.
*   **Clarification Requests:** Roo seeks more information.
    *   *Current Interaction:* `ask_followup_question` tool.
*   **Checkpointing:** Automatic saves before significant actions.
    *   *Current Interaction:* System-level, user can roll back.
*   **Error Detection & Reporting:** Systems from Phases 1-3 flag issues.
    *   *Current Interaction:* Error messages, potential task halts.
*   **Task Completion:** Roo signals task is finished.
    *   *Current Interaction:* `attempt_completion` tool.

### Identified Opportunities for Intervention:

Based on the above, strategic intervention points can be integrated or enhanced at:

1.  **Pre-Execution Review (Complex/High-Risk Tasks):** Before Roo commits to a complex plan or high-impact actions, especially if the task is novel or ambiguous.
2.  **Critical Milestone Verification (Boomerang Returns):** At the conclusion of key sub-tasks within the Boomerang workflow, particularly if outputs are foundational for subsequent steps.
3.  **Enhanced Tool Use Approval:** For high-risk tools or unusual tool requests, provide more context and require more explicit confirmation.
4.  **Proactive Clarification (Low Confidence):** When LLM confidence is low or ambiguity is detected by Roo, proactively trigger an `ask_followup_question` or present alternative interpretations.
5.  **Error-Triggered Intervention:** When any error detection system (semantic drift, boundary violation, cost anomaly, risky auto-approval) flags an issue, pause and require human input.
6.  **Cumulative Change Review:** If a large volume of changes (e.g., multiple files, significant lines of code) is generated without intermediate human input, prompt for a batch review.
7.  **Pre-`attempt_completion` Sanity Check:** Before final completion, offer a summary of actions and key outputs for a final user "go/no-go."

## 3. Proposed Decision Framework for Requesting Human Input

The decision to request human input should be governed by a dynamic framework considering multiple factors. The aim is to balance autonomy with safety and user control.

### Core Principles:

*   **Risk-Adaptive Oversight:** The level of human intervention should correlate with the potential risk and impact of Roo's actions.
*   **User-Centric Control:** Users should have configurable preferences for the level of autonomy and intervention.
*   **Transparency:** When intervention is requested, Roo should clearly explain *why*.

### Decision Criteria & Triggers:

| Criterion                                  | Description                                                                                                | Trigger for Intervention Examples                                                                                                |
| :----------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| **1. Risk/Impact Level**                   | Criticality of files, data loss potential, security, cost of error.                                        | High-risk ops (e.g., prod file edits, data deletion) → Mandatory confirmation, tiered approval.                                  |
| **2. Confidence Score**                    | LLM confidence, internal consistency checks.                                                               | Low score → Verification prompt. Very low score → Halt, request explicit guidance.                                               |
| **3. Novelty/Complexity**                  | Unseen task patterns, multi-step complexity, broad synthesis required.                                     | Novel/complex task → Milestone verification, plan review before execution.                                                       |
| **4. Ambiguity Level**                     | In user prompt or Roo's interpretation.                                                                    | Detected ambiguity → Proactive `ask_followup_question`, present interpretations for user selection.                              |
| **5. Error Detection Flags**               | Semantic drift, boundary violation, cost anomaly, auto-approval risk.                                      | Active flag → Specific action (halt, confirm, clarify) based on flag type.                                                       |
| **6. User Preferences**                    | User-defined oversight levels (e.g., "paranoid" vs. "trust" modes), specified review requirements.         | Adhere to settings. E.g., "Always ask before editing `config.json`".                                                             |
| **7. Irreversibility of Action**           | Difficult/impossible to undo (e.g., `git push --force`, permanent deletions).                              | Irreversible action → Mandatory confirmation with explicit warning.                                                              |
| **8. Cumulative Change Magnitude**         | Large number of file/line changes since last interaction.                                                  | Exceeds threshold → Prompt for batch review and checkpoint confirmation.                                                           |
| **9. Deviation from Patterns**             | Significant deviation from project conventions, best practices, or security norms.                         | Detected deviation → Flag concern, explain, request confirmation.                                                                |
| **10. Resource Consumption**               | Predicted/actual token use, execution time, API quotas nearing limits.                                     | Approaching limits → Inform user, request confirmation to proceed.                                                               |

## 4. Proposed Intervention Mechanisms

Interventions should be clear, informative, and minimally disruptive.

1.  **Modal Dialogs/Prompts:** For critical confirmations (e.g., high-risk actions, irreversible operations). Should clearly state the action, the reason for intervention, and potential consequences. Options: "Proceed," "Cancel," "More Info," "Edit Plan."
2.  **Inline Chat Notifications/Suggestions:** For lower-stakes verifications or suggestions (e.g., "Confidence is low on this section, would you like to review?"). Can offer quick actions like "Accept," "Reject," "Ask for Alternatives."
3.  **Task Pause & Status Update:** When an intervention is triggered, the relevant task in Roo Code should clearly indicate it's "Paused - Awaiting User Input." The UI should highlight what needs attention.
4.  **Differential Views:** For code changes, show a diff view (similar to Git) for easy review before applying.
5.  **Structured Clarification Prompts:** When using `ask_followup_question` due to low confidence/ambiguity, Roo could present its current understanding or multiple interpretations for the user to choose from or refine.
6.  **User-Configurable Notification Levels:** Allow users to choose how actively they are notified (e.g., subtle UI cues vs. prominent pop-ups) based on intervention severity.
7.  **"Explain Decision" Button:** Accompanying intervention prompts, allowing users to get more context on why Roo decided to ask for human input.

## 5. Considerations for Measuring Effectiveness

The effectiveness of these intervention strategies should be continuously monitored and refined.

*   **Error Reduction Rate:** Track decrease in errors post-intervention implementation (requires error telemetry from Task 4.1).
*   **User Satisfaction:** Gather feedback on the clarity, usefulness, and intrusiveness of interventions.
*   **Task Completion Efficiency:** Measure total task time, including human verification time. Aim to optimize the balance between safety and speed.
*   **Intervention Acceptance/Override Rates:** High override rates might indicate poorly tuned triggers or unclear intervention reasons.
*   **False Positive/Negative Rates for Interventions:** How often are interventions unnecessary, or how often are they missed when needed?
*   **User Trust & Autonomy Preferences:** Monitor if users gradually allow more autonomy as they trust the intervention system.
*   **Cognitive Load:** Assess the mental effort required from users; interventions should simplify, not complicate.

## 6. Example Scenarios

*   **Scenario 1: High-Risk File Modification**
    *   **Roo Action:** Attempts to `apply_diff` to a core configuration file identified as high-risk.
    *   **Trigger:** Risk/Impact Level.
    *   **Intervention:** Modal prompt: "Roo proposes to modify `settings.prod.json`. This is a critical production file. [Show Diff]. Do you approve?"
*   **Scenario 2: LLM Low Confidence**
    *   **Roo Action:** Generates a complex function but internal confidence score is 0.6 (threshold is 0.75).
    *   **Trigger:** Confidence Score.
    *   **Intervention:** Inline chat: "I've drafted the `calculate_risk_matrix` function, but I'm not fully confident in the edge case handling. Would you like to review it before I proceed with integration?"
*   **Scenario 3: Semantic Drift Detected**
    *   **Roo Action:** While refactoring a module, its output starts to deviate significantly from the documented purpose (semantic drift flag from Task 1.1).
    *   **Trigger:** Error Detection Flag.
    *   **Intervention:** Task Pause. Notification: "Task paused. Semantic drift detected in `user_auth_module`. The current changes seem to alter its core authentication logic. Please review and confirm or provide new instructions."
*   **Scenario 4: User Preference for Oversight**
    *   **Roo Action:** User has configured "always ask before executing any `git commit` command." Roo prepares a commit.
    *   **Trigger:** User Preference.
    *   **Intervention:** Modal prompt: "Roo is ready to commit the following changes: [Show commit message and changed files]. Approve commit?"

## 7. Conclusion

Implementing a robust decision framework for human intervention is crucial for maximizing the utility and safety of Roo Code. By strategically placing checkpoints and triggers based on risk, confidence, complexity, and user preferences, Roo Code can leverage human intelligence effectively, fostering trust and improving the quality of AI-assisted development. Continuous monitoring and refinement of these intervention mechanisms will be key to their long-term success.