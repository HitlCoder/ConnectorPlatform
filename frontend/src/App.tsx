import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard.tsx';
import Connectors from './components/Connectors.tsx';
import Connections from './components/Connections.tsx';
import OAuthCallback from './components/OAuthCallback.tsx';
import ApiTester from './components/ApiTester.tsx';
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
