import useAuthToken from "@/hooks/useAuthToken.jsx";

export default function useApi() {
    const { token, logout } = useAuthToken();

    return async function apiFetch(url, opts = {}) {
        const res = await fetch(url, {
            ...opts,
            headers: {
                "Content-Type": "application/json",
                ...(opts.headers || {}),
                ...(token ? { "X-Admin-Token": token } : {})
            }
        });
        if (res.status === 401) logout();
        return res.ok ? res.json() : Promise.reject(res);
    };
}