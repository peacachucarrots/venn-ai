import DisplaySurvey from "../DisplaySurvey/DisplaySurvey.jsx";
import "./Home.css";

const WELCOME_SURVEY_ID = "810056b0-b8ad-4f6e-ac45-4ba3f864aa2b"

export default function Home() {
    return (
        <>
            <div className="intro-container">
                <h1 className="intro-headline">
                    Tell us a bit about yourself.<br />
                    We're here to listen.
                </h1>
            </div>
            <DisplaySurvey surveyId={WELCOME_SURVEY_ID} />
        </>
    );
}