import { useState } from "react";
import useApi from "@/hooks/useApi.js";
import useSurveyResponses from "@/hooks/useSurveyResponses.js";
import "./SurveyResponses.css";
import { LoadingWithText } from "@/components/Loading/Loading.jsx";

export default function SurveyResponses() {
    const api = useApi();
    const [picked, setPicked] = useState("");
    const [surveys, setSurveys] = useState([]);

    useState(() => {
        api("/api/analytics/surveys").then(setSurveys);
    }, []);

    const { questions, responses, loading } = useSurveyResponses(picked);

    return (
        <div className="resp-page">
            <h1>Survey responses</h1>

            <label>
                Survey:
                <select
                    value={picked}
                    onChange={(e) => setPicked(e.target.value)}
                >
                    <option value="">- choose -</option>
                    {surveys.map((s) => (
                        <option key={s.survey_id} value={s.survey_id}>
                            {s.name}
                        </option>
                    ))}
                </select>
            </label>

            {loading && <LoadingWithText text="Loading..." />}

            {!loading && picked && (
                <div className="table-wrapper">
                    <table className="resp-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Name</th>
                                <th>Email</th>
                                {questions.map((q) => (
                                    <th key={q.id}>{q.prompt}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                        {responses.map((r, i) => (
                            <tr key={i}>
                                <td>{new Date(r.submitted_at).toLocaleString()}</td>
                                <td>{r.name}</td>
                                <td>{r.email}</td>
                                {questions.map((q) => (
                                    <td key={q.id}>
                                        {r.answers[q.id] ?? "-"}
                                    </td>
                                ))}
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}