# Product Requirements Document: Roo Code - Multi-Level Handoff & Memory Bank "Roomodes"
Version: 1.0
Date: June 4, 2025
Author: Gemini AI (Collaboratively with User)
Related PRD: Roo Code - FastAPI Database Persistence Layer (ID: roo_code_db_prd)

## 1. Introduction
This document outlines the requirements for implementing "Roomodes" – a system of specialized operational modes within Roo Code. This system will feature a multi-level handoff mechanism for task delegation and a sophisticated memory bank for context management, learning, and inter-mode communication. The goal is to enhance Roo Code's intelligence, adaptability, and problem-solving capabilities by allowing different "agents" or modes to collaborate on complex tasks, inspired by concepts from projects like Ennwise AI, Roo Commander, Pheromind, and BMAD.

## 2. Goals
- **Specialized Expertise**: Enable Roo Code to tackle diverse aspects of software development and problem-solving by delegating tasks to specialized "Roomodes" (e.g., planning, coding, research, testing).
- **Enhanced Problem Decomposition**: Allow a high-level "Orchestrator" Roomode to break down complex user goals into manageable sub-tasks for other Roomodes.
- **Intelligent Handoff**: Implement a robust mechanism for transferring control and context (relevant memories, task outputs) between Roomodes.
- **Sophisticated Memory System**: Develop a multi-tiered memory bank (global, local/mode-specific, shared scratchpad, long-term knowledge base) to support contextual understanding, learning, and efficient information sharing.
- **Evolving Intelligence (Ennwise AI inspired)**: Facilitate learning and adaptation by storing insights, successful solutions, and error patterns in the long-term knowledge base.
- **Strategic Orchestration (Roo Commander inspired)**: Establish a clear hierarchy or workflow for how Roomodes are activated and managed.
- **Distributed Cognition (Pheromind inspired)**: Allow Roomodes to leave "traces" or "pheromones" (structured data in the shared memory) for others to pick up, guiding subsequent actions.
- **Domain-Specific Application (BMAD inspired)**: Lay the groundwork for creating Roomodes tailored to specific domains or methodologies within software development (e.g., UI/UX, backend, security).
- **Modularity and Extensibility**: Design the Roomode framework to be easily extendable with new modes and capabilities.

## 3. Target Users
- **Primary**: The Roo Code application itself, which will leverage Roomodes to fulfill user requests more effectively.
- **Secondary**: Developers of Roo Code, who will be able to create, configure, and extend Roomodes and their interactions.

## 4. Functional Requirements

### 4.1. Core Roomode Framework
**FR4.1.1 Roomode Definition**: The system must allow for the definition of distinct Roomodes, each with:
- A unique identifier.
- A specific purpose or area of expertise.
- A defined set of inputs it can process (e.g., task descriptions, memory objects, user queries).
- A defined set of outputs it can produce (e.g., code, reports, updated task statuses, new memory objects).
- Access permissions to different tiers of the Memory Bank.

**FR4.1.2 Roomode Lifecycle**: Each Roomode will have a lifecycle (e.g., idle, active, paused, completed, error).

**FR4.1.3 Roomode Registration**: A mechanism for registering and discovering available Roomodes within the system.

### 4.2. Orchestrator Roomode ("Roo Commander" Inspired)
**FR4.2.1 Goal Ingestion**: The Orchestrator must be able to receive and parse high-level goals from the user or other system components.

**FR4.2.2 Task Decomposition**: It must be capable of breaking down complex goals into a sequence or graph of smaller, actionable tasks suitable for delegation to specialized Roomodes. This may involve LLM interaction.

**FR4.2.3 Roomode Selection & Activation**: Based on the nature of a sub-task, the Orchestrator must select the appropriate Roomode(s) and activate them.

**FR4.2.4 Workflow Management**: The Orchestrator will manage the overall flow of execution, including sequential and potentially parallel activation of Roomodes.

**FR4.2.5 Progress Monitoring**: It must monitor the progress and status of delegated tasks and Roomodes.

**FR4.2.6 Result Aggregation**: The Orchestrator will be responsible for aggregating results from various Roomodes to fulfill the initial user goal.

### 4.3. Specialized Roomodes (Examples)
The initial implementation should consider a few core specialized Roomodes:

**FR4.3.1 Planning Roomode**:
- Input: High-level task or goal from the Orchestrator.
- Function: Performs detailed task breakdown, identifies dependencies, estimates effort/resources (potentially interacting with the database for historical data), and populates the Task list in the database (via API calls to the persistence layer).
- Output: A structured plan (list of tasks with details, stored in the database).

