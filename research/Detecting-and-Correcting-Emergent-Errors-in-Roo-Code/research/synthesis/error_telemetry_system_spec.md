---
title: Roo Code Privacy-Respecting Error Telemetry System Specification
task_id: 4.1
date: 2025-05-19
last_updated: 2025-05-19
status: DRAFT
owner: deep-research-agent
---
## 1. Introduction

This document outlines the design for an opt-in, privacy-respecting error telemetry system for Roo Code. The primary goal is to allow users to voluntarily report errors and unexpected behaviors to help improve Roo Code, while ensuring user privacy and data protection. This system is designed with transparency and user control as core principles.

## 2. System Design

### 2.1. Core Principles
*   **User Opt-In:** Telemetry data will only be collected from users who explicitly opt-in. No data will be collected by default.
*   **Transparency:** Users will be clearly informed about what data is collected, how it's anonymized, stored, and used. This information will be easily accessible within Roo Code (e.g., in settings, documentation).
*   **Data Minimization:** Only data essential for understanding and fixing errors will be collected.
*   **Anonymization:** All collected data will be anonymized to protect user identity. Sensitive information will be stripped or generalized.
*   **User Control:** Users will have granular control over their participation and can opt-out or change their preferences at any time.
*   **Security:** Data will be transmitted and stored securely.

### 2.2. Opt-In Mechanism and User Controls

*   **Initial Opt-In:**
    *   Upon first use of a Roo Code version that includes this telemetry system, or upon a significant update to the telemetry policy, users will be presented with a clear, concise dialog explaining the error reporting feature.
    *   This dialog will detail:
        *   The purpose of telemetry (to improve Roo Code).
        *   What data is collected (anonymized error details, non-sensitive context).
        *   How data is anonymized and protected.
        *   A direct link to the full privacy policy/telemetry documentation.
    *   Users will have clear "Opt-In" and "Decline" buttons. The default will be "Decline".
*   **Settings Panel:**
    *   A dedicated section in Roo Code's settings will allow users to:
        *   Enable or disable error telemetry.
        *   View the types of data being collected.
        *   Access a history of their reported errors (locally, if feasible, without re-identifying them on the server).
        *   View a link to the privacy policy and telemetry documentation.
*   **Granular Control (Future Consideration):**
    *   Potentially allow users to choose levels of telemetry (e.g., "minimal" vs. "enhanced" error details), though the initial implementation will focus on a single, well-defined opt-in.

### 2.3. User Interface for Reporting Errors

*   **Automatic Reporting (Post Opt-In):** Once a user opts-in, certain classes of unhandled exceptions or significant operational failures within Roo Code could trigger an automatic preparation of an error report.
    *   Before sending, a non-intrusive notification could briefly inform the user that an error report is ready to be sent, offering a chance to review/cancel (though this adds complexity and potential friction). A simpler approach is to rely on the initial opt-in for consent to send these anonymized reports.
*   **Manual Reporting Command/Button:**
    *   A command (e.g., `/reportError` in the Roo Code chat interface) or a dedicated button in the UI (e.g., near error messages or in a help menu).
    *   This would allow users to report issues that aren't automatically caught or to provide additional context on an observed problem.
    *   The manual report could open a simple form where users can optionally add a brief description of what they were doing or what they expected. This description would also be subject to sanitization.
## 3. Data Collection

The following data points are proposed for collection, with a strong emphasis on anonymization and avoiding any Personally Identifiable Information (PII) or sensitive project/code data.

### 3.1. Data Points
*   **`report_id`**: A unique, randomly generated UUID for the report (not linked to user).
*   **`timestamp_utc`**: ISO 8601 timestamp of when the error occurred.
*   **`roo_code_version`**: Version of Roo Code in use (e.g., "1.2.3").
*   **`os_type`**: Operating system type (e.g., "Windows", "MacOS", "Linux").
*   **`os_version`**: Operating system version (generalized, e.g., "Windows 10/11", "MacOS 13.x").
*   **`active_mode_slug`**: The slug of the Roo Code mode active when the error occurred (e.g., "code", "deep-research-agent").
*   **`error_type`**: The class name or type of the error (e.g., "NullPointerException", "APIError", "UnhandledPromiseRejection").
*   **`error_message_template`**: A generalized template of the error message, with specific values (paths, variable names, IDs) replaced by placeholders (e.g., "Cannot read property 'x' of undefined", "API request to {URL} failed with status {STATUS_CODE}").
*   **`anonymized_stack_trace`**: Stack trace with file paths, line numbers, and function names.
    *   File paths will be anonymized:
        *   Project-specific paths replaced with placeholders (e.g., `{PROJECT_PATH}/src/module.js`).
        *   User directory paths removed or replaced (e.g., `/Users/{USER}/...` becomes `{USER_HOME_PATH}/...`).
        *   Focus on stack frames within Roo Code's own codebase or known libraries, potentially truncating or heavily generalizing external code paths.
    *   Function names and variable names within the stack trace should generally be preserved if they are part of Roo Code's own code or common libraries, as they are crucial for debugging. However, if these could inadvertently contain PII from user code, further sanitization might be needed.
