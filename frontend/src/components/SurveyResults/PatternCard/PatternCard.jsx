import "./PatternCard.css";

export default function PatternCard({ title, summary, areas, insight, risk, pathway }) {
    return (
        <div className="pattern-card">
            {title && <h3>{title}</h3>}
            {summary && <p>{summary}</p>}

            {areas && (
                <p><strong>Areas:</strong> {areas.join(", ")}</p>
            )}
            {insight && <p><strong>Insight:</strong> {insight}</p>}
            {risk && <p><strong>Risk:</strong> {risk}</p>}
            {pathway && <p><strong>Pathway:</strong> {pathway}</p>}
        </div>
    );
}