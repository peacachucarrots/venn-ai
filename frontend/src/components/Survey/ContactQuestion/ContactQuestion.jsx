import { useState, useEffect } from "react";
import "./ContactQuestion.css";  // reuse styles

export default function ContactQuestion({ questions, answers, onChangeText, onNext }) {
    // local mirror so typing in one field doesn't lag the others
    const [local, setLocal] = useState(() =>
        Object.fromEntries(questions.map(q => [q.question_id, answers[q.question_id] ?? ""]))
    );

    // keep local state in sync if user goes back
    useEffect(() => {
        setLocal(prev =>
            Object.fromEntries(
                questions.map(q => [q.question_id, answers[q.question_id] ?? prev[q.question_id] ?? ""])
            )
        );
    }, [questions, answers]);

    function handleChange(id, value) {
        setLocal(l => ({ ...l, [id]: value }));
        onChangeText(id, value);
    }

    function submit(e) {
        e.preventDefault();
        // make sure parent has the latest versions
        Object.entries(local).forEach(([id, txt]) => onChangeText(id, txt));
        onNext?.();
    }

    return (
        <form onSubmit={submit} className="contact-field">
            {questions.map(q => (
                <label key={q.question_id}>
                <span className="contact-label">{q.prompt}</span>
                <input
                    className="contact-input"
                    type="text"
                    value={local[q.question_id]}
                    onChange={e => handleChange(q.question_id, e.target.value)}
                />
            </label>
            ))}

            <button className="contact-next" type="submit">
                Next
            </button>
        </form>
  );
}
