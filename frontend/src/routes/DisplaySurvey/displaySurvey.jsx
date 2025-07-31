import { useEffect, useState, useMemo } from 'react';
import { useNavigate, useParams } from "react-router-dom";

import ProgressBar from '@/components/Survey/ProgressBar/progressBar.jsx'
import { LoadingWithText } from '@/components/Loading/index.jsx'
import MCQuestion from '@/components/Survey/MCQuestion/MCQuestion.jsx'
import MatrixQuestion from '@/components/Survey/MatrixQuestion/MatrixQuestion.jsx'
import ContactQuestion from '@/components/Survey/ContactQuestion/ContactQuestion.jsx'
import './DisplaySurvey.css';

export default function DisplaySurvey({ surveyId: propSurveyId }) {
    const { id: routeSurveyId } = useParams();
    const surveyId = propSurveyId || routeSurveyId;
    const navigate = useNavigate();

    const [survey, setSurvey] = useState(null);
    const [versionId, setVersionId] = useState(null);
    const [pageIndex, setPageIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [submitted, setSubmitted] = useState(false);

    useEffect(() => {
        if (!surveyId) return;
        fetch(`/api/surveys/${surveyId}`, {
            credentials: "include"
        })
            .then(r => r.json())
            .then(data => {
                setSurvey(data);
                setVersionId(data.survey_version_id);
            })
            .catch(console.error);
    }, [surveyId]);

    const pages = useMemo(() => {
        if (!survey) return [];

        const out = [];
        let contactBuf = [];

        const flush = () => {
            if (contactBuf.length) {
                out.push({ type: "contact", questions: contactBuf });
                contactBuf = [];
            }
        };

        survey.questions.forEach(q => {
            if (q.question_type === "contact") {
                contactBuf.push(q);
            } else {
                flush();
                out.push({ type: q.question_type, question: q });
            }
        });
        flush();
        return out;
    }, [survey]);

    useEffect(() => {
        if (!survey || submitted || pageIndex < pages.length) return;
        setSubmitted(true);

        fetch("/api/responses/create-response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                survey_version_id: versionId,
                answers: Object.entries(answers).map(([qid, val]) => (
                    typeof val === "object"
                    ? { question_id: qid, text: val.text }
                    : { question_id: qid, option_id: val }
                ))
            })
        })
            .then(r => r.json())
            .then(json => {
                navigate(`/results/${json.response_id}`, {
                    state: { analysis: json.analysis }
                });
            })
            .catch(console.error);
    }, [survey, submitted, pageIndex, pages.length, versionId, answers, navigate]);

    if (!survey)
        return <LoadingWithText text="Loading survey..." size={50} />;

    if (pageIndex >= pages.length)
        return <LoadingWithText text="Analyzing answers..." size={50} />;

    const nextQuestion = () => setPageIndex(i => i + 1);
    const setAns = (qid, val) => setAnswers(a => ({ ...a, [qid]: val }));

    const page = pages[pageIndex];

    return (
        <div className="survey-container">
            <h1 className="survey-name">Welcome to the {survey.name} Survey.</h1>
            <p className="survey-description">{survey.description}</p>
            <ProgressBar
                currentValue={pageIndex}
                maxValue={pages.length}
            />

            {page.type === "mcq" && (
                <MCQuestion
                    question={page.question}
                    options={page.question.options}
                    selectedOption={answers[page.question.question_id]}
                    onSelect={(opt) => {
                        setAns(page.question.question_id, opt.option_id);
                        nextQuestion();
                    }}
                />
            )}

            {page.type === "matrix" && (
                <MatrixQuestion
                    question={page.question}
                    rows={survey.questions.filter(q => q.question_type === "matrix")}
                    options={page.question.options}
                    answers={answers}
                    onChange={(qid, oid) => {
                        const first = !answers[qid];
                        setAns(qid, oid);
                        if (first) nextQuestion();
                    }}
                />
            )}

            {page.type === "contact" && (
                <ContactQuestion
                    questions={page.questions}
                    answers={answers}
                    onChangeText={(qid, txt) => setAns(qid, txt)}
                    onNext={nextQuestion}
                />
            )}
        </div>
    );
}