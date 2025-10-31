import { Outlet, NavLink } from 'react-router-dom';

export default function Dashboard() {
  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>Connector Platform</h1>
          <p>Developer Dashboard</p>
        </div>
        <nav className="sidebar-nav">
          <NavLink 
            to="/connectors" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Connectors
          </NavLink>
          <NavLink 
            to="/connections" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Connections
          </NavLink>
          <NavLink 
            to="/test" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            API Tester
          </NavLink>
        </nav>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
