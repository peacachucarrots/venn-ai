import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthTokenProvider } from "@/hooks/useAuthToken.jsx";

import Navbar         from "@/layout/Navbar/Navbar.jsx";
import Footer         from "@/layout/Footer/Footer.jsx";
import Home           from "@/routes/Home/index.jsx";
import RequireAuth    from "@/routes/RequireAuth.jsx";
import Analytics      from "@/routes/Analytics/Home/Analytics.jsx";
import ListSurveys    from "@/routes/ListSurveys/listSurveys.jsx"
import DisplaySurvey  from "@/routes/DisplaySurvey/DisplaySurvey.jsx";
import SurveyResults  from "@/routes/SurveyResults/surveyResults.jsx";
import SurveyResponses from "@/routes/Analytics/SurveyResponses/SurveyResponses.jsx";

function App() {
    return (
        <AuthTokenProvider>
            <BrowserRouter>
                <Navbar />

                <Routes>
                    <Route path="/"               element={<Home />} />
                    <Route path="/analytics"
                           element={<RequireAuth><Analytics /></RequireAuth>} />
                    <Route path="/analytics/responses"
                           element={<RequireAuth><SurveyResponses /></RequireAuth>} />
                    <Route path="/surveys"        element={<ListSurveys />} />
                    <Route path="/survey/:id"     element={<DisplaySurvey />} />
                    <Route path="/results/:rid"   element={<SurveyResults />} />
                </Routes>

                <Footer />
            </BrowserRouter>
        </AuthTokenProvider>
    );
}

export default App;
