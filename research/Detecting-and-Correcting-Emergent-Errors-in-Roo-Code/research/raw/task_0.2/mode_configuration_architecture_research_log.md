---
title: Mode Configuration Architecture Research Log
task_id: task_0.2
date: 2025-05-19
last_updated: 2025-05-19
status: DRAFT
owner: deep-research-agent
---

# Mode Configuration Architecture Research Log

## Research Process

### 1. Exploration of Repository Structure

Initial exploration revealed several key files and directories related to mode configuration and system prompt management:

- `Roo-Code/.roomodes`: Contains custom mode definitions
- `Roo-Code/src/shared/modes.ts`: Contains built-in mode definitions and mode management functions
- `Roo-Code/src/core/prompts/system.ts`: Responsible for generating system prompts
- `Roo-Code/src/core/webview/generateSystemPrompt.ts`: Integration point for system prompt generation
- `Roo-Code/src/core/tools/switchModeTool.ts`: Tool implementation for mode switching
- `Roo-Code/src/core/webview/ClineProvider.ts`: Handles mode switching and state management
- `Roo-Code/src/core/config/CustomModesManager.ts`: Manages custom modes from different sources

### 2. Analysis of Mode Configuration System

#### Mode Definition Sources
1. **Built-in Modes**: Defined in `shared/modes.ts`
   - Includes standard modes like "code", "architect", "ask", "debug", "orchestrator"
   - Each mode has a slug, name, role definition, and permission groups

2. **Custom Modes**: Defined in `.roomodes` file (project-specific) or global settings
   - Project-specific modes take precedence over global modes
   - Custom modes follow the same structure as built-in modes

#### Mode Loading and Merging
- `CustomModesManager` is responsible for:
  - Loading modes from both sources
  - Merging them with project modes taking precedence
  - Watching for changes in both files
  - Caching mode configurations for performance

### 3. Analysis of System Prompt Management

#### System Prompt Construction
- `system.ts` contains the `SYSTEM_PROMPT` function that:
  - Checks for file-based system prompt overrides first
  - Falls back to generating a prompt dynamically if no override exists
  - Combines various sections like role definition, tool descriptions, capabilities, rules

#### System Prompt Sections
- Role definition (from mode config)
- Markdown formatting section
- Tool use section with tool descriptions specific to the mode
- Tool use guidelines
- MCP servers section (if applicable)
- Capabilities section
- Modes section
- Rules section
- System info section
- Objective section
- Custom instructions

### 4. Analysis of Mode Switching

- `switchModeTool.ts` provides the user-facing tool for mode switching
- `ClineProvider.handleModeSwitch` performs the actual mode switch by:
  - Updating the global state with the new mode
  - Loading the saved API config for the new mode
  - Posting the updated state to the webview

### 5. Telemetry and Monitoring Integration

- `TelemetryService` already captures mode switching events
- `PostHogClient` defines various events including `MODE_SWITCH`
- No specific monitoring for system prompt application anomalies

## Key Files Examined

1. `Roo-Code/.roomodes`: Custom mode definitions
2. `Roo-Code/src/shared/modes.ts`: Built-in mode definitions and management functions
3. `Roo-Code/src/core/prompts/system.ts`: System prompt generation
4. `Roo-Code/src/core/webview/generateSystemPrompt.ts`: System prompt integration
5. `Roo-Code/src/core/tools/switchModeTool.ts`: Mode switching tool
6. `Roo-Code/src/core/webview/ClineProvider.ts`: Provider with mode switching logic
7. `Roo-Code/src/core/config/CustomModesManager.ts`: Custom modes management
8. `Roo-Code/src/services/telemetry/TelemetryService.ts`: Telemetry service
9. `Roo-Code/src/services/telemetry/PostHogClient.ts`: Event tracking implementation

## Insights and Observations

1. **Mode Configuration Flexibility**:
   - Roo Code supports both built-in and custom modes
   - Custom modes can be defined at project level or globally
   - Project-specific modes take precedence over global modes

2. **System Prompt Customization**:
   - System prompts can be overridden completely via file-based prompts
   - Default system prompts are dynamically generated based on various components
   - The system prompt integrates mode-specific permissions and capabilities

3. **Potential Monitoring Points**:
   - The mode switching process already has telemetry integration
   - System prompt construction lacks specific monitoring for anomalies
   - Several integration points identified for prompt monitoring

## Next Steps

1. Create architectural diagram illustrating the mode management system
2. Document identified monitoring integration points
3. Create final synthesis document with comprehensive analysis