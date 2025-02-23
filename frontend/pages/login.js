import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Login() {
  const [loginResponse, setLoginResponse] = useState(null);
  const [error, setError] = useState('');

  // This callback is triggered when Google returns a response after a successful sign-in.
  const handleCredentialResponse = async (response) => {
    const googleToken = response.credential; // ID token returned by Google

    try {
      const res = await fetch('http://localhost:8080/user/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ google_token: googleToken })
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Login failed');
        return;
      }

      const data = await res.json();
      setLoginResponse(data);
    } catch (err) {
      console.error(err);
      setError('An error occurred. Please try again.');
    }
  };

  useEffect(() => {
    if (typeof window !== 'undefined' && window.google) {
      window.google.accounts.id.initialize({
        client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || 'YOUR_GOOGLE_CLIENT_ID',
        callback: handleCredentialResponse,
      });
      window.google.accounts.id.renderButton(
        document.getElementById("google-signin"),
        { theme: "outline", size: "large" }
      );
    }
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '2rem' }}>
      <Head>
        <script src="https://accounts.google.com/gsi/client" async defer></script>
      </Head>
      
      <h1>Login with Google</h1>
      {/* The button will be rendered into this div */}
      <div id="google-signin"></div>
      
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loginResponse && (
        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <p>Access Token: {loginResponse.access_token}</p>
          <p>Token Type: {loginResponse.token_type}</p>
        </div>
      )}
    </div>
  );
} 