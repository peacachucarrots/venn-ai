import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home           from "./routes/Home/index.jsx";
import DisplaySurvey  from "./routes/DisplaySurvey/DisplaySurvey.jsx";
import SurveyResults  from "./routes/SurveyResults/surveyResults.jsx";

function App() {
    return (
    <BrowserRouter>
      <Routes>
        <Route path="/"               element={<Home />} />
        <Route path="/survey/:id"     element={<DisplaySurvey />} />
        <Route path="/results/:rid"   element={<SurveyResults />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
