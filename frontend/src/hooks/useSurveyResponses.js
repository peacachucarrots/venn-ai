import useApi from "@/hooks/useApi.js";
import { useState, useEffect } from "react";

export default function useSurveyResponses(surveyId) {
    const api = useApi();
    const [data, setData] = useState({ questions: [], responses: [] });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!surveyId) return;
        setLoading(true);
        api(`/api/analytics/survey/${surveyId}/responses`)
            .then(setData)
            .finally(() => setLoading(false));
    }, [surveyId]);

    return { ...data, loading };
}