**FR4.3.2 Coding Roomode**:
- Input: Specific coding task, relevant context from memory (e.g., existing codebase snippets, API documentation, user requirements).
- Function: Generates, modifies, or debugs code. Interacts with LLMs for code generation. May interact with a file system or version control.
- Output: Code (as text or file changes), status updates, new memories (e.g., challenges encountered, solutions found).

**FR4.3.3 Research/Learning Roomode ("Ennwise AI" Inspired)**:
- Input: A query, a topic to research, or an unknown concept encountered by another Roomode.
- Function: Uses tools (e.g., web search, document parsing) and LLMs to gather and synthesize information.
- Output: Summarized findings, relevant links, new entries for the Memory Bank (e.g., API specs, tutorials, explanations).

**FR4.3.4 Testing Roomode**:
- Input: Code to be tested, test specifications, or a general directive to test a feature.
- Function: Generates test cases (potentially with LLM assistance), executes tests (if integrated with testing frameworks), analyzes results.
- Output: Test results, bug reports (which could become new tasks), updated task statuses.

**FR4.3.5 User Interaction Roomode**:
- Input: Need for clarification, request for feedback, presentation of results.
- Function: Formulates questions for the user, presents information, parses user responses.
- Output: User input, clarifications for other Roomodes.

### 4.4. Memory Bank System
The Memory Bank will be crucial for context and learning, interacting with the FastAPI Database Persistence Layer.

**FR4.4.1 Global Memory**:
- Content: High-level project goals, overall architecture, critical user constraints, key decisions made by the Orchestrator.
- Access: Primarily managed by the Orchestrator; readable by most specialized Roomodes.
- Persistence: Stored in the database (e.g., within Project descriptions or a dedicated GlobalMemory table linked to projects).

**FR4.4.2 Local/Mode-Specific Memory (Working Memory)**:
- Content: Information directly relevant to a Roomode's current, active task (e.g., API details for Coding Roomode, specific search results for Research Roomode). This is transient or short-term.
- Access: Primarily private to the active Roomode.
- Persistence: May be temporarily stored in memory during Roomode execution or as short-lived entries in the database's Memory table, possibly tagged with the Roomode instance ID.

**FR4.4.3 Shared Scratchpad/Handoff Area ("Pheromones")**:
- Content: Structured data representing the output of one Roomode intended as direct input or context for the next Roomode in a sequence. Examples: file paths of generated code, list of identified issues, summary of user feedback.
- Access: Written by a completing Roomode, read by the next activated Roomode(s). Managed by the Orchestrator.
- Persistence: Could be transient if handoff is immediate, or stored temporarily in the Memory table with a specific "handoff" type and linked to tasks or Roomode transitions.

**FR4.4.4 Long-Term Knowledge Base (LTKB)**:
- Content: Curated insights, learned patterns, successful solutions to common problems, resolved error explanations, user preferences, effective prompts, validated code snippets, summaries of external documentation.
- Access: Writable by Roomodes (especially Research/Learning and after successful task completion), readable by all Roomodes for improving performance and decision-making.
- Persistence: Stored in the Memory table of the database, with appropriate tagging for type, relevance, and retrieval (e.g., keywords, embeddings for semantic search). This directly supports the "Ennwise AI" concept.

**FR4.4.5 Memory CRUD**: The system (likely via the Orchestrator or specialized memory management functions) must be able to create, read, update, and delete memory entries in the database via the existing FastAPI layer.

**FR4.4.6 Memory Retrieval**: Mechanisms for effective memory retrieval, potentially including:
- Keyword search.
- Tag-based filtering.
- Semantic search (future consideration, might involve vector embeddings).
- Contextual relevance scoring.

### 4.5. Handoff Mechanism
**FR4.5.1 Contextual Handoff**: When control is passed from one Roomode to another, all necessary context (relevant global memories, specific outputs from the Shared Scratchpad, pointers to relevant LTKB entries) must be made available to the receiving Roomode.

**FR4.5.2 Explicit Handoffs**: The Orchestrator will explicitly trigger the next Roomode in a sequence, providing it with the required context.

**FR4.5.3 Conditional Handoffs**: The Orchestrator should be able to determine the next Roomode based on the outcome or output of the current Roomode (e.g., if Coding Roomode produces errors, handoff to Debugging/Research Roomode; if successful, handoff to Testing Roomode).

**FR4.5.4 Handoff Data Packaging**: Data passed during handoff should be structured (e.g., using Pydantic models or standardized dictionaries).

