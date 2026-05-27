# Accessing Claude API using Go

This module is a Go (Golang) rewrite of the Python Jupyter Notebooks from `accessing-claude-api`.

In Go, we don't rely heavily on Jupyter Notebooks as they aren't standard for enterprise workflows. Instead, we structure each "notebook" or topic as a standalone executable package inside the `cmd/` directory. This allows you to explore the API using idiomatic Go practices, static typing, and standard error handling.

## Requirements

- Go 1.22+
- An `.env` file in the **repository root** containing your `ANTHROPIC_API_KEY` (or export it as an environment variable).

```env
ANTHROPIC_API_KEY=sk-ant-...
```

## Quick Start

Run each example using standard Go commands from within this directory (`accessing-claude-api-using-go/`):

### 001 Requests

Demonstrates the basics of connecting to the Claude API, handling errors gracefully, and building a multi-turn chat history.

```bash
go run ./cmd/001_requests
```

**What this example covers:**

| Feature | Details |
|---|---|
| Model | `claude-sonnet-4-5` via `anthropic.ModelClaudeSonnet4_5` typed constant |
| Connection check | Verifies the API key before proceeding |
| Granular error handling | Maps HTTP status codes to human-readable messages (401 → bad key, 429 → rate limit, etc.) |
| Helper functions | `addUserMessage`, `addAssistantMessage`, `chat` — Go equivalents of the notebook's Python helpers |
| Multi-turn conversation | Builds a running `[]anthropic.MessageParam` slice across two exchanges |

**Expected output:**

```
API key loaded: true
Successfully connected to Claude API!

Sending first request...
Assistant: Quantum computing is ...

Sending follow-up request...
Assistant: Additionally, ...
```

## Code Structure

```
accessing-claude-api-using-go/
├── cmd/
│   └── 001_requests/
│       └── main.go        # Multi-turn chat with granular error handling
├── go.mod
├── go.sum
└── README.md
```

## Key Design Patterns

### Pointer-to-slice for message accumulation

Go slices are value types — `append` may allocate a new backing array and return a new header. Passing `*[]anthropic.MessageParam` ensures the caller always sees the updated slice:

```go
func addUserMessage(messages *[]anthropic.MessageParam, text string) {
    *messages = append(*messages, anthropic.NewUserMessage(anthropic.NewTextBlock(text)))
}
```

### Typed model constants

Use the SDK's typed constants instead of raw strings to get compile-time validation:

```go
// ✅ Preferred — compile error if model is removed/renamed in a future SDK release
var model = anthropic.ModelClaudeSonnet4_5

// ❌ Avoid — silent runtime failure if the model string is wrong
model := anthropic.Model("claude-sonnet-4-5")
```

### Granular error handling

The SDK returns `*anthropic.Error` for all HTTP-level failures. Switch on `StatusCode` to match specific error types:

```go
var apiErr *anthropic.Error
if errors.As(err, &apiErr) {
    switch apiErr.StatusCode {
    case http.StatusUnauthorized:   // 401 — invalid API key
    case http.StatusBadRequest:     // 400 — malformed request
    case http.StatusTooManyRequests: // 429 — rate limited
    }
}
// If errors.As returns false → network-level failure (no HTTP response)
```

## Why Not Jupyter Notebooks for Go?

While experimental kernels like `gonb` exist for running Go in Jupyter, they circumvent standard Go tooling (`go mod`, `go build`, `go test`) which are fundamental to the ecosystem. Writing standard executable scripts (`main.go` files) is strongly recommended for learning and integrating Go APIs.
