# Building a Structured Transparent and Well Documented AI Team (In Roo Code)

**Building a Structured, Transparent, and Well-Documented AI Team that Delegates Its Own Tasks**

## 🙏 Support This Work

If this project helps you build better AI systems and you'd like to show your appreciation:

- **Buy Me a Coffee**: [https://buymeacoffee.com/mnehmos](https://buymeacoffee.com/mnehmos)
- **Check out Vario Research**: For advanced Deep Research alternatives (Talking about you Gemini, ChatGPT), visit [https://mnehmos.github.io/VarioResearch/](https://mnehmos.github.io/VarioResearch/) for custom reports in any format (I Prefer customized websites so i can add in API functionalities into your dashboards as needed. (Alpha Vantage, Yahoo Finance, Arxiv, google maps, etc))

## 🌟 Key Features

- **Multi-Agent Framework**: Specialized modes for different types of tasks
- **SPARC Framework**: Structured approach to complex problem-solving
- **Agentic Boomerang**: Reliable task delegation and tracking system
- **Structured Documentation**: Consistent, traceable documentation
- **Token Optimization**: Efficient resource usage through the "Scalpel, not Hammer" approach

## 🧩 Specialized Modes

The system includes the following specialized modes:

- **🪃 Orchestrator**: Task decomposition, assignment, and verification
- **💻 Code**: Software implementation and optimization
- **🏛️ Architect**: System design and pattern application
- **❓ Ask**: Information retrieval, evaluation, and communication
- **🪲 Debug**: Problem diagnosis and solution validation
- **💾 Memory**: Knowledge storage, organization, and retrieval
- **🔍 Deep Research**: In-depth investigation and analysis

## 🏗️ Architecture

Below is an architectural overview of how the Roo framework operates:

```
┌─────────────────────────────────┐
│            VS Code              │
│     (Primary Development        │
│          Environment)           │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│             Roo Code            │
│                ↓                │
│          System Prompt          │
│   (Contains SPARC Framework:    │
│    • Specification, Pseudocode, │
│      Architecture, Refinement,  │
│      Completion methodology     │
│    • Advanced reasoning models  │
│    • Best practices enforcement │
│    • Memory Bank integration    │
│    • Boomerang pattern support) │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐      ┌─────────────────────────┐
│           Orchestrator          │      │         User            │
│     (System Prompt contains:    │      │     (Customer with      │
│      roles, definitions,        │◄─────┤     minimal context)    │
│      systems, processes,        │      │                         │
│      nomenclature, etc.)        │      └─────────────────────────┘
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│        Query Processing         │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│         MCP → Reprompt          │
│     (Only called on direct      │
│         user input)             │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│     Structured Prompt Creation  │
│                                 │
│       Project Prompt Eng.       │
│       Project Context           │
│       System Prompt             │
│       Role Prompt               │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│           Orchestrator          │
│     (System Prompt contains:    │
│      roles, definitions,        │
│      systems, processes,        │
│      nomenclature, etc.)        │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│         Subtask Prompt         │
│   (Generated by Orchestrator    │
│        with structure)          │
│                                 │
│    ┌─────────┐  ┌─────────┐    │
│    │  Topic  │  │ Context │    │
│    └─────────┘  └─────────┘    │
│                                 │
│    ┌─────────┐  ┌─────────┐    │
│    │  Scope  │  │ Output  │    │
│    └─────────┘  └─────────┘    │
│                                 │
│    ┌─────────────────────┐     │
│    │       Extras        │     │
│    └─────────────────────┘     │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐   ┌────────────────────────────────────┐
│       Specialized Modes         │   │           MCP Tools                 │
│                                 │   │                                     │
│  ┌────────┐ ┌────────┐ ┌─────┐ │   │ ┌─────────┐  ┌─────────────────┐   │
│  │  Code  │ │ Debug  │ │ ... │ │──►│ │ Basic   │  │ CLI/Shell        │   │
│  └────┬───┘ └────┬───┘ └──┬──┘ │   │ │ CRUD    │  │ (cmd/PowerShell) │   │
│       │          │        │    │   │ └─────────┘  └─────────────────┘   │
└───────┼──────────┼────────┼────┘   │                                     │
        │          │        │        │ ┌─────────┐  ┌─────────────────┐   │
        │          │        │        │ │ API     │  │ Browser          │   │
        │          │        └───────►│ │ Calls   │  │ Automation       │   │
        │          │                 │ │ (Alpha  │  │ (Playwright)     │   │
        │          │                 │ │ Vantage)│  │                  │   │
        │          │                 │ └─────────┘  └─────────────────┘   │
        │          │                 │                                     │
        │          └────────────────►│ ┌──────────────────────────────┐   │
        │                            │ │        LLM Calls              │   │
        │                            │ │                               │   │
        │                            │ │ • Basic Queries               │   │
        └───────────────────────────►│ │ • Reporter Format            │   │
                                     │ │ • Logic MCP Primitives        │   │
                                     │ │ • Sequential Thinking         │   │
                                     │ └──────────────────────────────┘   │
                                     └────────────────┬─────────────────┬─┘
                                                      │                 │
                                                      ▼                 │
┌─────────────────────────────────────────────────────────────────┐    │
│                   Recursive Loop                                │    │
│                                                                 │    │
│  ┌────────────────────────┐    ┌───────────────────────┐       │    │
│  │     Task Execution     │    │      Reporting        │       │    │
│  │                        │    │                       │       │    │
│  │ • Execute assigned task│───►│ • Report work done    │       │◄───┘
│  │ • Solve specific issue │    │ • Share issues found  │       │
│  │ • Maintain focus       │    │ • Provide learnings   │       │
│  └────────────────────────┘    └─────────┬─────────────┘       │
│                                           │                     │
│                                           ▼                     │
│  ┌────────────────────────┐    ┌───────────────────────┐       │
│  │   Task Delegation      │    │    Deliberation       │       │
│  │                        │◄───┤                       │       │
│  │ • Identify next steps  │    │ • Assess progress     │       │
│  │ • Assign to best mode  │    │ • Integrate learnings │       │
│  │ • Set clear objectives │    │ • Plan next phase     │       │
│  └────────────────────────┘    └───────────────────────┘       │
│                                                                 │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Memory Mode                                  │
│                                                                 │
│  ┌────────────────────────┐    ┌───────────────────────┐       │
│  │  Project Archival      │    │   SQL Database        │       │
│  │                        │    │                       │       │
│  │ • Create memory folder │───►│ • Store project data  │       │
│  │ • Extract key learnings│    │ • Index for retrieval │       │
│  │ • Organize artifacts   │    │ • Version tracking    │       │
│  └────────────────────────┘    └─────────┬─────────────┘       │
│                                           │                     |
│                                           ▼                     │
│  ┌────────────────────────┐    ┌───────────────────────┐       │
│  │  Memory MCP            │    │   RAG System          │       │
│  │                        │◄───┤                       │       │
│  │ • Database writes      │    │ • Vector embeddings   │       │
│  │ • Data validation      │    │ • Semantic indexing   │       │
│  │ • Structured storage   │    │ • Retrieval functions │       │
│  └─────────────┬──────────┘    └───────────────────────┘       │
│                │                                               │
└────────────────┼───────────────────────────────────────────────┘
                 │
                 └───────────────────────────────────┐
                                                     ▼
┌─────────────────────────────────┐      ┌─────────────────────────┐
│           Orchestrator          │      │         User            │
│     (System Prompt contains:    │      │     (Customer with      │
│      roles, definitions,        │◄─────┤     minimal context)    │
│      systems, processes,        │      │                         │
│      nomenclature, etc.)        │      └─────────────────────────┘
└───────────────┬─────────────────┘
|
              Restart Recursive Loop
```
## 🚀 Getting Started

### Prerequisites

- A compatible AI assistant that supports custom modes
- Basic understanding of the SPARC framework concepts

### Installation

#### Option 1: NPM (Coming Soon)

```

```
=======

#### Option 2: Manual Setup

1. Clone this repository:
   ```
   git clone https://github.com/Mnehmos/The-Ultimate-Roo-Code-Hack-Building-a-Structured-Transparent-and-Well-Documented-AI-Team.git
   ```

2. Copy the `.roomodes` file to your project root

3. Configure your AI assistant to use the custom modes:
   - Click the "Modes" button in the Roo sidebar
   - Select "Edit Project Modes (.roomodes)"
   - Verify that the content matches the `.roomodes` file from this repository
   - Click "Save"

4. Set up the custom instructions:
   - Click the "Modes" button in the Roo sidebar
   - Scroll down to "Custom Instructions for All Modes"
   - Copy the contents of `templates/custom-instructions-for-all-modes.md`
   - Paste into the Custom Instructions field
   - Click "Save"

5. Create the `.roo` directory structure:
   - Create a `.roo` directory in your project root
   - Add subdirectories for each mode: `rules-orchestrator`, `rules-code`, etc.
   - Create a `logs` directory for activity tracking
   - Add a `memory` directory for knowledge storage

6. Initialize the boomerang state:
   - Create a `.roo/boomerang-state.json` file with an empty JSON object: `{}`

#### Option 3: Direct Setup with AI Assistant

If you prefer to set up the framework directly using an AI assistant like Roo, Claude, or ChatGPT, you can copy and paste the following prompt:

```
I want to set up the Ultimate Roo Code Hack multi-agent framework. Please help me:

1. Create a .roomodes file with configurations for these specialized modes:
   - Orchestrator (task management and delegation)
   - Code (software implementation)
   - Architect (system design)
   - Ask (information discovery)
   - Debug (problem diagnosis)
   - Memory (knowledge management)
   - Deep Research (in-depth investigation)

2. Create a meet-the-team.md file that describes each mode as a team member in plain English

3. Set up custom instructions that implement:
   - The SPARC framework for structured reasoning
   - Boomerang logic for task delegation
   - Token optimization strategies
   - Standardized documentation formats

Please provide the complete content for each file and instructions on how to use them.
```

### Additional Configuration

#### Configure Enhance Prompt (Optional)
1. Click the "Support Prompts" button in the Roo sidebar
2. Select "Enhance Prompt"
3. Copy the contents of `templates/enhance-prompt-template.md`
4. Paste into the Prompt field
5. Click "Save"

This feature helps transform basic prompts into comprehensive, structured project prompts.

## 🧩 Basic Usage

1. **Start with Orchestrator Mode** - This is your project manager who will coordinate everything
2. **Describe your project** - Be as detailed as possible in your initial prompt
3. **Let Orchestrator break it down** - It will create subtasks and delegate to specialist modes
4. **Review the results** - Orchestrator will integrate all the pieces and present the final result

## 🧩 Using the Modes

### Switching Modes
1. Click on the current mode name in the bottom left corner of the Roo interface
2. Select the desired mode from the dropdown menu

### Using the Enhance Prompt Feature
1. Type your basic prompt in the chat
2. Click the ✨ button next to the send button
3. Roo will transform your basic prompt into a comprehensive, structured project prompt

### Creating Custom Tasks
When creating tasks for specialist modes, use the standardized task prompt format:

```markdown
# [Task Title]

## Context
[Background information and relationship to the larger project]

## Scope
[Specific requirements and boundaries for the task]

## Expected Output
[Detailed description of deliverables]

## Additional Resources
[Relevant tips, examples, or reference materials]
```

This structured format ensures that specialist modes have all the information they need to complete tasks effectively and consistently.

## 🔄 The Boomerang Pattern

The Boomerang Pattern ensures reliable task delegation and tracking:

1. Add new modes by updating `config.json` and `.roomodes`
2. Create corresponding rule files in `.roo/rules-{new-mode}/rules.md`
3. Implement mode-specific logging in `.roo/logs/{new-mode}-activity.md`
4. Update memory indexes to accommodate new artifact types

> **Note**: While `.roomodes` is used for mode assignments, the `.roo` directory structure is still used for keeping notes, logs, and documenting activity and changes.

## 📊 Performance Optimization

- Keep context window utilization below 40%
- Start with the least token-intensive cognitive primitives
- Break complex tasks into atomic components
- Use the most specialized mode for each subtask

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- The SPARC framework developers
- Contributors to the multi-agent AI research community (Roo Code, huge shoutout)
- All users who provide feedback and suggestions
