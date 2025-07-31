import { useEffect } from "react";

export default function useVisitorCookie() {
    useEffect(() => {
        const hasCookie = document.cookie.split("; ").some(c => c.startsWith("visitor_id="));
        if (hasCookie) return;

        fetch("/api/visitors", {
            method: "POST",
            credentials: "include",
        })
            .catch(console.error);
    }, []);
}