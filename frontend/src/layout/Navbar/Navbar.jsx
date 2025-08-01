import { Link } from "react-router-dom";
import useAuthToken from "@/hooks/useAuthToken.jsx";
import { useState } from "react";
import Login from "@/components/Login/Login.jsx";
import logo from "@/assets/venn-ai-logo.png";
import "./Navbar.css";

export default function Navbar() {
    const { isAuthenticated, logout } = useAuthToken();
    const [showLogin, setShowLogin] = useState(false);

    return (
        <>
            <nav className="nav-container">
                <Link to="/" className="nav-logo">
                    <img src={logo} alt="Venn-AI Logo" />
                </Link>
                <Link to="/surveys">Surveys</Link>
                {isAuthenticated && <Link to="/analytics">Analytics</Link>}
                {isAuthenticated ? (
                    <button onClick={logout} className="logout-btn">Log out</button>
                ) : (
                    <button onClick={() => setShowLogin(true)}>Log in</button>
                )}
            </nav>

            {showLogin && <Login close={() => setShowLogin(false)} />}
        </>
    );
}