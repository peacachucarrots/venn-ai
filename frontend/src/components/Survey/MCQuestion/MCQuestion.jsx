import "./MCQuestion.css"

export default function MCQuestion({ question, options, selectedOption, onSelect }) {
    return (
        <div className="mcq-container">
            <h2 className="mcq-prompt">{question.prompt}</h2>
            <ul className="mcq-options">
                {options.map((opt) => (
                <li key={opt.option_id}
                    className="option-item"
                    onClick={() => onSelect(opt)}
                >
                    <input
                        type="radio"
                        name={`q-${question.question_id}`}
                        checked={selectedOption === opt.option_id}
                        onChange={() => onSelect(opt)}
                    />
                    {opt.label || opt.numeric_value}
                </li>
            ))}
            </ul>
        </div>
    );
}