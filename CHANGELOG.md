# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [0.2.6](https://pypi.org/project/dorans/0.2.6/) - 2026-03-31

### Added

- Camp and structure coordinates from [CDragon](https://www.communitydragon.org/).
- Unbearably fast runtime type-checking with [`beartype`](https://github.com/beartype/beartype).

## [0.2.5](https://pypi.org/project/dorans/0.2.5/) - 2025-05-02

### Added

- Type hints.

### Changed

- Refactored kill events to account for assist XP.

## [0.2.4](https://pypi.org/project/dorans/0.2.4/) - 2025-05-01

### Changed

- Refactored single `from-event` interface into several per-event functions: `from_kill`, `from_assist`, `from_dragon`, `from_elder_dragon`, `from_grub`, `from_rift_herald`, `from_baron` and `from_control_ward`.

## [0.2.3](https://pypi.org/project/dorans/0.2.3/) - 2025-04-30

### Added

- Grub and control ward XP.

## [0.2.2](https://pypi.org/project/dorans/0.2.2/) - 2025-04-25

### Added

- First release.
