import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import useApi from "@/hooks/useApi.js";
import { LoadingWithText } from "@/components/Loading/Loading.jsx";
import "./Analytics.css";
import SurveyResponses from "@/components/analytics/SurveyResponses/SurveyResponses.jsx";

export default function Analytics() {
    const api = useApi();
    const [overview, setOverview] = useState(null);
    const [surveys, setSurveys] = useState([]);
    const [selectedSurvey, setSelectedSurvey] = useState("");

    useEffect(() => {
        api("/api/analytics/overview").then(setOverview);
        api("/api/analytics/surveys").then(setSurveys);
    }, []);

    if (!overview) return <LoadingWithText text="Loading overview..." />;

    return (
        <div className="analytics-page">
            <h1>Overview</h1>
            {overview && (
                <section className="card-grid">
                    <StatCard label="Total surveys" value={overview.total_surveys} />
                    <StatCard label="Total versions" value={overview.total_versions} />
                    <StatCard label="Active surveys" value={overview.active_surveys} />
                    <StatCard label="Total responses" value={overview.total_responses} />
                    <StatCard label="Unique visitors" value={overview.unique_visitors} />
                </section>
            )}

            <section className="responses-section">
                <div className="responses-header">
                    <h2>Responses</h2>
                    <label className="survey-picker">
                        Survey:
                        <select
                            value={selectedSurvey}
                            onChange={(e) => setSelectedSurvey(e.target.value)}
                        >
                            <option value="">- choose -</option>
                            {surveys.map((s) => (
                                <option key={s.survey_id} value={s.survey_id}>
                                    {s.name} ({s.responses_active} active / {s.responses} total)
                                </option>
                            ))}
                        </select>
                    </label>
                </div>

                {selectedSurvey ? (
                    <SurveyResponses surveyId={selectedSurvey} />
                ) : (
                    <p className="muted">Pick a survey to list all responses.</p>
                )}
            </section>
        </div>
    );
}

function StatCard({ label, value }) {
    return (
        <div className="stat-card">
            <span className="stat-value">{value}</span>
            <span className="stat-label">{label}</span>
        </div>
    );
}
