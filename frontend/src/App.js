import './App.css';
import Home from './component/Home';
import MatchingPage from './component/MatchingPage';
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";


function App() {
  return (
    <div className="" >
      <Router>
        <Routes>
        <Route exact path="/" element={<Home/>}/>
        <Route exact path="/matchingpage" element={<MatchingPage/>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