*   **`context_metadata` (Highly Restricted & Anonymized):**
    *   `active_tool_used (if any)`: Name of the tool being used when error occurred (e.g., "read_file", "use_mcp_tool").
    *   `mcp_server_name (if applicable)`: Name of MCP server involved, if error related to MCP.
    *   `mcp_tool_name (if applicable)`: Name of MCP tool involved.
    *   `session_duration_approx_minutes`: Approximate duration of the current Roo Code session in minutes (bucketed, e.g., 0-5, 5-15, 15-60, >60).
    *   `error_source`: (e.g., "core_plugin", "mcp_communication", "ui_component").
*   **`user_description_hash` (for manually reported errors, optional):** If a user provides a manual description, a hash of this description could be sent. This allows grouping similar manually reported issues without sending the raw text. Alternatively, if raw text is deemed essential, it must be explicitly stated that this text will be sent and users should avoid PII. Given privacy focus, hashed or no text is safer.
*   **`opt_in_version`**: Version of the telemetry consent/policy the user agreed to.

### 3.2. Data NOT to Collect
*   User IP addresses.
*   Usernames, machine names, specific user IDs.
*   Actual file contents or snippets of user code/data.
*   Specific file names or paths that could identify a user or project (unless heavily anonymized as described above).
*   Environment variables or secrets.
*   Full, non-anonymized error messages if they might contain sensitive details.
*   Keystrokes, mouse movements, or detailed UI interaction sequences.
*   Any data from outside Roo Code's direct operational scope.
## 4. Data Format and Transmission

### 4.1. Data Format (JSON)
```json
{
  "report_id": "uuid-v4-random-string",
  "timestamp_utc": "2025-05-19T10:00:00Z",
  "roo_code_version": "1.2.3",
  "os_type": "Windows",
  "os_version": "Windows 10/11",
  "active_mode_slug": "code",
  "error_details": {
    "error_type": "TypeError",
    "error_message_template": "Cannot read properties of undefined (reading '{PROPERTY_NAME}')",
    "anonymized_stack_trace": [
      "TypeError: Cannot read properties of undefined (reading 'details')",
      "    at {PROJECT_PATH}/src/features/feature_x.js:105:25",
      "    at async {PROJECT_PATH}/src/core/task_runner.js:50:10"
    ],
    "error_source": "core_plugin"
  },
  "context_metadata": {
    "active_tool_used": "apply_diff",
    "session_duration_approx_minutes": "15-60"
  },
  "opt_in_version": "1.0"
}
```

### 4.2. Transmission
*   **Protocol:** HTTPS (TLS 1.2 or higher) exclusively.
*   **Endpoint:** A dedicated, secure API endpoint for receiving telemetry data.
*   **Batching:** Reports might be batched locally (e.g., a few reports or after a short time delay) to reduce network requests, but not held for so long that context is lost or the user opts out before sending.
*   **Retry Mechanism:** A limited retry mechanism for transient network failures, with backoff.

### 4.3. Storage
*   **Database:** A secure, access-controlled database (e.g., PostgreSQL, or a specialized time-series/analytics database).
*   **Access Control:** Strict access controls; only authorized Roo Code developers/analysts involved in error resolution and product improvement can access the raw (anonymized) telemetry data.
*   **Data Retention:** A defined data retention policy (e.g., raw anonymized reports retained for X months, aggregated statistics retained longer or indefinitely). This should be communicated to users.
*   **Encryption at Rest:** Data should be encrypted at rest.
## 5. Integration with Roo Code's Analytics Framework

### 5.1. Analysis of Existing Framework (Inference)
The file `Roo-Code/webview-ui/src/utils/TelemetryClient.ts` and its test file `Roo-Code/webview-ui/src/utils/__tests__/TelemetryClient.test.ts` strongly suggest an existing telemetry mechanism, possibly using PostHog (inferred from `Roo-Code/webview-ui/src/__mocks__/posthog-js.ts`).

**Assumptions based on file names:**
*   Roo Code likely has a `TelemetryClient` class.
*   It might be focused on UI interactions or general usage analytics rather than detailed error reporting.
*   It might already handle aspects of user identification (hopefully anonymized) and event tracking.

### 5.2. Integration Plan
*   **Leverage `TelemetryClient`:** If the existing `TelemetryClient` is suitable and aligns with privacy goals (e.g., uses anonymized user IDs, respects opt-in), the new error reporting can be channeled through it.
    *   A new event type (e.g., `roo_error_reported`) could be added.
    *   The JSON payload defined above would be the properties of this event.
*   **Extend or Complement:**
    *   If `TelemetryClient` is too generic or doesn't support the required level of detail/anonymization for errors, a specialized path for error telemetry might be needed. This could still share common infrastructure (like the opt-in status).
    *   The existing opt-in mechanism for general telemetry (if one exists and is robust) should ideally cover error reporting as well, or be extended with a specific sub-option for error details. If no robust opt-in exists, the one designed in section 2.2 takes precedence for error reporting.
