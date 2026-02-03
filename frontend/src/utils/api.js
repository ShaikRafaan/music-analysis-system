const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

async function apiFetch(endpoint, options = {}) {
    const { params, ...fetchOptions } = options;
    let url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    if (params && Object.keys(params).length > 0) {
        const query = new URLSearchParams(
            Object.entries(params).filter(
                ([_, v]) => v !== null && v !== undefined && v !== ""
            )
        ).toString();
        url += `?${query}`;
    }

    const headers = {
        "Content-Type": "application/json",
        ...(fetchOptions.headers || {}),
    };

    try {
        const response = await fetch(url, {
            credentials: "include",
            ...fetchOptions,
            headers 
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Error ${response.status}: ${errText}`);
        }

        const contentType = response.headers.get("content-type") || "";
            if (contentType.includes("application/json")) {
            return await response.json();
        }

        return await response.text();

    } catch (error) {
        console.error(`API fetch failed (${url}):`, error);
        throw error;
    }
}


export const api = {

    get: (endpoint, params) => apiFetch(endpoint, { params }),

    post: (endpoint, data) =>
        apiFetch(endpoint, {
            method: "POST",
            body: JSON.stringify(data),
        }),

    put: (endpoint, data) =>
        apiFetch(endpoint, {
            method: "PUT",
            body: JSON.stringify(data),
        }),
        
    delete: (endpoint) =>
        apiFetch(endpoint, {
            method: "DELETE",
        })

};

export default api;
