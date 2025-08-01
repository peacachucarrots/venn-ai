import "./ProgressBar.css"

export default function ProgressBar({currentValue, maxValue}) {
    const percentDone = maxValue > 0
        ? Math.round((currentValue / maxValue) * 100)
        : 0;
    return (
        <div className="progress"
             role="progressbar"
             aria-valuenow={currentValue}
             aria-valuemax={maxValue}>
            <div className="progress__fill" style={{ width:`${percentDone}%` }} />
        </div>
    );
}