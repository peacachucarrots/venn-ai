import { useEffect, useState } from "react";

import useVisitorCookie from "@/hooks/useVisitorCookie.jsx";
import DisplaySurvey from "../DisplaySurvey/DisplaySurvey.jsx";
import "./Home.css";

export default function Home() {
    useVisitorCookie();

    const [welcomeSurveyId, setWelcomeSurveyId] = useState(null);
    useEffect(() => {
        fetch(`/api/surveys/welcome`)
            .then(r => r.json())
            .then(data => setWelcomeSurveyId(data))
            .catch(console.error)
    }, []);

    return (
        <>
            <div className="intro-container">
                <h1 className="intro-headline">
                    Tell us a bit about yourself.<br />
                    We're here to listen.
                </h1>
            </div>
            <DisplaySurvey surveyId={welcomeSurveyId} />
        </>
    );
}