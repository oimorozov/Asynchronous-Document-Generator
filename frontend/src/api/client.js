const API_URL = "http://localhost:8000/api/v1";

export async function request(endpoint) {
    const config = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }
    try {
        const response = await fetch(`${API_URL}/${endpoint}`, config);
        if (!response.ok) {
            throw new Error()
        }
        return await response.json();
    } catch (e) {
        throw e;
    }
}