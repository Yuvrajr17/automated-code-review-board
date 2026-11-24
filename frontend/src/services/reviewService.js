
const API_BASE_URL = "http://127.0.0.1:8000";

export async function submitReview(reviewData) {
    const response = await fetch(`${API_BASE_URL}/reviews`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(reviewData),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Failed to submit code review."
        );
    }

    return data;
}
