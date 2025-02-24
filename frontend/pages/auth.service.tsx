
import { FirebaseApp, initializeApp } from "firebase/app";
import { useRouter } from "next/router";
import { createContext, useContext, useEffect, useState } from "react";

interface ITokenContext {
    token: string | null;
    setToken: (val: ((prevState: string | null) => null) | string | null) => void;
}

const TokenContext = createContext<ITokenContext | null>(null);

export const LOCAL_STORAGE_TOKEN_KEY = "token";
const AUTH_TOKEN_LOADING = "LOADING";

export const useAuthToken = () => {
    const { token, setToken } = useContext(TokenContext) || { token: AUTH_TOKEN_LOADING, setToken: null };
    return { token, setToken };
};

export const useAuthInit = () => {
    const [firebaseApp, setFirebaseApp] = useState<FirebaseApp | null>(null);

    useEffect(() => {
        if (!firebaseApp) {
            setFirebaseApp(
                initializeApp({
                    appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
                    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
                    projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
                    authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
                    storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
                    messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
                })
            );
        }
    }, [firebaseApp]);

    return { setFirebaseApp };
};

export const useAuth = () => {
    const router = useRouter();
    const { token } = useAuthToken();

    useEffect(() => {
        if (token === AUTH_TOKEN_LOADING) {
            console.log("Auth token is loading");
        } else if (!token && (router.pathname != "/login" && router.pathname != "/reset-password" && router.pathname != "/signup")) {
            router.push("/login");
        }
    }, [token, router, router.isReady]);

};

export const useNoAuth = () => {
    const router = useRouter();
    const { token } = useAuthToken();

    useEffect(() => {
        if (token) {
            router.push("/login");
        }
    }, [token]);
};