*   **Backend Integration:**
    *   The backend receiving data from `TelemetryClient` (e.g., PostHog instance or custom backend) would need to be configured to handle and store these structured error reports.
    *   Dashboards and alerting would be set up on this backend to monitor error trends, frequencies, and new types of errors.

### 5.3. Lightweight Approach (If No Suitable Existing Framework)
If `TelemetryClient` is non-existent or unsuitable:
*   A new, simple telemetry submission service would be implemented within Roo Code.
*   It would handle the opt-in logic, data collection, anonymization, and secure transmission to a dedicated backend API endpoint.
*   The backend would be a simple service responsible for receiving, validating, and storing the JSON reports in a secure database.
*   Analysis would initially be done via direct database queries or simple dashboards built on top of the database. OpenTelemetry collectors and exporters could be used to forward data to an analysis platform.
## 6. Privacy Considerations

This section is critical and underpins the entire design.

### 6.1. GDPR and Legal Compliance
*   **Lawful Basis for Processing:** Explicit user consent (opt-in) is the lawful basis.
*   **Data Subject Rights:**
    *   **Right to Access:** Users can be informed of the *types* of data collected (as per the policy). Direct access to their specific submitted anonymized reports is complex and might risk re-identification if not handled carefully. The focus is on transparency of data categories.
    *   **Right to Rectification:** Not directly applicable to anonymized, immutable error reports. Users can stop future reporting.
    *   **Right to Erasure (Right to be Forgotten):** If a user opts out, no *future* data is sent. Deleting already submitted anonymized data from aggregated datasets is typically not feasible or required, as it's no longer personal data. This distinction must be clear in the privacy policy.
    *   **Right to Restrict Processing:** Achieved by opting out.
    *   **Right to Data Portability:** Not typically applicable to anonymized telemetry.
    *   **Right to Object:** Achieved by opting out or not opting in.
*   **Data Protection Officer (DPO):** If Roo Code processes significant amounts of data or is subject to specific GDPR triggers, a DPO might be necessary.
*   **Privacy Policy:** A clear, comprehensive, and easily accessible privacy policy detailing the telemetry practices is mandatory. It should cover all points in this specification.

### 6.2. Data Minimization
*   Only data strictly necessary for diagnosing and fixing errors is collected.
*   Avoid collecting overly broad context or any user-specific content.
*   Fields like `os_version` are generalized.

### 6.3. Anonymization and Pseudonymization
*   **Anonymization Goal:** To ensure that data, once collected, cannot be reasonably used to identify an individual.
*   **Techniques to be employed:**
    *   Removal of direct identifiers (IP, username, machine name).
    *   Generalization (e.g., `os_version`, `session_duration_approx_minutes`).
    *   Placeholder replacement for sensitive strings in error messages and stack traces (e.g., file paths, specific values).
    *   Careful review of all collected fields to ensure no PII can be inferred.
    *   Differential privacy techniques could be explored for aggregated analytics in the future for stronger guarantees, but initial focus is on robust input sanitization and generalization.
*   **No Re-identification:** The system must be designed to prevent re-identification of users from the anonymized data.

### 6.4. User Consent Management
*   **Explicit Opt-In:** Consent must be freely given, specific, informed, and unambiguous.
*   **Easy Opt-Out:** Users can withdraw consent at any time easily through Roo Code settings.
*   **Consent Records:** Maintain a record of user consent (e.g., which version of the policy they agreed to, linked to an internal, non-exportable anonymous identifier if one is used by the general TelemetryClient, or simply a flag if no such ID exists).
*   **Clarity of Information:** Information provided at the point of consent must be easy to understand.

### 6.5. Data Security
*   **Transmission Security:** HTTPS for all data transfer.
*   **Storage Security:** Encryption at rest, strict access controls to the database/storage.
*   **Access Control:** Role-based access for Roo Code team members who need to analyze telemetry data.
*   **Regular Audits:** Periodically review the telemetry system, data collected, and anonymization techniques to ensure ongoing privacy compliance and effectiveness.

### 6.6. Transparency
*   All aspects of the telemetry system (data collected, purpose, anonymization, storage, retention) will be documented in a public privacy policy.
*   Consider open-sourcing the anonymization logic used, if custom-developed, to build trust.
## 7. Future Considerations
*   **Differential Privacy:** For aggregated analysis to provide stronger mathematical guarantees of privacy.
*   **Federated Learning/Analytics:** Explore if error patterns can be learned without centralizing raw (even anonymized) reports, though this is significantly more complex.
*   **User-Side Anonymization Preview:** Potentially show users (locally) what an anonymized report would look like before they opt-in or before it's sent, to enhance transparency.

## 8. Conclusion
This proposed error telemetry system aims to balance the need for valuable diagnostic data to improve Roo Code with an unwavering commitment to user privacy and trust. By implementing robust opt-in mechanisms, strong anonymization techniques, and transparent policies, Roo Code can foster a collaborative relationship with its community for error reporting.