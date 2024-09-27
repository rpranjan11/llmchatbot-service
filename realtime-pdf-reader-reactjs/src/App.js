import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Home } from './Home';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";

function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
    </Router>
    // <Home />
    // <p>hello</p>
  );
}

export default App;
