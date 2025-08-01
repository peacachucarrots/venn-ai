import "./Projections.css";

export default function Projections({ projections }) {
    return (
        <div className="projections">
            <p><strong>6 months:</strong> {projections.six_months}</p>
            <p><strong>12 months:</strong> {projections.twelve_months}</p>
        </div>
    );
}