# EVAL (EVL) – Experimental Validation Language

EVAL (short for **EVL**) is a **mini programming language and deterministic compiler/interpreter** developed for the **Analysis of Programming Languages (CIT4004)** course at the University of Technology, Jamaica.

The project implements a **full compiler pipeline** using **ANTLR** for lexical and syntactic analysis and compares deterministic execution with **LLM-based interpretation**.

---

## 🎯 Project Objectives

EVAL is designed to:

* Define a **custom programming language**
* Specify a **formal grammar** using ANTLR
* Implement lexical, syntax, and semantic analysis
* Execute programs deterministically
* Compare execution with probabilistic **LLM-based execution**
* Demonstrate characteristics of a **good programming language**

---

## ✨ Language Capabilities

The EVL language supports:

* Variable declarations and assignments
* Arithmetic expressions with correct precedence (PEMDAS/BODMAS)
* Identifiers and literals (integers and strings)
* Output/display statements
* Basic exception handling (`try` / `catch`)
* Deterministic execution with runtime error handling

### Sample EVL Program

```evl
int x = 10;
float y = 20.5;
int sum = x + y;  // Implicit conversion (weak typing)

print("Sum:", sum);

const int newVal = cast(y, int)



int pi = PI
int dayOfWeek = DAYS_IN_WEEK
int hourInDay =  HOURS_IN_DAY
int year = Year

float g = pow(by, number)
int val = sqrt(num)
int = min(y, r)
int max = max(t, w)
float vali = round(y)


try {
    int result = 100 / 0;
} catch {
    print("Error: Division by zero!");
}

```

---

## 🧠 Compiler Design Overview

EVAL follows a **classical compiler architecture**:

1. **Lexical Analysis**

   * Implemented using **ANTLR lexer rules**
2. **Syntax Analysis**

   * Implemented using **ANTLR parser rules**
   * Generates a parse tree
3. **Abstract Syntax Tree (AST) Construction**

   * Parse tree transformed into an AST
4. **Semantic Analysis**

   * Scope and binding checks
   * Symbol table management
   * Type validation
5. **Execution / Interpretation**

   * Deterministic interpreter
6. **LLM-Based Execution (Comparison)**

   * Execution simulated using a Large Language Model
   * Output comparison and analysis

---

## 🛠 Technology Stack

* **Programming Language:** Python 3.12+
* **Parser Generator:** **ANTLR 4**
* **Runtime:** ANTLR Python runtime
* **Environment Management:** `uv`
* **LLM Integration:** OpenAI / Gemini / Azure OpenAI (planned)
* **Version Control / Deployment:** GitHub

---

## 📐 Grammar Specification

* Grammar is defined using **ANTLR (`.g4`) files**
* Includes:

  * Lexer rules (tokens)
  * Parser rules (syntax)
  * Operator precedence and associativity
* Grammar format: **EBNF-style ANTLR grammar**

> The grammar will be documented and included in the project report as required by the course grading scheme.

---

## 📁 Project Structure (Proposed)

> **Note:** Folder structure is not finalized and may evolve.

```text
eval/
├── grammar/
│   └── EVL.g4
├── src/
│   ├── ast/
│   ├── semantic/
│   ├── interpreter/
│   ├── llm/
│   └── main.py
├── examples/
│   └── sample.evl
├── tests/
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.12+
* `uv`
* Java 11+ (required for ANTLR tool)

### Install Dependencies

```bash
uv sync
```

### Generate Lexer & Parser

```bash
antlr4 -Dlanguage=Python3 grammar/EVL.g4 -o src/grammer
```

### Run the Interpreter

```bash
uv run python src/main.py examples/sample.evl
```

---

## 🧪 LLM Execution Comparison (Planned)

EVAL will support:

* Sending EVL source code to an LLM
* Capturing probabilistic execution output
* Comparing it with deterministic interpreter output
* Highlighting differences, ambiguities, and limitations of LLM-based execution

---

## 📊 Course Alignment

This project satisfies core **CIT4004** requirements including:

* Formal grammar specification
* Lexical and syntax analysis using ANTLR
* AST generation
* Semantic analysis
* Deterministic execution
* LLM-based execution comparison
* GitHub/cloud deployment

---

## 👥 Team Information

> Add group member names, ID numbers, and individual contributions here as required by the course guidelines.

---

## 📌 Project Status

🚧 **In Active Development**

Planned milestones:

* Final grammar definition
* Semantic analyzer implementation
* Interpreter completion
* LLM integration
* Documentation and report finalization
