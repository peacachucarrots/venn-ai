import "./BottomLine.css";

export default function BottomLine({ scores, focus }) {
    return (
        <section className="bottom-line">
            <p>
                Mirage: {scores.mirage} | Swamp: {scores.swamp} | Forge: {scores.forge} | Radiant: {scores.radiant}
            </p>
            <p><strong>Next 30 days focus:</strong> {focus}</p>
        </section>
    );
}