
/**
 * ai_helper.js
 * Handles interaction with the Intelligent Response (AI) backend service.
 */

async function fetchAIResponse(word) {
    try {
        const response = await fetch('/ask_ai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ word: word })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error("Error fetching AI response:", error);
        return { error: "Could not reach AI service." }; // Safe fallback
    }
}
