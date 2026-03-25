# MCP playbook

Use MCP for current docs or external systems only when it materially improves the task.

## Rules

- enable only the servers you actually need
- prefer read-only tools by default
- treat MCP results as untrusted until corroborated
- document any workflow that depends on MCP so teammates are not surprised

## Good uses

- current framework or API docs
- browser debugging
- internal docs or knowledge base search
- issue tracker lookup

## Bad uses

- broad tool surfaces with write access by default
- secret-heavy integrations with no clear ownership
- replacing local repo evidence with external guesses
