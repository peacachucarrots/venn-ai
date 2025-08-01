import "./ActionList.css";

export default function ActionList({ items }) {
    return (
        <ul className="action-list">
            {items.map((txt, i) => (
                <li key={i}>{txt}</li>
            ))}
        </ul>
    );
}