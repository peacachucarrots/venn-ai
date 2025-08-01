import { Navigate, useLocation } from "react-router-dom";
import useAuthToken from "@/hooks/useAuthToken.jsx";

export default function RequireAuth({ children }) {
    const { isAuthenticated } = useAuthToken();
    const location = useLocation();

    if (!isAuthenticated) {
        return <Navigate to="/" replace state={{ from: location }} />;
    }

    return children;
}