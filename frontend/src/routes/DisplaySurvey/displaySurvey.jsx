import { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";

import ProgressBar from '@/components/ProgressBar/progressBar.jsx'
import { LoadingWithText } from '@/components/Loading/index.jsx'
import MCQuestion from '@/components/QuestionType/MCQuestion/MCQuestion.jsx'
import MatrixQuestion from '@/components/QuestionType/MatrixQuestion/MatrixQuestion.jsx'
import './DisplaySurvey.css';

export default function DisplaySurvey({ surveyId: propSurveyId }) {
    const { id: routeSurveyId } = useParams();
    const surveyId = propSurveyId || routeSurveyId;
    const navigate = useNavigate();
    const [survey, setSurvey] = useState(null);
    const [questionIndex, setQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [analysis, setAnalysis] = useState(null);
    const [promptDebug, setPromptDebug] = useState(null);
    const [submitted, setSubmitted] = useState(false);

    useEffect(() => {
        if (!surveyId) return;
        fetch(`/api/surveys/${surveyId}`)
            .then(r => r.json())
            .then(setSurvey)
            .catch(console.error);
    }, [surveyId]);

    useEffect(() => {
        if (!survey) return;
        const finished = questionIndex >= survey.questions.length;
        if (!finished || submitted) return;

        setSubmitted(true);
        fetch("/api/responses/create-response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                answers: Object.entries(answers).map(([q, o]) => ({
                    question_id: q,
                    option_id: o,
                }))
            })
        })
            .then(r => r.json())
            .then(json => {
                setAnalysis(json.analysis);
                setPromptDebug(json.prompt_debug);
                navigate(`/results/${json.response_id}`, {
                    state: { analysis: json.analysis, promptDebug: json.prompt_debug }
                });
            })
            .catch(console.error);
    }, [survey, questionIndex, submitted, answers, navigate, analysis, promptDebug]);

    if (!survey)
        return <LoadingWithText text="Loading survey..." size={50} />;

    if (questionIndex >= survey.questions.length)
        return <LoadingWithText text="Analyzing answers..." size={50} />;

    function handleMCQSelect(questionId, optionId) {
        setAnswers((prev) => ({ ...prev, [questionId]: optionId }));
        setQuestionIndex(i => i + 1);
    }

    function handleMatrixSelect(questionId, optionId) {
        const firstTime = !Object.prototype.hasOwnProperty.call(answers, questionId);
        setAnswers(prev => ({ ...prev, [questionId]: optionId }));
        if (firstTime) {
            setQuestionIndex(i => i + 1);
        }
    }

    const q = survey.questions[questionIndex];
    const matrixRows = survey.questions.filter(q => q.question_type === "matrix");
    const importanceOptions = matrixRows[0]?.options || [];
    const isMatrixQuestion = q.question_type === "matrix";

    return (
        <div className="survey-container">
            <h1 className="survey-name">Welcome to the {survey.name} Survey.</h1>
            <p className="survey-description">{survey.description}</p>
            <ProgressBar
                currentValue={questionIndex}
                maxValue={survey.questions.length}
            />

            {isMatrixQuestion ? (
                <MatrixQuestion
                    question={q}
                    rows={matrixRows}
                    options={importanceOptions}
                    answers={answers}
                    onChange={handleMatrixSelect}
                />
            ) : (
                <MCQuestion
                    question={q}
                    options={q.options}
                    selectedOption={answers[q.question_id]}
                    onSelect={(opt) =>
                        handleMCQSelect(q.question_id, opt.option_id)
                    }
                />
            )}
        </div>
    );
}