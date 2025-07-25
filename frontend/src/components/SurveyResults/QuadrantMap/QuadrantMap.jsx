import "./QuadrantMap.css";

export default function QuadrantMap({ quadrants }) {
    return (
        <section>
            <h2>Quadrant Map</h2>
            <div className="quadrants">
                <Quadrant title="Mirage" items={quadrants.mirage} />
                <Quadrant title="Swamp" items={quadrants.swamp} />
                <Quadrant title="Forge" items={quadrants.forge} />
                <Quadrant title="Radiant" items={quadrants.radiant} />
            </div>
        </section>
    );
}

function Quadrant({ title, items }) {
    if (!items?.length) return null;
    return (
        <div className="quadrant-block">
            <h3>{title}</h3>
            <ul>
                {items.map(d => <li key={d}>{d}</li>)}
            </ul>
        </div>
    );
}