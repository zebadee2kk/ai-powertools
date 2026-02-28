# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-02-28

### Added
- **Model Intelligence Framework**: Model discovery, benchmarking, tiering, and tier-aware routing (#4)
  - `src/powertools/model_registry/` - Complete model registry system
  - Dynamic model discovery for local and cloud providers
  - Performance benchmarking and intelligent tiering
  - Enhanced router with tier-aware selection
- **Security Module**: Prompt safety helpers to prevent secret leakage
  - `src/powertools/security/prompts.py` - Secret detection and sanitization
  - Pattern-based and ML-based leak prevention

### Changed
- **Branch Strategy**: Reconciled main/master divergence - `master` is now the single default branch
  - Security features from `main` branch merged into `master`
  - `main` branch archived as `backup/main-diverged` for historical reference

## [1.0.0-research] - 2026-02-15

### Added
- **Research Landscape**: Completed comprehensive competitive analysis of 25+ AI projects.
- **Distilled Arsenal**: Mapped 64 modular components into 7 high-impact core modules.
- **Build Strategy**: Defined a 5-stage bootstrapping plan using "Multiplier Components".
- **Memory Architecture**: Full specification for hierarchical, multi-type memory system.
- **whoamiAI Reference App**: Detailed breakdown of Personal AI Mirror (10 sub-components).
- **Core Strategy**: Defined positioning ("The composable toolkit LangChain should have been"), technical decisions, and integration paths.
- **Infrastructure Layers**: Added content engine tools (#46 Blogger, #47 Social Poster) and #54 Local Evolver.
- **Meta-Tools**: Added Auto GitHub Scaffolding and Dev Practices Engine.

### Fixed
- Outdated component count (upgraded from 50 to 64).
- Fragmented research documents (consolidated into `docs/` suite).

## [0.1.0-alpha] - 2026-02-09
- Initial project structure.
- Basic LLM Router prototype.
- Foundation tier design.
