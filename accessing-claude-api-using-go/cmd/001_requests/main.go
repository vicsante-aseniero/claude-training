package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
	"github.com/joho/godotenv"
)

// model is set at the package level so all helper functions can reference it
// without passing it as a parameter. This mirrors the notebook's global `model`
// variable and keeps the helper signatures clean.
//
// Best Practice: Use the SDK's typed constants (e.g. anthropic.ModelClaudeSonnet4_5)
// instead of raw strings. The constants are kept in sync with the SDK release,
// so a Go compiler error will tell you immediately if a model is removed or renamed.
var model = anthropic.ModelClaudeSonnet4_5

// client is the Anthropic API client, initialized in main() after loading the
// API key. Declared at package level so the helper functions can use it.
var client anthropic.Client

// ctx is the root context used for every API call.
// In a production server you would derive per-request contexts with timeouts;
// for a CLI tool a single background context is fine.
var ctx = context.Background()

// ---------------------------------------------------------------------------
// Helper functions — direct Go equivalents of the notebook's
// add_user_message, add_assistant_message, and chat.
// ---------------------------------------------------------------------------

// addUserMessage appends a user-role message to the conversation slice.
//
// Why a pointer-to-slice (*[]anthropic.MessageParam)?
// In Go, slices are value types backed by a pointer/length/capacity header.
// If `append` needs to grow the underlying array it returns a *new* slice
// header. Passing by value would silently discard that new header, so the
// caller's slice would not see the appended element. A pointer-to-slice
// guarantees the caller always sees the updated header — exactly like
// Python's list.append() which mutates in place.
func addUserMessage(messages *[]anthropic.MessageParam, text string) {
	*messages = append(*messages, anthropic.NewUserMessage(anthropic.NewTextBlock(text)))
}

// addAssistantMessage appends an assistant-role message to the conversation.
func addAssistantMessage(messages *[]anthropic.MessageParam, text string) {
	*messages = append(*messages, anthropic.NewAssistantMessage(anthropic.NewTextBlock(text)))
}

// chat sends the current conversation to Claude and returns the text response.
//
// Returning (string, error) instead of calling log.Fatal here follows Go's
// convention of letting the *caller* decide how to handle failures. This makes
// the function reusable and testable — a test can check the error without the
// process exiting.
func chat(messages []anthropic.MessageParam) (string, error) {
	msg, err := client.Messages.New(ctx, anthropic.MessageNewParams{
		Model:     model,
		MaxTokens: 1000,
		Messages:  messages,
	})
	if err != nil {
		return "", fmt.Errorf("chat request failed: %w", err)
	}
	return msg.Content[0].Text, nil
}

// ---------------------------------------------------------------------------
// Granular error handling — Go equivalent of the notebook's
// try/except AuthenticationError, BadRequestError, RateLimitError, …
// ---------------------------------------------------------------------------

// verifyConnection sends a minimal request to verify the API key works.
//
// The Anthropic Go SDK returns *anthropic.Error (an alias for the internal
// apierror.Error) for any HTTP-level failure. We use errors.As to unwrap it
// and then switch on the HTTP StatusCode, mirroring the Python SDK's typed
// exception hierarchy:
//
//	Python                        → Go StatusCode
//	AuthenticationError           → 401
//	BadRequestError               → 400
//	RateLimitError                → 429
//	APIConnectionError            → (err is not *anthropic.Error — network level)
func verifyConnection() error {
	_, err := client.Messages.New(ctx, anthropic.MessageNewParams{
		Model:     model,
		MaxTokens: 1000,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
		},
	})
	if err == nil {
		fmt.Println("Successfully connected to Claude API!")
		return nil
	}

	// Try to unwrap the SDK's API error to inspect the HTTP status code.
	var apiErr *anthropic.Error
	if errors.As(err, &apiErr) {
		switch apiErr.StatusCode {
		case http.StatusUnauthorized: // 401 — AuthenticationError
			fmt.Println("Check your ANTHROPIC_API_KEY.")
		case http.StatusBadRequest: // 400 — BadRequestError
			fmt.Printf("Bad request: %s\n", apiErr.Error())
		case http.StatusTooManyRequests: // 429 — RateLimitError
			fmt.Println("Rate limited. Slow down your request rate.")
		default:
			fmt.Printf("API error (HTTP %d): %s\n", apiErr.StatusCode, apiErr.Error())
		}
		return apiErr
	}

	// If errors.As didn't match, the failure happened before an HTTP response
	// was received — equivalent to Python's APIConnectionError.
	fmt.Println("Connection failed. Check your network.")
	return err
}

func main() {
	// -----------------------------------------------------------------------
	// 1. Load environment variables
	// -----------------------------------------------------------------------
	err := godotenv.Load("../../.env")
	if err != nil {
		fmt.Println("No .env file found or error reading it, continuing with environment variables...")
	}

	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	fmt.Printf("API key loaded: %t\n", apiKey != "")

	// -----------------------------------------------------------------------
	// 2. Create an API client
	// -----------------------------------------------------------------------
	client = anthropic.NewClient(
		option.WithAPIKey(apiKey),
	)

	// -----------------------------------------------------------------------
	// 3. Verify the connection with granular error handling
	// -----------------------------------------------------------------------
	if err := verifyConnection(); err != nil {
		log.Fatalf("Connection verification failed: %v", err)
	}

	// -----------------------------------------------------------------------
	// 4. Multi-turn conversation using helper functions
	// -----------------------------------------------------------------------

	// Make a starting list of messages
	messages := []anthropic.MessageParam{}

	// Add the initial user question
	addUserMessage(&messages, "Define quantum computing in one sentence")

	// Pass the list of messages into chat to get an answer
	fmt.Println("\nSending first request...")
	answer, err := chat(messages)
	if err != nil {
		log.Fatalf("Chat error: %v", err)
	}
	fmt.Printf("Assistant: %s\n", answer)

	// Take the answer and add it as an assistant message into our list
	addAssistantMessage(&messages, answer)

	// Add the user's follow-up question
	addUserMessage(&messages, "Write another sentence")

	// Call chat again with the full conversation history
	fmt.Println("\nSending follow-up request...")
	answer, err = chat(messages)
	if err != nil {
		log.Fatalf("Chat error: %v", err)
	}
	fmt.Printf("Assistant: %s\n", answer)
}
