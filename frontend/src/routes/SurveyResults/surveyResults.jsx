import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import "./SurveyResults.css";

import RadarScores from "@/components/SurveyResults/RadarScores/RadarScores.jsx";
import QuadrantMap from "@/components/SurveyResults/QuadrantMap/QuadrantMap.jsx";
import PatternCard from "@/components/SurveyResults/PatternCard/PatternCard.jsx";
import ActionList from "@/components/SurveyResults/ActionList/ActionList.jsx";
import Projections from "@/components/SurveyResults/Projections/Projections.jsx";
import Recommendations from "@/components/SurveyResults/Recommendations/Recommendations.jsx";
import BottomLine from "@/components/SurveyResults/BottomLine/BottomLine.jsx";
import { LoadingWithText } from "@/components/Loading";

export default function SurveyResults() {
    const { state } = useLocation();
    const { rid } = useParams();

    const [report, setReport] = useState(state?.analysis || null);

    useEffect(() => {
        if (report || !rid) return;
        fetch(`/api/responses/${rid}`)
            .then((r) => r.json())
            .then((json) => { setReport(json.analysis); })
            .catch(console.error);
    }, [rid, report]);

    if (!report) return <LoadingWithText text="Loading results..." />;

    return (
        <div className="results-page">
            <h1 className="results-heading">Your Venn Diagnostic Report</h1>

            <RadarScores scores={report.scores} size={720} />
            <QuadrantMap quadrants={report.quadrants} />

            <section>
                <h2>Dominant Pattern</h2>
                <PatternCard
                    title={report.dominant_pattern.name}
                    summary={report.dominant_pattern.summary}
                />
            </section>

            <section>
                <h2>This Week's Actions</h2>
                <ActionList items={report.actions_this_week} />
            </section>

            <section>
                <h2>Hidden Patterns</h2>
                {report.hidden_patterns.map((p, index) => (
                    <PatternCard
                        key={index}
                        areas={p.areas}
                        insight={p.insight}
                        risk={p.risk}
                        pathway={p.pathway}
                    />
                ))}
            </section>

            <section>
                <h2>Future Projections</h2>
                <Projections projections={report.future_projections} />
            </section>

            <section>
                <h2>Strategic Recommendations</h2>
                <Recommendations data={report.strategic_recommendations} />
            </section>

            <section>
                <h2>Bottom Line</h2>
                <BottomLine
                scores={report.bottom_line.summary_scores}
                focus={report.bottom_line.next_30_days_focus}
                />
            </section>
        </div>
    );
}