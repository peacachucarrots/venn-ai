import "./ContactQuestion.css";

export default function ContactQuestion({ question, value= "", onChangeText, onNext }) {

    function submit(e) {
        e.preventDefault();
        onNext?.();
    }

    return (
        <form onSubmit={submit} className="contact-field">
            <label>
                <span className="contact-label">{question.prompt}</span>
                <input
                    className="contact-input"
                    type="text"
                    value={value}
                    onChange={(e) => onChangeText?.(e.target.value)}
                />
            </label>
            <button className="contact-next" type="submit">Next</button>
        </form>
    );
}