## 5. High-Level Technical Design
**Roomode Implementation**: Each Roomode can be implemented as a Python class or module.
- Each Roomode class will have a primary execution method (e.g., execute(task_details, memory_accessor)).
- Roomodes will interact with the Memory Bank and the Task List (Projects, Epics, Tasks) via API calls to the FastAPI Database Persistence Layer.
- Roomodes requiring LLM interactions will use the unified LLM service (e.g., Not Diamond, liteLLM, Portkey as discussed previously).

**Orchestrator Logic**: The Orchestrator will maintain the state of the overall goal and the sub-tasks. It will likely use a state machine or a workflow engine pattern to manage Roomode transitions.

**Memory Access Layer**: A dedicated module or set of functions will abstract the interaction with the Memory Bank (which in turn calls the FastAPI endpoints for the Memory table and other relevant data). This layer will handle formatting data for storage and retrieval.

**Integration with Database API**: All persistent state (task definitions, task statuses, long-term memories, global context) will be stored and retrieved using the API endpoints defined in the roo_code_db_prd.
- Example: The Planning Roomode, after decomposing a goal, will make POST requests to /tasks/ to create new tasks.
- Example: The Research Roomode will make POST requests to a (future) /memories/ endpoint to store its findings.

**Configuration**: A configuration system will be needed to define available Roomodes, their parameters, and potentially default workflows or routing rules for the Orchestrator.

**Conceptual Flow**:
1. User provides a high-level goal to Roo Code.
2. The Orchestrator Roomode ingests the goal.
3. Orchestrator consults its internal logic and potentially the LTKB (via Memory Access Layer -> DB API) to decompose the goal into a plan of sub-tasks.
4. Orchestrator activates the Planning Roomode.
5. Planning Roomode refines the plan, creates detailed task entries in the database (via DB API: POST /tasks/, POST /epics/).
6. Orchestrator, based on the first task, selects and activates an appropriate Specialized Roomode (e.g., Coding Roomode). It provides context from Global Memory and the Shared Scratchpad (if any).
7. The Specialized Roomode executes its function:
   - Reads from various Memory Bank tiers (via Memory Access Layer -> DB API).
   - Performs its core logic (e.g., calls LLM service, interacts with file system).
   - Writes outputs to the Shared Scratchpad (via Memory Access Layer -> DB API).
   - Updates its task status in the database (via DB API: PUT /tasks/{task_id}).
   - Potentially contributes new knowledge to the LTKB (via Memory Access Layer -> DB API).
8. The Specialized Roomode signals completion to the Orchestrator.
9. Orchestrator evaluates the result, consults its workflow, and initiates handoff to the next appropriate Roomode (Steps 6-8 repeat).
10. If user interaction is needed, the User Interaction Roomode is activated.
11. Once all sub-tasks are completed, the Orchestrator aggregates the final result and presents it to the user.

## 6. Non-Functional Requirements
**NFR6.1 Performance**: Handoffs between Roomodes should be efficient. Memory retrieval should be fast enough not to become a bottleneck.

**NFR6.2 Scalability**: The framework should allow for adding many Roomodes without significant performance degradation in the orchestration logic. The underlying database API handles data scalability.

**NFR6.3 Maintainability**: Roomode logic should be well-encapsulated. The Memory Bank interaction logic should be clean and reusable.

**NFR6.4 Testability**: Individual Roomodes should be testable in isolation. The orchestration logic should also be testable with mock Roomodes.

**NFR6.5 Configurability**: It should be easy to configure which Roomodes are active, and potentially define or modify orchestration workflows.

## 7. Future Considerations / Next Steps
- **Advanced Orchestration**: Explore more dynamic orchestration strategies, potentially using AI/LLMs to decide the next best Roomode or action.
- **Parallel Roomode Execution**: Allow for concurrent execution of independent Roomodes where applicable.
- **Semantic Memory Search**: Integrate vector embeddings and semantic search capabilities for more intelligent retrieval from the Long-Term Knowledge Base.
- **Roomode Discovery Service**: If the number of Roomodes grows significantly, a more dynamic discovery service might be needed.
- **Visual Workflow Editor**: For complex orchestrations, a visual tool to define and manage Roomode workflows could be beneficial.
- **Memory Prioritization and Garbage Collection**: Strategies for managing the size and relevance of the Memory Bank, especially the LTKB.

## 8. Assumptions and Dependencies
- The FastAPI Database Persistence Layer (as defined in roo_code_db_prd) is implemented and operational.
- A unified LLM interaction service is available for Roomodes that require it.
- The core Roo Code application can host and manage the lifecycle of the Orchestrator and other Roomodes.
- Initial Roomodes will be developed in Python.

This PRD lays the foundation for a significantly more intelligent and capable Roo Code by introducing a structured approach to specialized agents and memory management.