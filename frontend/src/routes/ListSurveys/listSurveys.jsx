import { useEffect, useState } from 'react';
import { Link } from "react-router-dom";

import "./listSurveys.css";
import LoadingWithText from "@/components/Loading/index.jsx";

export default function ListSurveys() {
    const [list, setList] = useState([]);

    useEffect(() => {
        fetch("/api/surveys/")
            .then(r => r.json())
            .then(setList)
            .catch(console.error);
    }, []);

    if (!list.length) return <LoadingWithText text="Loading Survey List..." />;

    return (
        <div className="list-surveys">
            <h1>Available surveys</h1>
            <ul>
                {list.map((s) => (
                    <li key={s.survey_id}>
                        <Link to={`/survey/${s.survey_id}`}>{s.name}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}