# Developer Dashboard Guide

## Overview

The Connector Platform includes a comprehensive web-based dashboard for managing connectors, connections, and testing API endpoints. The dashboard provides an intuitive interface for developers to:

- Browse available connectors
- Create and manage connections
- Complete OAuth authorization flows
- Test API endpoints interactively

## Accessing the Dashboard

The dashboard is available at the root URL of your deployed application:

```
http://localhost:5000/
```

## Dashboard Features

### 1. Connectors View

**Path:** `/connectors`

Displays all available connectors in a card-based grid layout.

**Features:**
- View connector name, description, and authentication type
- See connector version information
- Click on any connector to view detailed information
- View available API endpoints for each connector

**Details Modal:**
- Base URL
- Authentication method
- Full list of available endpoints with methods (GET, POST, PUT, DELETE)
- Endpoint descriptions

### 2. Connections View

**Path:** `/connections`

Manage your connector integrations.

**Features:**
- Create new connections with the "+ New Connection" button
- View all existing connections in a grid layout
- See connection status (active, pending, inactive)
- Delete connections
- OAuth authorization flow integration

**Creating a Connection:**
1. Click "+ New Connection"
2. Select a connector from the dropdown
3. Enter a friendly name for your connection
4. Click "Create & Authorize"
5. Complete the OAuth flow in the popup window
6. You'll be redirected back to the dashboard upon success

**Connection Cards Display:**
- Connection name
- Connector type
- Creation date
- Status badge (active/pending)
- Delete button

### 3. API Tester

**Path:** `/test`

Interactive API endpoint testing interface.

**Features:**
- Select from your active connections
- Choose an endpoint from the connector
- Fill in required and optional parameters
- Execute requests with a single click
- View formatted JSON responses
- See detailed error messages

**Using the API Tester:**
1. Select an active connection
2. Choose an endpoint from the dropdown
3. Fill in any required parameters
4. Click "Execute Request"
5. View the response in the formatted JSON viewer

**Response Display:**
- Syntax-highlighted JSON
- Scrollable for large responses
- Copy-friendly formatting

### 4. OAuth Callback Handler

**Path:** `/oauth/callback`

Automated OAuth callback handler that:
- Validates OAuth state parameters (CSRF protection)
- Exchanges authorization codes for access tokens
- Stores tokens securely
- Redirects back to the Connections view
- Displays success/error messages

## Navigation

The sidebar provides easy navigation between all sections:

- **Connectors** - Browse available integrations
- **Connections** - Manage your connections
- **API Tester** - Test endpoints interactively

The active section is highlighted in blue.

## User Interface

### Design Elements

**Color Scheme:**
- Dark sidebar (#1e293b) for navigation
- Light content area (#f8fafc) for readability
- Blue accent (#3b82f6) for primary actions
- Status-specific colors (green for success, yellow for warnings, red for errors)

**Components:**
- **Cards:** Elevated containers with hover effects
- **Badges:** Colored labels for status and categories
- **Buttons:** Clear call-to-action buttons with hover states
- **Modals:** Overlay dialogs for detailed views
- **Forms:** Clean input fields with validation
- **Alerts:** Contextual messages for feedback

### Responsive Design

The dashboard is designed to work on:
- Desktop browsers (optimized for 1280px+ screens)
- Tablet devices
- Responsive grid layouts that adapt to screen size

## Technical Details

### Technology Stack

- **Frontend Framework:** React 19 with TypeScript
- **Build Tool:** Vite 7
- **Routing:** React Router DOM 7
- **HTTP Client:** Axios
- **Styling:** Custom CSS with utility classes

### API Integration

The dashboard communicates with the backend API at `/api/v1` using:
- **Connectors API:** List and get connector details
- **Connections API:** CRUD operations for connections
- **OAuth API:** Authorization flow management
- **Proxy API:** Execute authenticated API requests

### State Management

- React hooks (useState, useEffect) for local component state
- LocalStorage for OAuth flow state management
- No global state management library (intentionally simple)

### Error Handling

The dashboard includes comprehensive error handling:
- API error messages displayed in alerts
- Network error fallbacks
- OAuth flow error recovery
- User-friendly error messages

## Development

### Running the Dashboard Locally

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

The dashboard will be available at `http://localhost:5000`

### Building for Production

```bash
# Build the dashboard
cd frontend
npm run build

# Preview the production build
npm run preview
```

The built files will be in `frontend/dist/`

### Project Structure

```
frontend/
├── src/
│   ├── components/         # React components
│   │   ├── Dashboard.tsx   # Main layout
│   │   ├── Connectors.tsx  # Connectors view
│   │   ├── Connections.tsx # Connections management
│   │   ├── ApiTester.tsx   # API testing interface
│   │   └── OAuthCallback.tsx # OAuth handler
│   ├── api/
│   │   └── client.ts       # API client and types
│   ├── App.tsx             # Root component with routing
│   ├── App.css             # Global styles
│   └── main.tsx            # Entry point
├── vite.config.ts          # Vite configuration
├── tsconfig.json           # TypeScript configuration
└── package.json            # Dependencies
```

## Security Considerations

### OAuth Flow Security

- **State Parameter:** CSRF protection using random state values
- **LocalStorage:** Temporary storage of OAuth state (cleared after completion)
- **Redirect URI Validation:** Backend validates redirect URIs

### API Security

- **No Credentials in Frontend:** API keys and secrets never exposed to client
- **Token Storage:** OAuth tokens stored on backend, not in browser
- **HTTPS Required:** Use HTTPS in production

## Best Practices

### For End Users

1. **Use Descriptive Names:** Name your connections clearly (e.g., "My Gmail Account")
2. **Test Before Using:** Use the API Tester to verify connections work
3. **Monitor Status:** Check connection status badges regularly
4. **Clean Up:** Delete unused connections

### For Developers

1. **Error Handling:** Always wrap API calls in try-catch blocks
2. **Loading States:** Show loading indicators for async operations
3. **User Feedback:** Display success and error messages
4. **Type Safety:** Use TypeScript interfaces for API responses

## Troubleshooting

### Connection Won't Authorize

- Verify OAuth credentials are configured in backend environment variables
- Check that redirect URI matches your application URL
- Ensure the browser allows popups

### API Calls Failing

- Check that the backend server is running
- Verify network connectivity
- Check browser console for detailed error messages
- Ensure connection status is "active"

### Dashboard Not Loading

- Clear browser cache
- Check that frontend server is running on port 5000
- Verify backend API is accessible
- Check browser console for errors

## Future Enhancements

Potential features for future versions:

- Activity logs and audit trails
- Usage analytics and dashboards
- Bulk connection management
- Connection sharing between users
- Custom endpoint builders
- Request/response history
- API documentation browser
- Dark mode toggle
