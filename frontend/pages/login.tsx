import { useState, useEffect } from 'react';
import { GoogleAuthProvider, getAuth, signInWithPopup } from "firebase/auth";
import { useAuthToken } from "./auth.service";
import { AuthFlowLayout } from "./auth-flow";
import { IconBrandGoogle } from "@tabler/icons-react";

export const GoogleButton = () => {
    const { setToken } = useAuthToken();
    const [active, setActive] = useState(false);

    const loginWithProvider = async (provider) => {
        let authProvider = null;
        setActive(true);
        switch (provider) {
            case "google":
                authProvider = new GoogleAuthProvider();
                break;
            default:
                throw "Invalid provider";
        }

        try {
            const { user } = await signInWithPopup(getAuth(), authProvider);

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ google_token: await user.getIdToken() }),
            });
            const data = await res.json();
            if (data) {
                setToken?.(data);
            }
        } catch (er) {
            if (er instanceof Error) {
                if (er.message.indexOf("auth/popup-closed-by-user") >= 0) {
                    return;
                }
            }
        } finally {
            setActive(false);
        }
    };

    return (
        <button
            onClick={() => loginWithProvider("google")}
        >
            <IconBrandGoogle />
            Continue with Google
        </button>
    );
};

export default function Login() {
  const [loginResponse, setLoginResponse] = useState(null);
  const [error, setError] = useState('');

  const { setToken } = useAuthToken();


  return (
    <AuthFlowLayout>
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '2rem' }}>

      <GoogleButton />
      
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loginResponse && (
        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <p>Access Token: {loginResponse.access_token}</p>
          <p>Token Type: {loginResponse.token_type}</p>
        </div>
      )}
    </div>
    </AuthFlowLayout>
  );
} 