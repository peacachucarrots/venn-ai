import { useEffect } from "react";

export default function useVisitorCookie() {
    useEffect(() => {
        fetch("/api/visitors", {
            method: "POST",
            credentials: "include",
        })
            .catch(console.error);
    }, []);
}