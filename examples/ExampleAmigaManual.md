# ExampleAmiga User Manual

Version: 0.0.0-m2

## Introduction

ExampleAmiga demonstrates the Documentation-Tools M2 source format.

Use the [Command Reference](#command-reference) for command syntax. The literal address `user@example.invalid` exercises AmigaGuide `@` escaping.

## Requirements

- An Amiga system supported by the consumer project.
- Enough memory and storage for that project's requirements.

## Installation

Copy the program to a suitable drawer and follow the project's installation notes.

## Quick Start

Run:

```text
ExampleAmiga
```

Then see the [ARexx Reference](#arexx-reference) for automation.

## Command Reference

### HELP

Displays command help.

Syntax: `HELP [topic]`

Arguments: optional `topic` selects a help topic.

Returns: exit code 0 on success.

Example:

```text
ExampleAmiga HELP commands
```

## API Reference

### ExampleQueryStatus

Query current application state.

Prototype: `LONG ExampleQueryStatus(void)`

Returns: zero for the idle example state.

## ARexx Reference

Port: `EXAMPLEAMIGA`

The port is available while ExampleAmiga is running.

### GETSTATUS

Query current application status.

Command: `GETSTATUS`

Result: `RESULT` contains the textual state.

RC: `0` on success.

Example:

```text
ADDRESS EXAMPLEAMIGA 'GETSTATUS'
SAY RESULT
```

## Troubleshooting

Check the project's requirements and diagnostic output first. Return to the [Introduction](#introduction) after testing this cross-reference.

## License and Support

Refer to the consuming project's repository and license.
