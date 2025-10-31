import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Connectors from './components/Connectors';
import Connections from './components/Connections';
import OAuthCallback from './components/OAuthCallback';
import ApiTester from './components/ApiTester';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />}>
          <Route index element={<Navigate to="/connectors" replace />} />
          <Route path="connectors" element={<Connectors />} />
          <Route path="connections" element={<Connections />} />
          <Route path="test" element={<ApiTester />} />
        </Route>
        <Route path="/oauth/callback" element={<OAuthCallback />} />
      </Routes>
    </Router>
  );
}

export default App;
