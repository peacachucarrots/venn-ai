import { createContext, useCallback, useContext, useState } from "react";

const STORAGE_TOKEN = "adminToken";
const AuthCtx = createContext(null);

export function AuthTokenProvider({ children }) {
    const [token, setToken] = useState(() => localStorage.getItem(STORAGE_TOKEN));

    const login = useCallback(async (candidate) => {
        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token: candidate.trim() })
        });

        if (res.ok) {
            localStorage.setItem(STORAGE_TOKEN, candidate.trim());
            setToken(candidate.trim());
            return true;
        }
        return false;
    }, []);

    const logout = useCallback(() => {
        localStorage.removeItem(STORAGE_TOKEN);
        setToken(null);
    }, []);

    const value = { token, isAuthenticated: Boolean(token), login, logout };
    return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;
}

export default function useAuthToken() {
    return useContext(AuthCtx);
}