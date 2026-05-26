\# OBSIDIAN-8 COMMAND API VERSION SPEC



\## Version

v1.0.0 — Stable Core Command Interface



\---



\## Purpose

This document defines the official versioned contract for all COMMAND layer interactions in OBSIDIAN-8.



All implementations MUST conform to this specification to ensure compatibility, stability, and extensibility.



\---



\## Core Contract



\### Request Format



All commands MUST follow:



```json

{

&#x20; "type": "COMMAND\_TYPE",

&#x20; "payload": {}

}

