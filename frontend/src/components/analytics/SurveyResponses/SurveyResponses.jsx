import useSurveyResponses from "@/hooks/useSurveyResponses.js";
import "./SurveyResponses.css";
import { LoadingWithText } from "@/components/Loading/Loading.jsx";

export default function SurveyResponses({ surveyId }) {
    const { questions, responses, loading } = useSurveyResponses(surveyId);

    if (loading) return <LoadingWithText text="Loading responses..." />;
    if (!responses.length) return <p className="muted">No responses yet.</p>;

    return (
        <div className="table-wrapper">
            <table className="resp-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Version</th>
                        {questions.map((q) => (
                            <th key={q.id} title={q.revision ? `v${q.revision}` : undefined}>
                                {q.prompt}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                {responses.map((r, i) => (
                    <tr key={i}>
                        <td>{new Date(r.submitted_at).toLocaleString()}</td>
                        <td>{r.name}</td>
                        <td>{r.email}</td>
                        <td>{`v${r.revision}`}</td>
                        {questions.map((q) => (
                            <td key={q.id}>{r.answers[q.id] ?? "-"}</td>
                        ))}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}