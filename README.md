# AI-PROMPT-GENERATOR

<img src="https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true" alt="Project Badge" width="150">

<img src="https://raw.githubusercontent.com/ManfredAabye/AI-PROMPT-GENERATOR/refs/heads/main/UniversalPromptManager.png" alt="Project Badge" width="450">

Desktop prompt generator for structured AI workflows with a JSON-driven category system.

The project currently provides 37 category definitions, multilingual UI support, source code planning workflows, and a dedicated 3D OBJ/MTL prompt category.

Status: Alpha
Languages: German, English, French, Spanish
UI stack: Python, Tkinter, ttkbootstrap

## Main Applications

### UniversalPromptManager

The main desktop application for category-based prompt generation.

Current highlights:

- 37 JSON-based categories in the categories folder
- multilingual UI and localized category labels in German, English, French, and Spanish
- source code prompts with extended framework/runtime coverage including .NET variants
- Sourcecode Planning-Style and Sourcecode Planning-Style Light categories
- planning strategy injection via StrategySelector and ReasoningEngine
- output formatting for different target styles and prompt export workflows
- new 3D-Objekte category for structured OBJ and MTL generation

### RodinPromptGenerator

Separate application entry point for Rodin-specific prompt generation.

## Categories

The repository currently includes these categories:

- 3D Objects
- Account and Login
- Architecture
- Automation / Workflow
- Image Description
- Business Plan
- Data Analysis / SQL
- Privacy and Security
- Documentation
- Email / Communication
- Custom Template
- Nutrition Plan
- Events and Webinars
- Feedback and Suggestions
- Warranty and Repairs
- General / Other Inquiries
- Careers and Job Openings
- AI Art
- Delivery Inquiries
- Marketing
- Partnerships and Collaborations
- Presentations / Pitch Deck
- Press and Media Inquiries
- Product Requirements
- Product Information
- Invoices and Receipts
- Returns and Exchanges
- SEO / Blog / Content
- Social Media
- Source Code
- Source Code Planning Style
- Source Code Planning Style Light
- Technical Issues
- UX / UI Concept
- Contract Changes and Cancellation
- Payment Inquiries
- Order Inquiries

## 3D-Objekte Category

The new 3D category is designed for OBJ and MTL generation with explicit structural guidance.

Included capabilities:

- OBJ + MTL prompt generation with strict file-content-only output rules
- configurable shape, dimensions, mesh quality, material mode, separator mode, and material values
- optional vt and vn output guidance
- stricter geometry validation rules for indices and shape-specific expectations
- preset profiles for Standard, Game-Asset Low-Poly, CAD-Clean, and Multi-Material Demo
- automatic preset-based default switching in the UI

## Sourcecode Planning Features

The planning workflow has been expanded beyond basic source code prompting.

Included capabilities:

- Sourcecode Planning-Style category for deeper structured planning
- Sourcecode Planning-Style Light for a more compact workflow
- task-type presets including Re-Engineering and Rewrite
- localized planning strategies and language-aware strategy injection
- export-oriented formatting for different prompt consumer styles

## Start

Run the applications directly:

```bat
start-universal.bat
start-rodin.bat
```

Or start them with Python:

```bat
python UniversalPromptManager.py
python RodinPromptGenerator.py
```

## Build

Build Windows executables with the included batch files:

```bat
build-universal.bat
build-rodin.bat
```

The universal build currently:

- installs PyInstaller if needed
- builds UniversalPromptManager.exe
- copies upmlanguages.json
- copies the categories folder
- copies icon assets into dist

## Project Structure

Important files and folders:

- UniversalPromptManager.py: main desktop application
- RodinPromptGenerator.py: Rodin-specific generator
- categories/: JSON category definitions
- upmlanguages.json: UI translations and category labels
- app_settings.json: persisted application settings
- strategy_selector.py: planning strategy selection
- reasoning_engine.py: localized strategy loading and prompt injection
- strategies/: planning, reflection, verification, and decomposition templates

## Intended Use

UniversalPromptManager is intended as a practical prompt authoring tool, especially for users who want structured inputs instead of writing prompts from scratch.

Stand: Mai 2026
