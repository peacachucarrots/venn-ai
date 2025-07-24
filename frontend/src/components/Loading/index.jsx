import "./Loading.css"

export default function Loading({ size = 40 }) {
    return <div className="spinner" style={{ width: size, height: size }} />;
}

export function LoadingWithText({ text = "Loading...", size = 40 }) {
    return (
        <div className="loading-container">
            <div className="spinner" style={{ width: size, height: size }} />
            <span className="loading-text">{text}</span>
        </div>
    );
}