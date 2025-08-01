import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import useApi from "@/hooks/useApi.js";
import { LoadingWithText } from "@/components/Loading/Loading.jsx";
import "./Analytics.css";

export default function Analytics() {
    const api = useApi();
    const [overview, setOverview] = useState(null);
    const [surveys, setSurveys] = useState([]);

    useEffect(() => {
        api("/api/analytics/overview").then(setOverview);
        api("/api/analytics/surveys").then(setSurveys);
    }, []);

    if (!overview) return <LoadingWithText text="Loading overview..." />;

    return (
        <div className="analytics-page">
            <section className="card-grid">
                <StatCard label="Total surveys" value={overview.total_surveys} />
                <StatCard label="Active surveys" value={overview.active_surveys} />
                <StatCard label="Total responses" value={overview.total_responses} />
                <StatCard label="Unique visitors" value={overview.unique_visitors} />
            </section>

            <h2>Responses per survey</h2>
            <div className="table-wrapper">
                <table className="survey-table">
                    <thead><tr><th>Survey</th><th>Responses</th></tr></thead>
                    <tbody>
                    {surveys.map((s) => (
                        <tr key={s.survey_id}>
                            <td>{s.name}</td>
                            <td>{s.responses}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>

            <h2>View all responses for a survey</h2>
            <Link to="/analytics/responses">View All Responses</Link>
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
