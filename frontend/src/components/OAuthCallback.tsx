import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { oauthApi } from '../api/client';

export default function OAuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'processing' | 'success' | 'error'>('processing');
  const [message, setMessage] = useState('Processing OAuth callback...');

  useEffect(() => {
    handleOAuthCallback();
  }, []);

  const handleOAuthCallback = async () => {
    try {
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const storedState = localStorage.getItem('oauth_state');
      const connectionId = localStorage.getItem('oauth_connection_id');
      const redirectUri = localStorage.getItem('oauth_redirect_uri');

      if (!code || !state || !storedState || !connectionId || !redirectUri) {
        throw new Error('Missing OAuth parameters');
      }

      if (state !== storedState) {
        throw new Error('Invalid state parameter - possible CSRF attack');
      }

      await oauthApi.completeOAuth({
        connection_id: connectionId,
        code,
        state,
        redirect_uri: redirectUri,
      });

      localStorage.removeItem('oauth_state');
      localStorage.removeItem('oauth_connection_id');
      localStorage.removeItem('oauth_redirect_uri');

      setStatus('success');
      setMessage('OAuth authorization successful! Redirecting...');

      setTimeout(() => {
        navigate('/connections');
      }, 2000);
    } catch (err: any) {
      setStatus('error');
      setMessage(err.response?.data?.detail || err.message || 'OAuth authorization failed');
      
      setTimeout(() => {
        navigate('/connections');
      }, 3000);
    }
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      backgroundColor: '#f8fafc'
    }}>
      <div className="card" style={{ maxWidth: '500px', textAlign: 'center' }}>
        {status === 'processing' && (
          <>
            <h2>Processing...</h2>
            <p style={{ marginTop: '1rem', color: '#64748b' }}>{message}</p>
          </>
        )}
        {status === 'success' && (
          <>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✓</div>
            <h2 style={{ color: '#166534' }}>Success!</h2>
            <p style={{ marginTop: '1rem', color: '#64748b' }}>{message}</p>
          </>
        )}
        {status === 'error' && (
          <>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✗</div>
            <h2 style={{ color: '#991b1b' }}>Error</h2>
            <p style={{ marginTop: '1rem', color: '#64748b' }}>{message}</p>
          </>
        )}
      </div>
    </div>
  );
}
