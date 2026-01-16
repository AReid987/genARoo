# Roo Code Extension API Specification

## 1. Design Goals and Principles

The Roo Code Extension API aims to provide a robust and flexible platform for third-party developers to create specialized error detection modules. The core design principles are:

*   **Extensibility:** Allow a wide range of error detection capabilities to be integrated.
*   **Stability:** Ensure API contracts remain stable across Roo Code versions, with clear versioning strategies.
*   **Ease of Use:** Provide a straightforward and well-documented API for extension development.
*   **Security:** Implement measures to protect Roo Code and users from malicious or poorly-written extensions.
*   **Performance:** Minimize the performance impact of extensions on Roo Code's core functionality.
*   **Modularity:** Enable extensions to focus on specific error types or contexts.
*   **Interoperability:** Allow extensions to potentially interact with existing Roo Code mechanisms like the Validator mode or auto-approval system.

## 2. API Endpoints and Data Structures

This section outlines the primary ways extensions will interact with Roo Code.

### 2.1. Core Interaction Model

Extensions will primarily function by registering "Error Detectors." Roo Code will invoke these detectors at appropriate points in its workflow, providing relevant context and receiving detected errors in return.

### 2.2. Data Structures for Roo Code -> Extension Communication

When Roo Code invokes an error detector, it will provide the following information:

*   **`TaskContext`**:
    *   `taskId`: string (Unique identifier for the current task)
    *   `userPrompt`: string (The initial user request for the task)
    *   `currentMode`: string (Identifier of the Roo Code mode currently active, e.g., "code", "debug")
    *   `workspaceRoot`: string (Path to the current workspace)
    *   `activeFiles`: Array<string> (List of currently open or relevant file paths)
    *   `llmInteractionHistory`: Array<`LLMMessage`> (Chronological record of LLM prompts and responses for the current task)
        *   `LLMMessage`:
            *   `role`: "user" | "assistant" | "system"
            *   `content`: string
            *   `timestamp`: string (ISO 8601)
            *   `metadata`: object (Optional, for additional context like model name, tokens used)
    *   `rooCodeEnvironment`: object
        *   `version`: string (Roo Code version)
        *   `operatingSystem`: string
        *   `activeTerminals`: Array<object> (Information about active terminals)

