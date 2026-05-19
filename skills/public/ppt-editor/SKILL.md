# AGENTS.md

> Docker mount paths:
> - Skill root: `/mnt/skills/public/ppt-editor/skills/ppt-editor`
> - User data: `/mnt/user-data`
> - Projects: `/mnt/user-data/projects`

This file serves as the project entry point for general AI agents. Before executing PPT modification tasks, **you MUST first read `/mnt/skills/public/ppt-editor/skills/ppt-editor/SKILL.md`** for the complete workflow and rules.

## Project Overview

PPT Editor is an AI-driven **presentation modification system**. Unlike ppt-master which creates PPTs from scratch, ppt-editor takes **an existing PPTX** and performs user-guided modifications — content changes, design updates, restructuring, restyling.

**Core Pipeline**: `Input PPT → Analyze PPT → Understand Current State → [Modification Loop: Ask → Specify → Modify → Confirm → Repeat] → Export Modified PPTX`

**Key Differences from ppt-master**:
- ppt-master: Create from source documents (8-step pipeline, 3 blocking checkpoints)
- ppt-editor: Modify existing PPTX (iterative loop, each modification is a blocking step)

> ⚠️ **Each modification is a BLOCKING step**: You MUST ask the user for detailed specs about each change, apply it, show the result, and get confirmation before moving to the next modification.

## Execution Requirements

- Before starting a PPT modification task, read `/mnt/skills/public/ppt-editor/skills/ppt-editor/SKILL.md` first
- Always ask the user for details — never assume modification specs
- Each modification must be confirmed before proceeding to the next
- Reference files are in `/mnt/skills/public/ppt-editor/skills/ppt-editor/references/`

## Core Directories

- `/mnt/skills/public/ppt-editor/skills/ppt-editor/SKILL.md` — Main entry point and complete workflow
- `/mnt/skills/public/ppt-editor/skills/ppt-editor/references/` — Reference files
- `/mnt/user-data/projects/` — User project workspace
