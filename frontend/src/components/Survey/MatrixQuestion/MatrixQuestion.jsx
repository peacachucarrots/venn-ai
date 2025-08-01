import { useEffect } from "react";
import "./MatrixQuestion.css"

export default function MatrixQuestion({
                                           question,
                                           rows,
                                           options,
                                           answers,
                                           onChange
                                       }) {
    const instructions = question.shared_set?.instructions || "";

    return (
        <div className="matrix-container">
            {instructions && (<h2 className="matrix-instructions">{instructions}</h2>)}

            <table className="matrix-table">
                <thead>
                    <tr>
                        <th className="corner-cell"></th>
                        {options.map((opt) => (
                            <th key={opt.option_id}>{opt.label}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row) => (
                        <tr key={row.question_id}>
                            <th className="row-header">{row.prompt}</th>
                            {options.map((opt) => (
                                <td key={opt.option_id}>
                                    <input
                                        type="radio"
                                        name={`q-${row.question_id}`}
                                        value={opt.option_id}
                                        checked={answers[row.question_id] === opt.option_id}
                                        onChange={() => onChange(row.question_id, opt.option_id)}
                                    />
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}