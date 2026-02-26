# Workspace Capability Catalog

> Auto-generated from `registry.yaml` — do not edit manually
> Re-generate: `python3 scripts/gen-catalog.py`

**Total: 257 entries** | 11 Agents | 239 Skills | 4 Commands | 3 MCPs
**Updated:** 2026-02-26

### By Vendor

| Vendor | Count |
|--------|-------|
| awesome-copilot | 198 |
| oh-my-opencode | 19 |
| anthropic-skills | 16 |
| superpowers | 14 |
| openspec | 8 |
| custom | 2 |

---

## Agents

| Name | Category | Model | Description | Profiles |
|------|----------|-------|-------------|----------|
| **sisyphus** | workflow | `github-copilot/claude-opus-4.6` | Persistent task executor — primary orchestrator for complex multi-step work | daily-dev, full-stack, minimal |
| **hephaestus** | code-quality | `system-default` | Code generation specialist — crafts implementation from specs and plans | daily-dev, full-stack, minimal |
| **oracle** | ai-tooling | `github-copilot/claude-opus-4.6` | Knowledge retrieval and deep question answering | daily-dev, full-stack |
| **librarian** | ai-tooling | `github-copilot/claude-sonnet-4.5` | Codebase indexing, file discovery, and context gathering | daily-dev, full-stack, minimal |
| **explore** | ai-tooling | `github-copilot/claude-haiku-4.5` | Fast codebase exploration — file search, grep, quick reads | daily-dev, full-stack, minimal |
| **atlas** | code-quality | `github-copilot/claude-sonnet-4.5` | Large-scale refactoring and cross-file changes | daily-dev, full-stack, minimal |
| **prometheus** | workflow | `github-copilot/claude-opus-4.6` | Architecture design and system-level reasoning | daily-dev, full-stack, minimal |
| **metis** | workflow | `github-copilot/claude-opus-4.6` | Strategic planning and task decomposition | daily-dev, full-stack |
| **momus** | code-quality | `github-copilot/claude-opus-4.6` | Code review and critical feedback | daily-dev, full-stack |
| **multimodal-looker** | ai-tooling | `github-copilot/claude-haiku-4.5` | Image and visual content analysis | full-stack |
| **sisyphus-junior** | workflow | `system-default` | Lightweight task executor for simpler background work | daily-dev, full-stack, minimal |

---

## Skills