*   **`AnalysisTarget`**:
    *   `targetType`: "llm_output" | "file_content" | "code_diff" | "generic_text"
    *   `content`: string (The actual text content to be analyzed, e.g., an LLM response, a file's content, a code diff hunk)
    *   `filePath`: string (Optional, if `targetType` is `file_content` or `code_diff`)
    *   `languageId`: string (Optional, programming language identifier if applicable, e.g., "python", "javascript")
    *   `metadata`: object (Optional, for additional context specific to the target)

### 2.3. Data Structures for Extension -> Roo Code Communication

Extensions will return detected errors using the following structure:

*   **`DetectedError`**:
    *   `extensionId`: string (Unique identifier of the extension reporting the error)
    *   `errorCode`: string (Extension-specific error code or identifier)
    *   `description`: string (Human-readable description of the error)
    *   `severity`: "critical" | "error" | "warning" | "info"
    *   `confidenceScore`: number (0.0 to 1.0, indicating the extension's confidence in this detection)
    *   `filePath`: string (Optional, path to the file where the error is located)
    *   `range`: object (Optional, specifying the location within the file)
        *   `startLine`: number
        *   `startCharacter`: number
        *   `endLine`: number
        *   `endCharacter`: number
    *   `suggestedActions`: Array<`SuggestedAction`> (Optional, actions Roo Code or the user could take)
        *   `SuggestedAction`:
            *   `actionId`: string (Unique identifier for the action)
            *   `description`: string (Description of the action)
            *   `command`: string (Optional, a Roo Code command to execute)
            *   `arguments`: Array<any> (Optional, arguments for the command)
    *   `metadata`: object (Optional, for additional error-specific details)

### 2.4. API Endpoints (Conceptual)

Roo Code will expose an API namespace, tentatively `roo.extensions`, with functions like:

*   **`roo.extensions.registerErrorDetector(detectorId: string, detector: ErrorDetector): Disposable`**:
    *   `detectorId`: A unique string identifying this specific detector (e.g., "my-python-linter-detector").
    *   `ErrorDetector`: An object or class provided by the extension with a method like `detect(taskContext: TaskContext, analysisTarget: AnalysisTarget): Promise<DetectedError[] | null>`.
    *   Returns a `Disposable` object that can be used to unregister the detector.

*   **`roo.extensions.log(level: "info" | "warn" | "error", message: string, extensionId: string)`**:
    *   Allows extensions to write to Roo Code's logs for debugging and information purposes.

*   **`roo.extensions.getConfiguration(section: string): any`**:
    *   Allows extensions to access their specific configuration settings managed by Roo Code.

*   **`roo.extensions.showInformationMessage(message: string): void`** (and similar for warnings/errors):
    *   Allows extensions to display non-modal messages to the user, similar to VS Code's `window.showInformationMessage`.

## 3. Extension Lifecycle and Integration

The lifecycle of an error detection extension within Roo Code involves several key stages:

*   **Packaging and Manifest:**
    *   Extensions are packaged in a standard format (e.g., similar to VS Code's `.vsix`).
    *   Each extension must include a manifest file (e.g., `package.json`) that declares its metadata, capabilities, and contribution points.
    *   **Contribution Point Example (`package.json`):**
        ```json
        {
          "name": "my-error-detector-extension",
          "version": "0.1.0",
          "publisher": "myPublisher",
          "engines": {
            "rooCode": "^1.0.0" // Specifies compatible Roo Code API version
          },
          "contributes": {
            "errorDetectors": [
              {
                "id": "myJsonSyntaxChecker",
                "name": "JSON Syntax Checker",
                "description": "Detects basic syntax errors in JSON content.",
                "activationEvents": [
                  "onLanguage:json",
                  "onAnalysisTarget:llm_output" // If LLM might output JSON
                ],
                "targetLanguageIds": ["json"], // Optimisation hint
                "targetTypes": ["file_content", "llm_output", "generic_text"] // Optimisation hint
              }
            ]
          },
          "activationEvents": [ // Main extension activation
            "onStartup", // Or more specific events
            "onCommand:myExtension.configure"
          ],
          "main": "./out/extension.js" // Entry point
        }
        ```

*   **Installation & Discovery:**
    *   Roo Code will provide a mechanism for users to install and manage extensions (e.g., from a marketplace or local files).
    *   On startup or when an extension is installed/enabled, Roo Code parses the manifest to discover available error detectors and other contributions.

*   **Activation:**
    *   Extensions are activated based on `activationEvents` defined in their manifest. These events can be:
        *   `onStartup`: Activate as soon as Roo Code starts.
        *   `onCommand:[commandId]`: Activate when a specific command is executed.
        *   `onLanguage:[languageId]`: Activate when a file of a specific language is opened or becomes the `AnalysisTarget`.
        *   `onAnalysisTarget:[targetType]`: Activate when a specific type of content is about to be analyzed.
        *   `onModeChange:[mode_slug]`: Activate when Roo Code switches to a particular mode.
        *   `onTaskStart`: Activate when a new task begins.
    *   Upon activation, the extension's main module (specified in `main` in `package.json`) is loaded, and its `activate(context: ExtensionContext)` function is called.
    *   The `ExtensionContext` would provide access to the `roo.extensions` API.

*   **Registration (within `activate` function):**
    *   Inside its `activate` function, the extension uses `roo.extensions.registerErrorDetector(detectorId, detector)` to make its error detection logic available to Roo Code.
    *   The `detectorId` should match one of the IDs declared in the `contributes.errorDetectors` section of the manifest.

*   **Invocation:**
    *   Roo Code's core error processing pipeline determines when and which registered error detectors to invoke.
    *   **Selection Criteria:** Detectors might be selected based on:
        *   The `AnalysisTarget.targetType` (e.g., only invoke detectors interested in "llm_output").
        *   The `AnalysisTarget.languageId` (e.g., only invoke Python-specific detectors for Python code).
        *   User configuration (e.g., enabling/disabling specific detectors or extensions).
        *   The current `TaskContext.currentMode`.
    *   **Data Flow:**
        1.  Roo Code prepares the `TaskContext` and `AnalysisTarget` objects.
        2.  For each selected and active detector, Roo Code calls its `detect(taskContext, analysisTarget)` method.
        3.  The detector performs its analysis asynchronously and returns `Promise<DetectedError[] | null>`.
        4.  Roo Code collects all `DetectedError` objects from all invoked detectors.

*   **Deactivation & Disposal:**
    *   When an extension is disabled or uninstalled, or when Roo Code shuts down, its `deactivate()` function (if exported) is called.
    *   The `Disposable` returned by `registerErrorDetector` should be disposed of by the extension during deactivation to unregister its detector.

*   **Interaction with Roo Code Systems:**
    *   **Validator Mode:** `DetectedError` objects can be presented to the Validator mode. The `confidenceScore`, `severity`, and `description` will help the Validator (or the user via the Validator) decide on the validity of the error. `suggestedActions` can be presented as options.
    *   **Auto-Approval System:** Errors with high `confidenceScore`, low `severity`, and clear, safe `suggestedActions` (especially those with defined `command`s) could potentially be handled by the auto-approval system, if the user has configured such behavior.
    *   **Error Telemetry:** Aggregated, anonymized data from `DetectedError` (e.g., `extensionId`, `errorCode`, `severity`) could be contributed to the error telemetry system (Task 4.1) if the extension and user opt-in.
    *   **User Interface:** Detected errors will be displayed in the Roo Code UI, potentially in a dedicated "Problems" panel, as inline annotations in code editors, or as part of the chat/task output. The `filePath` and `range` are crucial for this.

## 4. Conceptual Example of an Extension Implementation

This example demonstrates a simple extension that checks for basic JSON syntax errors.

**`package.json` (Manifest Snippet):**
```json
{
  "name": "json-syntax-checker",
  "version": "0.1.0",
  "publisher": "rooCommunity",
  "engines": {
    "rooCode": "^1.0.0"
  },
  "activationEvents": [
    "onLanguage:json"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "errorDetectors": [
      {
        "id": "jsonSyntaxCheckerBasic",
        "name": "Basic JSON Syntax Checker",
        "description": "Detects syntax errors in JSON content using JSON.parse().",
        "activationEvents": ["onLanguage:json", "onAnalysisTarget:file_content", "onAnalysisTarget:generic_text"],
        "targetLanguageIds": ["json"],
        "targetTypes": ["file_content", "generic_text"]
      }
    ]
  }
}
```

**`src/extension.ts` (TypeScript-like Pseudo-code):**

```typescript
// Import types from the Roo Code Extension API (conceptual)
// import { ExtensionContext, TaskContext, AnalysisTarget, DetectedError, ErrorDetector, Disposable, Range, roo } from 'roo-code-extension-api';

// Placeholder for actual API types
interface ExtensionContext { subscriptions: { push(disposable: Disposable): void }; }
interface TaskContext { /* ... as defined in spec ... */ }
interface AnalysisTarget { targetType: string; content: string; filePath?: string; languageId?: string; }
interface DetectedError { /* ... as defined in spec ... */ }
interface ErrorDetector { detect(taskContext: TaskContext, analysisTarget: AnalysisTarget): Promise<DetectedError[] | null>; }
interface Disposable { dispose(): void; }
interface Range { startLine: number; startCharacter: number; endLine: number; endCharacter: number; }
const roo = { // Conceptual API namespace
  extensions: {
    registerErrorDetector: (id: string, detector: ErrorDetector): Disposable => ({ dispose: () => console.log(`${id} disposed`) }),
    log: (level: string, message: string, extensionId: string) => console.log(`[${extensionId}] ${level.toUpperCase()}: ${message}`)
  }
};

const EXTENSION_ID = "json-syntax-checker";

class JsonSyntaxDetector implements ErrorDetector {
  async detect(taskContext: TaskContext, analysisTarget: AnalysisTarget): Promise<DetectedError[] | null> {
    if (analysisTarget.languageId !== 'json' && analysisTarget.targetType !== 'generic_text_json_hint') { // Second condition is hypothetical
      // Not a JSON target or not explicitly hinted as JSON for generic text
      return null;
    }

    const errors: DetectedError[] = [];
    try {
      JSON.parse(analysisTarget.content);
    } catch (e: any) {
      roo.extensions.log("info", `JSON parsing error: ${e.message}`, EXTENSION_ID);

      // Try to extract line and character from common JSON error messages (very basic)
      let errorRange: Range | undefined = undefined;
      const match = e.message.match(/at position (\d+)/);
      if (match && match[1]) {
        const errorPosition = parseInt(match[1]);
        let line = 0;
        let char = 0;
        let currentPos = 0;
        const lines = analysisTarget.content.split('\n');
        for (let i = 0; i < lines.length; i++) {
          const lineLength = lines[i].length + 1; // +1 for newline char
          if (currentPos + lineLength > errorPosition) {
            line = i;
            char = errorPosition - currentPos;
            break;
          }
          currentPos += lineLength;
        }
        errorRange = { startLine: line + 1, startCharacter: char, endLine: line + 1, endCharacter: char + 1 };
      }

      errors.push({
        extensionId: EXTENSION_ID,
        errorCode: "JSON_SYNTAX_ERROR",
        description: `Invalid JSON: ${e.message}`,
        severity: "error",
        confidenceScore: 1.0,
        filePath: analysisTarget.filePath,
        range: errorRange,
        suggestedActions: [],
        metadata: { rawError: e.toString() }
      });
    }
    return errors.length > 0 ? errors : null;
  }
}

export function activate(context: ExtensionContext) {
  roo.extensions.log("info", "JSON Syntax Checker extension activated.", EXTENSION_ID);

  const jsonDetector = new JsonSyntaxDetector();
  const disposable = roo.extensions.registerErrorDetector("jsonSyntaxCheckerBasic", jsonDetector);
  context.subscriptions.push(disposable);
}

export function deactivate() {
  roo.extensions.log("info", "JSON Syntax Checker extension deactivated.", EXTENSION_ID);
}
```

## 5. Documentation and Security Considerations

Comprehensive documentation and robust security measures are critical for the success and safety of the Roo Code extension ecosystem.

### 5.1. Documentation Requirements

The following documentation will be essential for API consumers (extension developers):

*   **API Reference:**
    *   Detailed descriptions of all `roo.extensions` namespace functions (e.g., `registerErrorDetector`, `log`, `getConfiguration`, `showInformationMessage`).
    *   Complete specifications for all data structures (`TaskContext`, `AnalysisTarget`, `DetectedError`, `LLMMessage`, `SuggestedAction`, etc.), including all properties, types, and whether they are optional or required.
    *   Clear explanations of enums and their possible values (e.g., `DetectedError.severity`, `AnalysisTarget.targetType`).
*   **Getting Started Guide:**
    *   Step-by-step tutorial on creating a "Hello World" error detection extension.
    *   Instructions on setting up a development environment.
    *   Guidance on packaging and publishing an extension.
*   **Extension Manifest (`package.json`) Guide:**
    *   Detailed explanation of the `contributes.errorDetectors` section and its properties (`id`, `name`, `description`, `activationEvents`, `targetLanguageIds`, `targetTypes`).
    *   Explanation of general manifest properties like `name`, `version`, `publisher`, `engines`, `main`, and `activationEvents`.
*   **Lifecycle and Activation:**
    *   In-depth explanation of the extension lifecycle: packaging, installation, discovery, activation (with all event types), registration, invocation, and deactivation.
    *   Best practices for managing disposables and cleaning up resources in `activate` and `deactivate`.
*   **Development Best Practices:**
    *   **Performance:** Tips for writing efficient detectors, minimizing blocking operations, and using asynchronous patterns correctly. Guidance on leveraging `targetLanguageIds` and `targetTypes` for optimized invocation.
    *   **Security:** Reinforce the security considerations outlined below. Emphasize validating inputs and being cautious with external data.
    *   **User Experience (UX):** Guidelines for providing clear error messages, actionable suggestions, and appropriate severity levels. How to use `confidenceScore` effectively.
    *   **Error Handling within Extensions:** How to gracefully handle errors within the extension's own code and use `roo.extensions.log` for diagnostics.
*   **Example Extensions:**
    *   Provide source code for several example extensions demonstrating different capabilities (e.g., simple linter, LLM output checker, regex-based detector).
*   **Configuration and Settings:**
    *   How extensions can define their own configuration settings and access them using `roo.extensions.getConfiguration`.
*   **Debugging Extensions:**
    *   Instructions on how to debug Roo Code extensions, including using `roo.extensions.log`.
*   **API Versioning and Compatibility:**
    *   Explanation of the API versioning strategy and how extensions should specify `engines.rooCode`.
    *   Guidelines on how Roo Code will handle API changes and ensure backward compatibility where possible.

### 5.2. Security Considerations

Ensuring the security of Roo Code and its users when running third-party extensions is paramount. The following considerations and mitigation strategies will be implemented:

*   **Sandboxing / Process Isolation:**
    *   **Strategy:** Extensions should ideally run in a separate, sandboxed process (an "Extension Host") similar to VS Code's architecture. This isolates Roo Code's main process from extension code, preventing direct memory access or interference.
    *   **Benefits:** Protects against crashes in extensions affecting Roo Code's stability; limits the scope of potential exploits.
    *   **Considerations:** Inter-process communication (IPC) overhead. The design of the API (data structures, invocation methods) must be IPC-friendly. Task 2.3 (Sandbox Mode Implementation) provides foundational principles for such isolation.

*   **Permissions Model:**
    *   **Strategy:** Implement a granular permissions model. Extensions must declare required permissions in their manifest (e.g., access to file system, network requests, specific Roo Code APIs).
    *   **User Consent:** Users will be prompted to review and approve these permissions upon installation or when an extension attempts to use a new permission.
    *   **Principle of Least Privilege:** Extensions should only be granted the minimum permissions necessary for their declared functionality.
    *   **API Access Control:** The `roo.extensions` API itself will act as a controlled gateway. Access to more sensitive internal Roo Code functions will not be exposed directly.

*   **Input Sanitization and Validation:**
    *   **Roo Code Responsibility:** Roo Code will validate and sanitize data passed *to* extensions via `TaskContext` and `AnalysisTarget` to prevent injection attacks against extensions.
    *   **Extension Responsibility:** Extensions must validate and sanitize any data they receive (especially `content` in `AnalysisTarget`) before processing it, particularly if it's used to construct file paths, shell commands, or database queries. Documentation must strongly emphasize this.

*   **Resource Limits and Monitoring:**
    *   **Strategy:** The Extension Host should monitor resource consumption (CPU, memory, execution time) of each extension.
    *   **Throttling/Termination:** Roo Code should be able to throttle or terminate misbehaving extensions that consume excessive resources or become unresponsive.
    *   **Performance Profiling:** Provide tools or guidance for extension developers to profile their extension's performance.

*   **Code Signing and Verification (Future Consideration):**
    *   **Strategy:** For a trusted marketplace, consider requiring extensions to be signed. Roo Code could then verify signatures before loading.
    *   **Benefits:** Helps ensure extension authenticity and integrity, reducing the risk of tampered or malicious code.

*   **API Rate Limiting (If applicable):**
    *   If extensions can make frequent calls to certain Roo Code APIs (e.g., for configuration or state), consider rate limiting to prevent abuse.

*   **Secure Data Storage:**
    *   If extensions need to store sensitive data, Roo Code should provide a secure storage API (e.g., leveraging system keychain services), rather than extensions implementing their own insecure storage. The `ExtensionContext` could provide access to such an API.

*   **Clear Uninstallation and Cleanup:**
    *   Ensure that uninstalling an extension completely removes its code and any stored data (unless explicitly kept by user action).

*   **Reporting Vulnerabilities:**
    *   Establish a clear process for developers and users to report security vulnerabilities found in extensions or the Extension API itself.

*   **User Awareness and Control:**
    *   Users should be able to easily see which extensions are installed, what permissions they have, and disable or uninstall them.
    *   Provide clear indicators when an extension is active or has contributed to an analysis.