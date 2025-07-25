import "./Recommendations.css";

export default function Recommendations({ data }) {
    return (
        <div className="recs-block">
            <RecBlock title="🚨 Immediate" items={data.immediate} />
            <RecBlock title="🔥 Forge Focus" items={data.forge_focus} />
            <RecBlock title="🌟 Leverage" items={data.leverage} />
            <RecBlock title="🌫️ Transformation" items={data.transformation} />
        </div>
    );
}

function RecBlock({ title, items }) {
    if (!items?.length) return null;
    return (
        <div className="rec-block">
            <h3>{title}</h3>
            <ul>
                {items.map((t, index) => <li key={index}>{t}</li>)}
            </ul>
        </div>
    );
}