### Ai Tooling (24)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **agent-browser** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/agent-browser/SKILL.md` | Automates browser interactions for web testing, form filling, screenshots, an... | daily-dev, full-stack, minimal |
| **dev-browser** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/dev-browser/SKILL.md` | Browser automation with persistent page state. | daily-dev, full-stack, minimal |
| **mcp-builder** | anthropic-skills | `vendor/anthropic-skills/skills/mcp-builder/SKILL.md` | Guide for creating high-quality MCP (Model Context Protocol) servers that ena... | daily-dev, full-stack, minimal |
| **find-skills** | custom | `skills/custom/find-skills/SKILL.md` | Helps users discover agent skills — checks the local workspace registry first... | daily-dev, full-stack, minimal |
| **agent-governance** | awesome-copilot | `vendor/awesome-copilot/skills/agent-governance/SKILL.md` | Patterns and techniques for adding governance, safety, and trust controls to ... | daily-dev, full-stack, minimal |
| **agentic-eval** | awesome-copilot | `vendor/awesome-copilot/skills/agentic-eval/SKILL.md` | Patterns and techniques for evaluating and improving AI agent outputs. | daily-dev, full-stack, minimal |
| **chrome-devtools** | awesome-copilot | `vendor/awesome-copilot/skills/chrome-devtools/SKILL.md` | Expert-level browser automation, debugging, and performance analysis using Ch... | daily-dev, full-stack, minimal |
| **create-agentsmd** | awesome-copilot | `vendor/awesome-copilot/skills/create-agentsmd/SKILL.md` | Prompt for generating an AGENTS.md file for a repository | daily-dev, full-stack, minimal |
| **csharp-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/csharp-mcp-server-generator/SKILL.md` | Generate a complete MCP server project in C# with tools, prompts, and proper ... | daily-dev, full-stack, minimal |
| **declarative-agents** | awesome-copilot | `vendor/awesome-copilot/skills/declarative-agents/SKILL.md` | Complete development kit for Microsoft 365 Copilot declarative agents with th... | daily-dev, full-stack, minimal |
| **finalize-agent-prompt** | awesome-copilot | `vendor/awesome-copilot/skills/finalize-agent-prompt/SKILL.md` | Finalize prompt file using the role of an AI agent to polish the prompt for t... | daily-dev, full-stack, minimal |
| **mcp-cli** | awesome-copilot | `vendor/awesome-copilot/skills/mcp-cli/SKILL.md` | Interface for MCP (Model Context Protocol) servers via CLI. | daily-dev, full-stack, minimal |
| **mcp-copilot-studio-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/mcp-copilot-studio-server-generator/SKILL.md` | Generate a complete MCP server implementation optimized for Copilot Studio in... | daily-dev, full-stack, minimal |
| **mcp-create-adaptive-cards** | awesome-copilot | `vendor/awesome-copilot/skills/mcp-create-adaptive-cards/SKILL.md` | Skill converted from mcp-create-adaptive-cards.prompt.md | daily-dev, full-stack, minimal |
| **mcp-create-declarative-agent** | awesome-copilot | `vendor/awesome-copilot/skills/mcp-create-declarative-agent/SKILL.md` | Skill converted from mcp-create-declarative-agent.prompt.md | daily-dev, full-stack, minimal |
| **mcp-deploy-manage-agents** | awesome-copilot | `vendor/awesome-copilot/skills/mcp-deploy-manage-agents/SKILL.md` | Skill converted from mcp-deploy-manage-agents.prompt.md | daily-dev, full-stack, minimal |
| **microsoft-skill-creator** | awesome-copilot | `vendor/awesome-copilot/skills/microsoft-skill-creator/SKILL.md` | Create agent skills for Microsoft technologies using Learn MCP tools. | daily-dev, full-stack, minimal |
| **playwright-automation-fill-in-form** | awesome-copilot | `vendor/awesome-copilot/skills/playwright-automation-fill-in-form/SKILL.md` | Automate filling in a form using Playwright MCP | daily-dev, full-stack, minimal |
| **python-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/python-mcp-server-generator/SKILL.md` | Generate a complete MCP server project in Python with tools, resources, and p... | daily-dev, full-stack, minimal |
| **remember-interactive-programming** | awesome-copilot | `vendor/awesome-copilot/skills/remember-interactive-programming/SKILL.md` | A micro-prompt that reminds the agent that it is an interactive programmer. | daily-dev, full-stack, minimal |
| **sql-optimization** | awesome-copilot | `vendor/awesome-copilot/skills/sql-optimization/SKILL.md` | Universal SQL performance optimization assistant for comprehensive query tuni... | daily-dev, full-stack, minimal |
| **tldr-prompt** | awesome-copilot | `vendor/awesome-copilot/skills/tldr-prompt/SKILL.md` | Create tldr summaries for GitHub Copilot files (prompts, agents, instructions... | daily-dev, full-stack, minimal |
| **typescript-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/typescript-mcp-server-generator/SKILL.md` | Generate a complete MCP server project in TypeScript with tools, resources, a... | daily-dev, full-stack, minimal |
| **typespec-create-agent** | awesome-copilot | `vendor/awesome-copilot/skills/typespec-create-agent/SKILL.md` | Generate a complete TypeSpec declarative agent with instructions, capabilitie... | daily-dev, full-stack, minimal |

### Code Quality (13)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **receiving-code-review** | superpowers | `vendor/superpowers/skills/receiving-code-review/SKILL.md` | Use when receiving code review feedback, before implementing suggestions, esp... | daily-dev, full-stack, minimal |
| **requesting-code-review** | superpowers | `vendor/superpowers/skills/requesting-code-review/SKILL.md` | Use when completing tasks, implementing major features, or before merging to ... | daily-dev, full-stack, minimal |
| **code-simplifier** | custom | `skills/custom/code-simplifier/SKILL.md` | Simplifies and refines code for clarity, consistency, and maintainability whi... | daily-dev, full-stack, minimal |
| **ai-prompt-engineering-safety-review** | awesome-copilot | `vendor/awesome-copilot/skills/ai-prompt-engineering-safety-review/SKILL.md` | Comprehensive AI prompt engineering safety review and improvement prompt. | daily-dev, full-stack, minimal |
| **apple-appstore-reviewer** | awesome-copilot | `vendor/awesome-copilot/skills/apple-appstore-reviewer/SKILL.md` | Serves as a reviewer of the codebase with instructions on looking for Apple A... | daily-dev, full-stack, minimal |
| **comment-code-generate-a-tutorial** | awesome-copilot | `vendor/awesome-copilot/skills/comment-code-generate-a-tutorial/SKILL.md` | Transform this Python script into a polished, beginner-friendly project by re... | daily-dev, full-stack, minimal |
| **java-refactoring-extract-method** | awesome-copilot | `vendor/awesome-copilot/skills/java-refactoring-extract-method/SKILL.md` | Refactoring using Extract Methods in Java Language | daily-dev, full-stack, minimal |
| **java-refactoring-remove-parameter** | awesome-copilot | `vendor/awesome-copilot/skills/java-refactoring-remove-parameter/SKILL.md` | Refactoring using Remove Parameter in Java Language | daily-dev, full-stack, minimal |
| **postgresql-code-review** | awesome-copilot | `vendor/awesome-copilot/skills/postgresql-code-review/SKILL.md` | PostgreSQL-specific code review assistant focusing on PostgreSQL best practic... | daily-dev, full-stack, minimal |
| **refactor** | awesome-copilot | `vendor/awesome-copilot/skills/refactor/SKILL.md` | Surgical code refactoring to improve maintainability without changing behavior. | daily-dev, full-stack, minimal |
| **refactor-method-complexity-reduce** | awesome-copilot | `vendor/awesome-copilot/skills/refactor-method-complexity-reduce/SKILL.md` | Refactor given method `${input:methodName}` to reduce its cognitive complexit... | daily-dev, full-stack, minimal |
| **review-and-refactor** | awesome-copilot | `vendor/awesome-copilot/skills/review-and-refactor/SKILL.md` | Review and refactor code in your project according to defined instructions | daily-dev, full-stack, minimal |
| **sql-code-review** | awesome-copilot | `vendor/awesome-copilot/skills/sql-code-review/SKILL.md` | Universal SQL code review assistant that performs comprehensive security, mai... | daily-dev, full-stack, minimal |

### Creative (4)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **algorithmic-art** | anthropic-skills | `vendor/anthropic-skills/skills/algorithmic-art/SKILL.md` | Creating algorithmic art using p5.js with seeded randomness and interactive p... | daily-dev, full-stack, minimal |
| **slack-gif-creator** | anthropic-skills | `vendor/anthropic-skills/skills/slack-gif-creator/SKILL.md` | Knowledge and utilities for creating animated GIFs optimized for Slack. | daily-dev, full-stack, minimal |
| **theme-factory** | anthropic-skills | `vendor/anthropic-skills/skills/theme-factory/SKILL.md` | Toolkit for styling artifacts with a theme. | daily-dev, full-stack, minimal |
| **azure-devops-cli** | awesome-copilot | `vendor/awesome-copilot/skills/azure-devops-cli/SKILL.md` | Manage Azure DevOps resources via CLI including projects, repos, pipelines, b... | daily-dev, full-stack, minimal |

### Devops (48)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **git-master** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/git-master/SKILL.md` | MUST USE for ANY git operations. Atomic commits, rebase/squash, history searc... | daily-dev, full-stack, minimal |
| **github-triage** | oh-my-opencode | `vendor/oh-my-opencode/.opencode/skills/github-triage/SKILL.md` | Unified GitHub triage for issues AND PRs. | daily-dev, full-stack, minimal |
| **using-git-worktrees** | superpowers | `vendor/superpowers/skills/using-git-worktrees/SKILL.md` | Use when starting feature work that needs isolation from current workspace or... | daily-dev, full-stack, minimal |
| **add-educational-comments** | awesome-copilot | `vendor/awesome-copilot/skills/add-educational-comments/SKILL.md` | Add educational comments to the file specified, or prompt asking for file to ... | daily-dev, full-stack, minimal |
| **aspire** | awesome-copilot | `vendor/awesome-copilot/skills/aspire/SKILL.md` | Aspire skill covering the Aspire CLI, AppHost orchestration, service discover... | daily-dev, full-stack, minimal |
| **az-cost-optimize** | awesome-copilot | `vendor/awesome-copilot/skills/az-cost-optimize/SKILL.md` | Analyze Azure resources used in the app (IaC files and/or resources in a targ... | daily-dev, full-stack, minimal |
| **azure-deployment-preflight** | awesome-copilot | `vendor/awesome-copilot/skills/azure-deployment-preflight/SKILL.md` | Performs comprehensive preflight validation of Bicep deployments to Azure, in... | daily-dev, full-stack, minimal |
| **azure-static-web-apps** | awesome-copilot | `vendor/awesome-copilot/skills/azure-static-web-apps/SKILL.md` | Helps create, configure, and deploy Azure Static Web Apps using the SWA CLI. | daily-dev, full-stack, minimal |
| **containerize-aspnet-framework** | awesome-copilot | `vendor/awesome-copilot/skills/containerize-aspnet-framework/SKILL.md` | Containerize an ASP.NET .NET Framework project by creating Dockerfile and .do... | daily-dev, full-stack, minimal |
| **containerize-aspnetcore** | awesome-copilot | `vendor/awesome-copilot/skills/containerize-aspnetcore/SKILL.md` | Containerize an ASP.NET Core project by creating Dockerfile and .dockerfile f... | daily-dev, full-stack, minimal |
| **copilot-usage-metrics** | awesome-copilot | `vendor/awesome-copilot/skills/copilot-usage-metrics/SKILL.md` | Retrieve and display GitHub Copilot usage metrics for organizations and enter... | daily-dev, full-stack, minimal |
| **create-architectural-decision-record** | awesome-copilot | `vendor/awesome-copilot/skills/create-architectural-decision-record/SKILL.md` | Create an Architectural Decision Record (ADR) document for AI-optimized decis... | daily-dev, full-stack, minimal |
| **create-github-action-workflow-specification** | awesome-copilot | `vendor/awesome-copilot/skills/create-github-action-workflow-specification/SKILL.md` | Create a formal specification for an existing GitHub Actions CI/CD workflow, ... | daily-dev, full-stack, minimal |
| **create-github-issue-feature-from-specification** | awesome-copilot | `vendor/awesome-copilot/skills/create-github-issue-feature-from-specification/SKILL.md` | Create GitHub Issue for feature request from specification file using feature... | daily-dev, full-stack, minimal |
| **create-github-issues-feature-from-implementation-plan** | awesome-copilot | `vendor/awesome-copilot/skills/create-github-issues-feature-from-implementation-plan/SKILL.md` | Create GitHub Issues from implementation plan phases using feature_request.ym... | daily-dev, full-stack, minimal |
| **create-github-issues-for-unmet-specification-requirements** | awesome-copilot | `vendor/awesome-copilot/skills/create-github-issues-for-unmet-specification-requirements/SKILL.md` | Create GitHub Issues for unimplemented requirements from specification files ... | daily-dev, full-stack, minimal |
| **create-github-pull-request-from-specification** | awesome-copilot | `vendor/awesome-copilot/skills/create-github-pull-request-from-specification/SKILL.md` | Create GitHub Pull Request for feature request from specification file using ... | daily-dev, full-stack, minimal |
| **create-llms** | awesome-copilot | `vendor/awesome-copilot/skills/create-llms/SKILL.md` | Create an llms.txt file from scratch based on repository structure following ... | daily-dev, full-stack, minimal |
| **create-specification** | awesome-copilot | `vendor/awesome-copilot/skills/create-specification/SKILL.md` | Create a new specification file for the solution, optimized for Generative AI... | daily-dev, full-stack, minimal |
| **create-technical-spike** | awesome-copilot | `vendor/awesome-copilot/skills/create-technical-spike/SKILL.md` | Create time-boxed technical spike documents for researching and resolving cri... | daily-dev, full-stack, minimal |
| **entra-agent-user** | awesome-copilot | `vendor/awesome-copilot/skills/entra-agent-user/SKILL.md` | Create Agent Users in Microsoft Entra ID from Agent Identities, enabling AI a... | daily-dev, full-stack, minimal |
| **generate-custom-instructions-from-codebase** | awesome-copilot | `vendor/awesome-copilot/skills/generate-custom-instructions-from-codebase/SKILL.md` | Migration and code evolution instructions generator for GitHub Copilot. | daily-dev, full-stack, minimal |
| **gh-cli** | awesome-copilot | `vendor/awesome-copilot/skills/gh-cli/SKILL.md` | GitHub CLI (gh) comprehensive reference for repositories, issues, pull reques... | daily-dev, full-stack, minimal |
| **git-commit** | awesome-copilot | `vendor/awesome-copilot/skills/git-commit/SKILL.md` | Execute git commit with conventional commit message analysis, intelligent sta... | daily-dev, full-stack, minimal |
| **git-flow-branch-creator** | awesome-copilot | `vendor/awesome-copilot/skills/git-flow-branch-creator/SKILL.md` | Intelligent Git Flow branch creator that analyzes git status/diff and creates... | daily-dev, full-stack, minimal |
| **github-copilot-starter** | awesome-copilot | `vendor/awesome-copilot/skills/github-copilot-starter/SKILL.md` | Set up complete GitHub Copilot configuration for a new project based on techn... | daily-dev, full-stack, minimal |
| **github-issues** | awesome-copilot | `vendor/awesome-copilot/skills/github-issues/SKILL.md` | Create, update, and manage GitHub issues using MCP tools. | daily-dev, full-stack, minimal |
| **go-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/go-mcp-server-generator/SKILL.md` | Generate a complete Go MCP server project with proper structure, dependencies... | daily-dev, full-stack, minimal |
| **java-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/java-mcp-server-generator/SKILL.md` | Generate a complete Model Context Protocol server project in Java using the o... | daily-dev, full-stack, minimal |
| **kotlin-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/kotlin-mcp-server-generator/SKILL.md` | Generate a complete Kotlin MCP server project with proper structure, dependen... | daily-dev, full-stack, minimal |
| **make-skill-template** | awesome-copilot | `vendor/awesome-copilot/skills/make-skill-template/SKILL.md` | Create new Agent Skills for GitHub Copilot from prompts or by duplicating thi... | daily-dev, full-stack, minimal |
| **mcp-configure** | awesome-copilot | `vendor/awesome-copilot/skills/mcp-configure/SKILL.md` | Configure an MCP server for GitHub Copilot with your Dataverse environment. | daily-dev, full-stack, minimal |
| **meeting-minutes** | awesome-copilot | `vendor/awesome-copilot/skills/meeting-minutes/SKILL.md` | Generate concise, actionable meeting minutes for internal meetings. Includes ... | daily-dev, full-stack, minimal |
| **microsoft-docs** | awesome-copilot | `vendor/awesome-copilot/skills/microsoft-docs/SKILL.md` | Query official Microsoft documentation to find concepts, tutorials, and code ... | daily-dev, full-stack, minimal |
| **multi-stage-dockerfile** | awesome-copilot | `vendor/awesome-copilot/skills/multi-stage-dockerfile/SKILL.md` | Create optimized multi-stage Dockerfiles for any language or framework | daily-dev, full-stack, minimal |
| **openapi-to-application-code** | awesome-copilot | `vendor/awesome-copilot/skills/openapi-to-application-code/SKILL.md` | Generate a complete, production-ready application from an OpenAPI specification | daily-dev, full-stack, minimal |
| **plantuml-ascii** | awesome-copilot | `vendor/awesome-copilot/skills/plantuml-ascii/SKILL.md` | Generate ASCII art diagrams using PlantUML text mode. | daily-dev, full-stack, minimal |
| **postgresql-optimization** | awesome-copilot | `vendor/awesome-copilot/skills/postgresql-optimization/SKILL.md` | PostgreSQL-specific development assistant focusing on unique PostgreSQL featu... | daily-dev, full-stack, minimal |
| **refactor-plan** | awesome-copilot | `vendor/awesome-copilot/skills/refactor-plan/SKILL.md` | Plan a multi-file refactor with proper sequencing and rollback steps | daily-dev, full-stack, minimal |
| **ruby-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/ruby-mcp-server-generator/SKILL.md` | Generate a complete Model Context Protocol server project in Ruby using the o... | daily-dev, full-stack, minimal |
| **sponsor-finder** | awesome-copilot | `vendor/awesome-copilot/skills/sponsor-finder/SKILL.md` | Find which of a GitHub repository's dependencies are sponsorable via GitHub S... | daily-dev, full-stack, minimal |
| **suggest-awesome-github-copilot-agents** | awesome-copilot | `vendor/awesome-copilot/skills/suggest-awesome-github-copilot-agents/SKILL.md` | Suggest relevant GitHub Copilot Custom Agents files from the awesome-copilot ... | daily-dev, full-stack, minimal |
| **suggest-awesome-github-copilot-instructions** | awesome-copilot | `vendor/awesome-copilot/skills/suggest-awesome-github-copilot-instructions/SKILL.md` | Suggest relevant GitHub Copilot instruction files from the awesome-copilot re... | daily-dev, full-stack, minimal |
| **suggest-awesome-github-copilot-prompts** | awesome-copilot | `vendor/awesome-copilot/skills/suggest-awesome-github-copilot-prompts/SKILL.md` | Suggest relevant GitHub Copilot prompt files from the awesome-copilot reposit... | daily-dev, full-stack, minimal |
| **suggest-awesome-github-copilot-skills** | awesome-copilot | `vendor/awesome-copilot/skills/suggest-awesome-github-copilot-skills/SKILL.md` | Suggest relevant GitHub Copilot skills from the awesome-copilot repository ba... | daily-dev, full-stack, minimal |
| **swift-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/swift-mcp-server-generator/SKILL.md` | Generate a complete Model Context Protocol server project in Swift using the ... | daily-dev, full-stack, minimal |
| **update-llms** | awesome-copilot | `vendor/awesome-copilot/skills/update-llms/SKILL.md` | Update the llms.txt file in the root folder to reflect changes in documentati... | daily-dev, full-stack, minimal |
| **update-markdown-file-index** | awesome-copilot | `vendor/awesome-copilot/skills/update-markdown-file-index/SKILL.md` | Update a markdown file section with an index/table of files from a specified ... | daily-dev, full-stack, minimal |

### Documentation (22)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **doc-coauthoring** | anthropic-skills | `vendor/anthropic-skills/skills/doc-coauthoring/SKILL.md` | Guide users through a structured workflow for co-authoring documentation. | daily-dev, full-stack, minimal |
| **docx** | anthropic-skills | `vendor/anthropic-skills/skills/docx/SKILL.md` | Use this skill whenever the user wants to create, read, edit, or manipulate W... | daily-dev, full-stack, minimal |
| **internal-comms** | anthropic-skills | `vendor/anthropic-skills/skills/internal-comms/SKILL.md` | A set of resources to help me write all kinds of internal communications, usi... | daily-dev, full-stack, minimal |
| **pdf** | anthropic-skills | `vendor/anthropic-skills/skills/pdf/SKILL.md` | Use this skill whenever the user wants to do anything with PDF files. | daily-dev, full-stack, minimal |
| **pptx** | anthropic-skills | `vendor/anthropic-skills/skills/pptx/SKILL.md` | Use this skill any time a .pptx file is involved in any way — as input, outpu... | daily-dev, full-stack, minimal |
| **xlsx** | anthropic-skills | `vendor/anthropic-skills/skills/xlsx/SKILL.md` | Use this skill any time a spreadsheet file is the primary input or output. | daily-dev, full-stack, minimal |
| **architecture-blueprint-generator** | awesome-copilot | `vendor/awesome-copilot/skills/architecture-blueprint-generator/SKILL.md` | Comprehensive project architecture blueprint generator that analyzes codebase... | daily-dev, full-stack, minimal |
| **aspnet-minimal-api-openapi** | awesome-copilot | `vendor/awesome-copilot/skills/aspnet-minimal-api-openapi/SKILL.md` | Create ASP.NET Minimal API endpoints with proper OpenAPI documentation | daily-dev, full-stack, minimal |
| **convert-plaintext-to-md** | awesome-copilot | `vendor/awesome-copilot/skills/convert-plaintext-to-md/SKILL.md` | Convert a text-based document to markdown following instructions from prompt,... | daily-dev, full-stack, minimal |
| **create-oo-component-documentation** | awesome-copilot | `vendor/awesome-copilot/skills/create-oo-component-documentation/SKILL.md` | Create comprehensive, standardized documentation for object-oriented componen... | daily-dev, full-stack, minimal |
| **create-readme** | awesome-copilot | `vendor/awesome-copilot/skills/create-readme/SKILL.md` | Create a README.md file for the project | daily-dev, full-stack, minimal |
| **csharp-docs** | awesome-copilot | `vendor/awesome-copilot/skills/csharp-docs/SKILL.md` | Ensure that C# types are documented with XML comments and follow best practic... | daily-dev, full-stack, minimal |
| **folder-structure-blueprint-generator** | awesome-copilot | `vendor/awesome-copilot/skills/folder-structure-blueprint-generator/SKILL.md` | Comprehensive technology-agnostic prompt for analyzing and documenting projec... | daily-dev, full-stack, minimal |
| **java-docs** | awesome-copilot | `vendor/awesome-copilot/skills/java-docs/SKILL.md` | Ensure that Java types are documented with Javadoc comments and follow best p... | daily-dev, full-stack, minimal |
| **mkdocs-translations** | awesome-copilot | `vendor/awesome-copilot/skills/mkdocs-translations/SKILL.md` | Generate a language translation for a mkdocs documentation stack. | daily-dev, full-stack, minimal |
| **pdftk-server** | awesome-copilot | `vendor/awesome-copilot/skills/pdftk-server/SKILL.md` | Skill for using the command-line tool pdftk (PDFtk Server) for working with P... | daily-dev, full-stack, minimal |
| **project-workflow-analysis-blueprint-generator** | awesome-copilot | `vendor/awesome-copilot/skills/project-workflow-analysis-blueprint-generator/SKILL.md` | Comprehensive technology-agnostic prompt generator for documenting end-to-end... | daily-dev, full-stack, minimal |
| **readme-blueprint-generator** | awesome-copilot | `vendor/awesome-copilot/skills/readme-blueprint-generator/SKILL.md` | Intelligent README.md generation prompt that analyzes project documentation s... | daily-dev, full-stack, minimal |
| **technology-stack-blueprint-generator** | awesome-copilot | `vendor/awesome-copilot/skills/technology-stack-blueprint-generator/SKILL.md` | Comprehensive technology stack blueprint generator that analyzes codebases to... | daily-dev, full-stack, minimal |
| **transloadit-media-processing** | awesome-copilot | `vendor/awesome-copilot/skills/transloadit-media-processing/SKILL.md` | Process media files (video, audio, images, documents) using Transloadit. | daily-dev, full-stack, minimal |
| **update-oo-component-documentation** | awesome-copilot | `vendor/awesome-copilot/skills/update-oo-component-documentation/SKILL.md` | Update existing object-oriented component documentation following industry be... | daily-dev, full-stack, minimal |
| **write-coding-standards-from-file** | awesome-copilot | `vendor/awesome-copilot/skills/write-coding-standards-from-file/SKILL.md` | Write a coding standards document for a project using the coding styles from ... | daily-dev, full-stack, minimal |

### Frontend (47)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **frontend-ui-ux** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/frontend-ui-ux/SKILL.md` | Designer-turned-developer who crafts stunning UI/UX even without design mockups | daily-dev, full-stack |
| **brand-guidelines** | anthropic-skills | `vendor/anthropic-skills/skills/brand-guidelines/SKILL.md` | Applies Anthropic's official brand colors and typography to any sort of artif... | daily-dev, full-stack, minimal |
| **canvas-design** | anthropic-skills | `vendor/anthropic-skills/skills/canvas-design/SKILL.md` | Create beautiful visual art in .png and . | daily-dev, full-stack, minimal |
| **frontend-design** | anthropic-skills | `vendor/anthropic-skills/skills/frontend-design/SKILL.md` | Create distinctive, production-grade frontend interfaces with high design qua... | daily-dev, full-stack, minimal |
| **web-artifacts-builder** | anthropic-skills | `vendor/anthropic-skills/skills/web-artifacts-builder/SKILL.md` | Suite of tools for creating elaborate, multi-component claude. | daily-dev, full-stack, minimal |
| **arch-linux-triage** | awesome-copilot | `vendor/awesome-copilot/skills/arch-linux-triage/SKILL.md` | Triage and resolve Arch Linux issues with pacman, systemd, and rolling-releas... | daily-dev, full-stack, minimal |
| **azure-role-selector** | awesome-copilot | `vendor/awesome-copilot/skills/azure-role-selector/SKILL.md` | When user is asking for guidance for which role to assign to an identity give... | daily-dev, full-stack, minimal |
| **boost-prompt** | awesome-copilot | `vendor/awesome-copilot/skills/boost-prompt/SKILL.md` | Interactive prompt refinement workflow: interrogates scope, deliverables, con... | daily-dev, full-stack, minimal |
| **breakdown-epic-arch** | awesome-copilot | `vendor/awesome-copilot/skills/breakdown-epic-arch/SKILL.md` | Prompt for creating the high-level technical architecture for an Epic, based ... | daily-dev, full-stack, minimal |
| **breakdown-epic-pm** | awesome-copilot | `vendor/awesome-copilot/skills/breakdown-epic-pm/SKILL.md` | Prompt for creating an Epic Product Requirements Document (PRD) for a new epi... | daily-dev, full-stack, minimal |
| **breakdown-feature-prd** | awesome-copilot | `vendor/awesome-copilot/skills/breakdown-feature-prd/SKILL.md` | Prompt for creating Product Requirements Documents (PRDs) for new features, b... | daily-dev, full-stack, minimal |
| **centos-linux-triage** | awesome-copilot | `vendor/awesome-copilot/skills/centos-linux-triage/SKILL.md` | Triage and resolve CentOS issues using RHEL-compatible tooling, SELinux-aware... | daily-dev, full-stack, minimal |
| **copilot-cli-quickstart** | awesome-copilot | `vendor/awesome-copilot/skills/copilot-cli-quickstart/SKILL.md` | Use this skill when someone wants to learn GitHub Copilot CLI from scratch. | daily-dev, full-stack, minimal |
| **copilot-sdk** | awesome-copilot | `vendor/awesome-copilot/skills/copilot-sdk/SKILL.md` | Build agentic applications with GitHub Copilot SDK. | daily-dev, full-stack, minimal |
| **cosmosdb-datamodeling** | awesome-copilot | `vendor/awesome-copilot/skills/cosmosdb-datamodeling/SKILL.md` | Step-by-step guide for capturing key application requirements for NoSQL use-c... | daily-dev, full-stack, minimal |
| **create-implementation-plan** | awesome-copilot | `vendor/awesome-copilot/skills/create-implementation-plan/SKILL.md` | Create a new implementation plan file for new features, refactoring existing ... | daily-dev, full-stack, minimal |
| **create-tldr-page** | awesome-copilot | `vendor/awesome-copilot/skills/create-tldr-page/SKILL.md` | Create a tldr page from documentation URLs and command examples, requiring bo... | daily-dev, full-stack, minimal |
| **create-web-form** | awesome-copilot | `vendor/awesome-copilot/skills/create-web-form/SKILL.md` | Create robust, accessible web forms with best practices for HTML structure, C... | daily-dev, full-stack, minimal |
| **dataverse-python-quickstart** | awesome-copilot | `vendor/awesome-copilot/skills/dataverse-python-quickstart/SKILL.md` | Generate Python SDK setup + CRUD + bulk + paging snippets using official patt... | daily-dev, full-stack, minimal |
| **dataverse-python-usecase-builder** | awesome-copilot | `vendor/awesome-copilot/skills/dataverse-python-usecase-builder/SKILL.md` | Generate complete solutions for specific Dataverse SDK use cases with archite... | daily-dev, full-stack, minimal |
| **debian-linux-triage** | awesome-copilot | `vendor/awesome-copilot/skills/debian-linux-triage/SKILL.md` | Triage and resolve Debian Linux issues with apt, systemd, and AppArmor-aware ... | daily-dev, full-stack, minimal |
| **documentation-writer** | awesome-copilot | `vendor/awesome-copilot/skills/documentation-writer/SKILL.md` | Diátaxis Documentation Expert. An expert technical writer specializing in cre... | daily-dev, full-stack, minimal |
| **dotnet-design-pattern-review** | awesome-copilot | `vendor/awesome-copilot/skills/dotnet-design-pattern-review/SKILL.md` | Review the C#/.NET code for design pattern implementation and suggest improve... | daily-dev, full-stack, minimal |
| **fedora-linux-triage** | awesome-copilot | `vendor/awesome-copilot/skills/fedora-linux-triage/SKILL.md` | Triage and resolve Fedora issues with dnf, systemd, and SELinux-aware guidance. | daily-dev, full-stack, minimal |
| **first-ask** | awesome-copilot | `vendor/awesome-copilot/skills/first-ask/SKILL.md` | Interactive, input-tool powered, task refinement workflow: interrogates scope... | daily-dev, full-stack, minimal |
| **fluentui-blazor** | awesome-copilot | `vendor/awesome-copilot/skills/fluentui-blazor/SKILL.md` | Guide for using the Microsoft Fluent UI Blazor component library (Microsoft. | daily-dev, full-stack, minimal |
| **game-engine** | awesome-copilot | `vendor/awesome-copilot/skills/game-engine/SKILL.md` | Expert skill for building web-based game engines and games using HTML5, Canva... | daily-dev, full-stack, minimal |
| **gen-specs-as-issues** | awesome-copilot | `vendor/awesome-copilot/skills/gen-specs-as-issues/SKILL.md` | This workflow guides you through a systematic approach to identify missing fe... | daily-dev, full-stack, minimal |
| **java-add-graalvm-native-image-support** | awesome-copilot | `vendor/awesome-copilot/skills/java-add-graalvm-native-image-support/SKILL.md` | GraalVM Native Image expert that adds native image support to Java applicatio... | daily-dev, full-stack, minimal |
| **legacy-circuit-mockups** | awesome-copilot | `vendor/awesome-copilot/skills/legacy-circuit-mockups/SKILL.md` | Generate breadboard circuit mockups and visual diagrams using HTML5 Canvas dr... | daily-dev, full-stack, minimal |
| **make-repo-contribution** | awesome-copilot | `vendor/awesome-copilot/skills/make-repo-contribution/SKILL.md` | All changes to code must follow the guidance documented in the repository. | daily-dev, full-stack, minimal |
| **model-recommendation** | awesome-copilot | `vendor/awesome-copilot/skills/model-recommendation/SKILL.md` | Analyze chatmode or prompt files and recommend optimal AI models based on tas... | daily-dev, full-stack, minimal |
| **penpot-uiux-design** | awesome-copilot | `vendor/awesome-copilot/skills/penpot-uiux-design/SKILL.md` | Comprehensive guide for creating professional UI/UX designs in Penpot using M... | daily-dev, full-stack, minimal |
| **power-bi-model-design-review** | awesome-copilot | `vendor/awesome-copilot/skills/power-bi-model-design-review/SKILL.md` | Comprehensive Power BI data model design review prompt for evaluating model a... | daily-dev, full-stack, minimal |
| **power-bi-report-design-consultation** | awesome-copilot | `vendor/awesome-copilot/skills/power-bi-report-design-consultation/SKILL.md` | Power BI report visualization design prompt for creating effective, user-frie... | daily-dev, full-stack, minimal |
| **power-platform-mcp-connector-suite** | awesome-copilot | `vendor/awesome-copilot/skills/power-platform-mcp-connector-suite/SKILL.md` | Generate complete Power Platform custom connector with MCP integration for Co... | daily-dev, full-stack, minimal |
| **powerbi-modeling** | awesome-copilot | `vendor/awesome-copilot/skills/powerbi-modeling/SKILL.md` | Power BI semantic modeling assistant for building optimized data models. | daily-dev, full-stack, minimal |
| **prd** | awesome-copilot | `vendor/awesome-copilot/skills/prd/SKILL.md` | Generate high-quality Product Requirements Documents (PRDs) for software syst... | daily-dev, full-stack, minimal |
| **prompt-builder** | awesome-copilot | `vendor/awesome-copilot/skills/prompt-builder/SKILL.md` | Guide users through creating high-quality GitHub Copilot prompts with proper ... | daily-dev, full-stack, minimal |
| **terraform-azurerm-set-diff-analyzer** | awesome-copilot | `vendor/awesome-copilot/skills/terraform-azurerm-set-diff-analyzer/SKILL.md` | Analyze Terraform plan JSON output for AzureRM Provider to distinguish betwee... | daily-dev, full-stack, minimal |
| **update-implementation-plan** | awesome-copilot | `vendor/awesome-copilot/skills/update-implementation-plan/SKILL.md` | Update an existing implementation plan file with new or update requirements t... | daily-dev, full-stack, minimal |
| **update-specification** | awesome-copilot | `vendor/awesome-copilot/skills/update-specification/SKILL.md` | Update an existing specification file for the solution, optimized for Generat... | daily-dev, full-stack, minimal |
| **vscode-ext-commands** | awesome-copilot | `vendor/awesome-copilot/skills/vscode-ext-commands/SKILL.md` | Guidelines for contributing commands in VS Code extensions. | daily-dev, full-stack, minimal |
| **vscode-ext-localization** | awesome-copilot | `vendor/awesome-copilot/skills/vscode-ext-localization/SKILL.md` | Guidelines for proper localization of VS Code extensions, following VS Code e... | daily-dev, full-stack, minimal |
| **web-design-reviewer** | awesome-copilot | `vendor/awesome-copilot/skills/web-design-reviewer/SKILL.md` | This skill enables visual inspection of websites running locally or remotely ... | daily-dev, full-stack, minimal |
| **winapp-cli** | awesome-copilot | `vendor/awesome-copilot/skills/winapp-cli/SKILL.md` | Windows App Development CLI (winapp) for building, packaging, and deploying W... | daily-dev, full-stack, minimal |
| **workiq-copilot** | awesome-copilot | `vendor/awesome-copilot/skills/workiq-copilot/SKILL.md` | Guides the Copilot CLI on how to use the WorkIQ CLI/MCP server to query Micro... | daily-dev, full-stack, minimal |

### Security (1)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **bigquery-pipeline-audit** | awesome-copilot | `vendor/awesome-copilot/skills/bigquery-pipeline-audit/SKILL.md` | Audits Python + BigQuery pipelines for cost safety, idempotency, and producti... | daily-dev, full-stack, minimal |

### Testing (23)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **finishing-a-development-branch** | superpowers | `vendor/superpowers/skills/finishing-a-development-branch/SKILL.md` | Use when implementation is complete, all tests pass, and you need to decide h... | daily-dev, full-stack, minimal |
| **systematic-debugging** | superpowers | `vendor/superpowers/skills/systematic-debugging/SKILL.md` | Use when encountering any bug, test failure, or unexpected behavior, before p... | daily-dev, full-stack, minimal |
| **test-driven-development** | superpowers | `vendor/superpowers/skills/test-driven-development/SKILL.md` | Use when implementing any feature or bugfix, before writing implementation code | daily-dev, full-stack, minimal |
| **verification-before-completion** | superpowers | `vendor/superpowers/skills/verification-before-completion/SKILL.md` | Use when about to claim work is complete, fixed, or passing, before committin... | daily-dev, full-stack, minimal |
| **webapp-testing** | anthropic-skills | `vendor/anthropic-skills/skills/webapp-testing/SKILL.md` | Toolkit for interacting with and testing local web applications using Playwri... | daily-dev, full-stack, minimal |
| **breakdown-plan** | awesome-copilot | `vendor/awesome-copilot/skills/breakdown-plan/SKILL.md` | Issue Planning and Automation prompt that generates comprehensive project pla... | daily-dev, full-stack, minimal |
| **breakdown-test** | awesome-copilot | `vendor/awesome-copilot/skills/breakdown-test/SKILL.md` | Test Planning and Quality Assurance prompt that generates comprehensive test ... | daily-dev, full-stack, minimal |
| **csharp-mstest** | awesome-copilot | `vendor/awesome-copilot/skills/csharp-mstest/SKILL.md` | Get best practices for MSTest 3.x/4.x unit testing, including modern assertio... | daily-dev, full-stack, minimal |
| **csharp-nunit** | awesome-copilot | `vendor/awesome-copilot/skills/csharp-nunit/SKILL.md` | Get best practices for NUnit unit testing, including data-driven tests | daily-dev, full-stack, minimal |
| **csharp-tunit** | awesome-copilot | `vendor/awesome-copilot/skills/csharp-tunit/SKILL.md` | Get best practices for TUnit unit testing, including data-driven tests | daily-dev, full-stack, minimal |
| **csharp-xunit** | awesome-copilot | `vendor/awesome-copilot/skills/csharp-xunit/SKILL.md` | Get best practices for XUnit unit testing, including data-driven tests | daily-dev, full-stack, minimal |
| **devops-rollout-plan** | awesome-copilot | `vendor/awesome-copilot/skills/devops-rollout-plan/SKILL.md` | Generate comprehensive rollout plans with preflight checks, step-by-step depl... | daily-dev, full-stack, minimal |
| **java-junit** | awesome-copilot | `vendor/awesome-copilot/skills/java-junit/SKILL.md` | Get best practices for JUnit 5 unit testing, including data-driven tests | daily-dev, full-stack, minimal |
| **javascript-typescript-jest** | awesome-copilot | `vendor/awesome-copilot/skills/javascript-typescript-jest/SKILL.md` | Best practices for writing JavaScript/TypeScript tests using Jest, including ... | daily-dev, full-stack, minimal |
| **php-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/php-mcp-server-generator/SKILL.md` | Generate a complete PHP Model Context Protocol server project with tools, res... | daily-dev, full-stack, minimal |
| **playwright-explore-website** | awesome-copilot | `vendor/awesome-copilot/skills/playwright-explore-website/SKILL.md` | Website exploration for testing using Playwright MCP | daily-dev, full-stack, minimal |
| **playwright-generate-test** | awesome-copilot | `vendor/awesome-copilot/skills/playwright-generate-test/SKILL.md` | Generate a Playwright test based on a scenario using Playwright MCP | daily-dev, full-stack, minimal |
| **polyglot-test-agent** | awesome-copilot | `vendor/awesome-copilot/skills/polyglot-test-agent/SKILL.md` | Generates comprehensive, workable unit tests for any programming language usi... | daily-dev, full-stack, minimal |
| **pytest-coverage** | awesome-copilot | `vendor/awesome-copilot/skills/pytest-coverage/SKILL.md` | Run pytest tests with coverage, discover lines missing coverage, and increase... | daily-dev, full-stack, minimal |
| **rust-mcp-server-generator** | awesome-copilot | `vendor/awesome-copilot/skills/rust-mcp-server-generator/SKILL.md` | Generate a complete Rust Model Context Protocol server project with tools, pr... | daily-dev, full-stack, minimal |
| **scoutqa-test** | awesome-copilot | `vendor/awesome-copilot/skills/scoutqa-test/SKILL.md` | This skill should be used when the user asks to "test this website", "run exp... | daily-dev, full-stack, minimal |
| **update-avm-modules-in-bicep** | awesome-copilot | `vendor/awesome-copilot/skills/update-avm-modules-in-bicep/SKILL.md` | Update Azure Verified Modules (AVM) to latest versions in Bicep files. | daily-dev, full-stack, minimal |
| **webapp-testing** | awesome-copilot | `vendor/awesome-copilot/skills/webapp-testing/SKILL.md` | Toolkit for interacting with and testing local web applications using Playwri... | daily-dev, full-stack, minimal |

### Workflow (57)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **brainstorming** | superpowers | `vendor/superpowers/skills/brainstorming/SKILL.md` | You MUST use this before any creative work - creating features, building comp... | daily-dev, full-stack, minimal |
| **dispatching-parallel-agents** | superpowers | `vendor/superpowers/skills/dispatching-parallel-agents/SKILL.md` | Use when facing 2+ independent tasks that can be worked on without shared sta... | daily-dev, full-stack, minimal |
| **executing-plans** | superpowers | `vendor/superpowers/skills/executing-plans/SKILL.md` | Use when you have a written implementation plan to execute in a separate sess... | daily-dev, full-stack, minimal |
| **subagent-driven-development** | superpowers | `vendor/superpowers/skills/subagent-driven-development/SKILL.md` | Use when executing implementation plans with independent tasks in the current... | daily-dev, full-stack, minimal |
| **using-superpowers** | superpowers | `vendor/superpowers/skills/using-superpowers/SKILL.md` | Use when starting any conversation - establishes how to find and use skills, ... | daily-dev, full-stack, minimal |
| **writing-plans** | superpowers | `vendor/superpowers/skills/writing-plans/SKILL.md` | Use when you have a spec or requirements for a multi-step task, before touchi... | daily-dev, full-stack, minimal |
| **writing-skills** | superpowers | `vendor/superpowers/skills/writing-skills/SKILL.md` | Use when creating new skills, editing existing skills, or verifying skills wo... | daily-dev, full-stack, minimal |
| **skill-creator** | anthropic-skills | `vendor/anthropic-skills/skills/skill-creator/SKILL.md` | Create new skills, modify and improve existing skills, and measure skill perf... | daily-dev, full-stack, minimal |
| **openspec-apply-change** | openspec | `.opencode/skills/openspec-apply-change/SKILL.md` | Implement tasks from an OpenSpec change. Use when the user wants to start imp... | daily-dev, full-stack, minimal |
| **openspec-archive-change** | openspec | `.opencode/skills/openspec-archive-change/SKILL.md` | Archive a completed change in the experimental workflow. Use when the user wa... | daily-dev, full-stack, minimal |
| **openspec-explore** | openspec | `.opencode/skills/openspec-explore/SKILL.md` | Enter explore mode - a thinking partner for exploring ideas, investigating pr... | daily-dev, full-stack, minimal |
| **openspec-propose** | openspec | `.opencode/skills/openspec-propose/SKILL.md` | Propose a new change with all artifacts generated in one step. | daily-dev, full-stack, minimal |
| **appinsights-instrumentation** | awesome-copilot | `vendor/awesome-copilot/skills/appinsights-instrumentation/SKILL.md` | Instrument a webapp to send useful telemetry data to Azure App Insights | daily-dev, full-stack, minimal |
| **azure-resource-health-diagnose** | awesome-copilot | `vendor/awesome-copilot/skills/azure-resource-health-diagnose/SKILL.md` | Analyze Azure resource health, diagnose issues from logs and telemetry, and c... | daily-dev, full-stack, minimal |
| **azure-resource-visualizer** | awesome-copilot | `vendor/awesome-copilot/skills/azure-resource-visualizer/SKILL.md` | Analyze Azure resource groups and generate detailed Mermaid architecture diag... | daily-dev, full-stack, minimal |
| **breakdown-feature-implementation** | awesome-copilot | `vendor/awesome-copilot/skills/breakdown-feature-implementation/SKILL.md` | Prompt for creating detailed feature implementation plans, following Epoch mo... | daily-dev, full-stack, minimal |
| **code-exemplars-blueprint-generator** | awesome-copilot | `vendor/awesome-copilot/skills/code-exemplars-blueprint-generator/SKILL.md` | Technology-agnostic prompt generator that creates customizable AI prompts for... | daily-dev, full-stack, minimal |
| **context-map** | awesome-copilot | `vendor/awesome-copilot/skills/context-map/SKILL.md` | Generate a map of all files relevant to a task before making changes | daily-dev, full-stack, minimal |
| **conventional-commit** | awesome-copilot | `vendor/awesome-copilot/skills/conventional-commit/SKILL.md` | Prompt and workflow for generating conventional commit messages using a struc... | daily-dev, full-stack, minimal |
| **copilot-instructions-blueprint-generator** | awesome-copilot | `vendor/awesome-copilot/skills/copilot-instructions-blueprint-generator/SKILL.md` | Technology-agnostic blueprint generator for creating comprehensive copilot-in... | daily-dev, full-stack, minimal |
| **create-spring-boot-java-project** | awesome-copilot | `vendor/awesome-copilot/skills/create-spring-boot-java-project/SKILL.md` | Create Spring Boot Java Project Skeleton | daily-dev, full-stack, minimal |
| **create-spring-boot-kotlin-project** | awesome-copilot | `vendor/awesome-copilot/skills/create-spring-boot-kotlin-project/SKILL.md` | Create Spring Boot Kotlin Project Skeleton | daily-dev, full-stack, minimal |
| **csharp-async** | awesome-copilot | `vendor/awesome-copilot/skills/csharp-async/SKILL.md` | Get best practices for C# async programming | daily-dev, full-stack, minimal |
| **dataverse-python-advanced-patterns** | awesome-copilot | `vendor/awesome-copilot/skills/dataverse-python-advanced-patterns/SKILL.md` | Generate production code for Dataverse SDK using advanced patterns, error han... | daily-dev, full-stack, minimal |
| **dataverse-python-production-code** | awesome-copilot | `vendor/awesome-copilot/skills/dataverse-python-production-code/SKILL.md` | Generate production-ready Python code using Dataverse SDK with error handling... | daily-dev, full-stack, minimal |
| **dotnet-best-practices** | awesome-copilot | `vendor/awesome-copilot/skills/dotnet-best-practices/SKILL.md` | Ensure .NET/C# code meets best practices for the solution/project. | daily-dev, full-stack, minimal |
| **dotnet-upgrade** | awesome-copilot | `vendor/awesome-copilot/skills/dotnet-upgrade/SKILL.md` | Ready-to-use prompts for comprehensive .NET framework upgrade analysis and ex... | daily-dev, full-stack, minimal |
| **editorconfig** | awesome-copilot | `vendor/awesome-copilot/skills/editorconfig/SKILL.md` | Generates a comprehensive and best-practice-oriented .editorconfig file based... | daily-dev, full-stack, minimal |
| **ef-core** | awesome-copilot | `vendor/awesome-copilot/skills/ef-core/SKILL.md` | Get best practices for Entity Framework Core | daily-dev, full-stack, minimal |
| **excalidraw-diagram-generator** | awesome-copilot | `vendor/awesome-copilot/skills/excalidraw-diagram-generator/SKILL.md` | Generate Excalidraw diagrams from natural language descriptions. | daily-dev, full-stack, minimal |
| **fabric-lakehouse** | awesome-copilot | `vendor/awesome-copilot/skills/fabric-lakehouse/SKILL.md` | Use this skill to get context about Fabric Lakehouse and its features for sof... | daily-dev, full-stack, minimal |
| **finnish-humanizer** | awesome-copilot | `vendor/awesome-copilot/skills/finnish-humanizer/SKILL.md` | Detect and remove AI-generated markers from Finnish text, making it sound lik... | daily-dev, full-stack, minimal |
| **image-manipulation-image-magick** | awesome-copilot | `vendor/awesome-copilot/skills/image-manipulation-image-magick/SKILL.md` | Process and manipulate images using ImageMagick. | daily-dev, full-stack, minimal |
| **java-springboot** | awesome-copilot | `vendor/awesome-copilot/skills/java-springboot/SKILL.md` | Get best practices for developing applications with Spring Boot. | daily-dev, full-stack, minimal |
| **kotlin-springboot** | awesome-copilot | `vendor/awesome-copilot/skills/kotlin-springboot/SKILL.md` | Get best practices for developing applications with Spring Boot and Kotlin. | daily-dev, full-stack, minimal |
| **markdown-to-html** | awesome-copilot | `vendor/awesome-copilot/skills/markdown-to-html/SKILL.md` | Convert Markdown files to HTML similar to `marked. | daily-dev, full-stack, minimal |
| **memory-merger** | awesome-copilot | `vendor/awesome-copilot/skills/memory-merger/SKILL.md` | Merges mature lessons from a domain memory file into its instruction file. Sy... | daily-dev, full-stack, minimal |
| **microsoft-code-reference** | awesome-copilot | `vendor/awesome-copilot/skills/microsoft-code-reference/SKILL.md` | Look up Microsoft API references, find working code samples, and verify SDK c... | daily-dev, full-stack, minimal |
| **my-issues** | awesome-copilot | `vendor/awesome-copilot/skills/my-issues/SKILL.md` | List my issues in the current repository | daily-dev, full-stack, minimal |
| **my-pull-requests** | awesome-copilot | `vendor/awesome-copilot/skills/my-pull-requests/SKILL.md` | List my pull requests in the current repository | daily-dev, full-stack, minimal |
| **nano-banana-pro-openrouter** | awesome-copilot | `vendor/awesome-copilot/skills/nano-banana-pro-openrouter/SKILL.md` | Generate or edit images via OpenRouter with the Gemini 3 Pro Image model. Use... | daily-dev, full-stack, minimal |
| **next-intl-add-language** | awesome-copilot | `vendor/awesome-copilot/skills/next-intl-add-language/SKILL.md` | Add new language to a Next.js + next-intl application | daily-dev, full-stack, minimal |
| **nuget-manager** | awesome-copilot | `vendor/awesome-copilot/skills/nuget-manager/SKILL.md` | Manage NuGet packages in .NET projects/solutions. | daily-dev, full-stack, minimal |
| **power-apps-code-app-scaffold** | awesome-copilot | `vendor/awesome-copilot/skills/power-apps-code-app-scaffold/SKILL.md` | Scaffold a complete Power Apps Code App project with PAC CLI setup, SDK integ... | daily-dev, full-stack, minimal |
| **power-bi-dax-optimization** | awesome-copilot | `vendor/awesome-copilot/skills/power-bi-dax-optimization/SKILL.md` | Comprehensive Power BI DAX formula optimization prompt for improving performa... | daily-dev, full-stack, minimal |
| **power-bi-performance-troubleshooting** | awesome-copilot | `vendor/awesome-copilot/skills/power-bi-performance-troubleshooting/SKILL.md` | Systematic Power BI performance troubleshooting prompt for identifying, diagn... | daily-dev, full-stack, minimal |
| **quasi-coder** | awesome-copilot | `vendor/awesome-copilot/skills/quasi-coder/SKILL.md` | Expert 10x engineer skill for interpreting and implementing code from shortha... | daily-dev, full-stack, minimal |
| **remember** | awesome-copilot | `vendor/awesome-copilot/skills/remember/SKILL.md` | Transforms lessons learned into domain-organized memory instructions (global ... | daily-dev, full-stack, minimal |
| **repo-story-time** | awesome-copilot | `vendor/awesome-copilot/skills/repo-story-time/SKILL.md` | Generate a comprehensive repository summary and narrative story from commit h... | daily-dev, full-stack, minimal |
| **shuffle-json-data** | awesome-copilot | `vendor/awesome-copilot/skills/shuffle-json-data/SKILL.md` | Shuffle repetitive JSON objects safely by validating schema consistency befor... | daily-dev, full-stack, minimal |
| **snowflake-semanticview** | awesome-copilot | `vendor/awesome-copilot/skills/snowflake-semanticview/SKILL.md` | Create, alter, and validate Snowflake semantic views using Snowflake CLI (snow). | daily-dev, full-stack, minimal |
| **structured-autonomy-generate** | awesome-copilot | `vendor/awesome-copilot/skills/structured-autonomy-generate/SKILL.md` | Structured Autonomy Implementation Generator Prompt | daily-dev, full-stack, minimal |
| **structured-autonomy-implement** | awesome-copilot | `vendor/awesome-copilot/skills/structured-autonomy-implement/SKILL.md` | Structured Autonomy Implementation Prompt | daily-dev, full-stack, minimal |
| **structured-autonomy-plan** | awesome-copilot | `vendor/awesome-copilot/skills/structured-autonomy-plan/SKILL.md` | Structured Autonomy Planning Prompt | daily-dev, full-stack, minimal |
| **typespec-api-operations** | awesome-copilot | `vendor/awesome-copilot/skills/typespec-api-operations/SKILL.md` | Add GET, POST, PATCH, and DELETE operations to a TypeSpec API plugin with pro... | daily-dev, full-stack, minimal |
| **typespec-create-api-plugin** | awesome-copilot | `vendor/awesome-copilot/skills/typespec-create-api-plugin/SKILL.md` | Generate a TypeSpec API plugin with REST operations, authentication, and Adap... | daily-dev, full-stack, minimal |
| **what-context-needed** | awesome-copilot | `vendor/awesome-copilot/skills/what-context-needed/SKILL.md` | Ask Copilot what files it needs to see before answering a question | daily-dev, full-stack, minimal |

---

## Commands

| Command | Vendor | Path | Description | Profiles |
|---------|--------|------|-------------|----------|
| `/opsx-apply` | openspec | `.opencode/command/opsx-apply.md` | Implement tasks from an OpenSpec change (Experimental) | daily-dev, full-stack, minimal |
| `/opsx-archive` | openspec | `.opencode/command/opsx-archive.md` | Archive a completed change in the experimental workflow | daily-dev, full-stack, minimal |
| `/opsx-explore` | openspec | `.opencode/command/opsx-explore.md` | Enter explore mode - think through ideas, investigate problems, clarify requi... | daily-dev, full-stack, minimal |
| `/opsx-propose` | openspec | `.opencode/command/opsx-propose.md` | Propose a new change - create it and generate all artifacts in one step | daily-dev, full-stack, minimal |

---

## MCPs

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **websearch** | oh-my-opencode | `vendor/oh-my-opencode/src/mcp/websearch.ts` | Web search via Exa/Tavily MCP | daily-dev, full-stack |
| **context7** | oh-my-opencode | `vendor/oh-my-opencode/src/mcp/context7.ts` | Library documentation lookup via Context7 MCP | daily-dev, full-stack, minimal |
| **grep_app** | oh-my-opencode | `vendor/oh-my-opencode/src/mcp/grep-app.ts` | Code search across public repositories via grep.app MCP | daily-dev, full-stack |

---

## Profile Legend

| Profile | Description |
|---------|-------------|
| minimal | Lightweight — fewer agents and MCPs, low concurrency |
| daily-dev | Balanced default for normal development |
| full-stack | Everything enabled, max concurrency |
