import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import "./SurveyResults.css";

export default function SurveyResults() {
    const { state } = useLocation();
    const { rid } = useParams();

    const [analysis, setAnalysis] = useState(state?.analysis || null);
    const [promptDebug, setPromptDebug] = useState(state?.promptDebug || null);

    useEffect(() => {
        if (analysis) return;
        fetch(`/api/responses/${rid}`)
            .then((r) => r.json())
            .then((json) => {
                setAnalysis(json.analysis);
                setPromptDebug(json.prompt_debug);
            })
            .catch(console.error);
    }, [rid, analysis]);

    if (!analysis) return <p>Loading results...</p>;

    let parsed = null;
    try {
        parsed = JSON.parse(analysis);
    } catch {
        /* fallback UI */
    }

    return (
        <div>
            <div className="results-container">
                {parsed ? (
                    <>
                        <h2 className="results-title">Your Focus Area</h2>
                        <p className="results-focus">{parsed.focus_area}</p>

                        <h3 className="results-subtitle">Recommended next step</h3>
                        <p className="results-followup">{parsed.followup_survey}</p>
                    </>
                ) : (
                    <>
                        <p>
                            <em>Couldn't parse JDON response.</em>
                        </p>
                        <pre className="results-raw">{analysis}</pre>
                    </>
                )}
            </div>

            {/* DEV-only prompt dump */}
            {promptDebug && (
                <>
                    <h3 className="results-subtitle">
                        Prompt sent to OpenAI (dev)
                    </h3>
                    <pre className="results-raw">{promptDebug}</pre>
                </>
            )}
        </div>
    );
}