import { useState } from "react";
import useAuthToken from "@/hooks/useAuthToken.jsx";

import "./Login.css";

export default function Login({ close }) {
    const { login } = useAuthToken();
    const [input, setInput] = useState("");

    async function handleSubmit(e){
        e.preventDefault();
        const ok = await login(input);
        if (ok) close();
        else alert("Invalid token");
    }

    return (
        <div className="modal">
            <form className="modal-box" onSubmit={handleSubmit}>
                <h2>Authentication token</h2>
                <input
                    type="password"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                />
                <div className="btn-row">
                    <button type="submit" className="submit">Submit</button>
                    <button type="button" onClick={close} className="cancel">Cancel</button>
                </div>
            </form>
        </div>
    );
}