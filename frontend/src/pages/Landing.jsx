import { useState, useEffect } from 'react';
import '../App.css';
import { api } from '../utils/api';

export const Landing = () => {
    const [serverHello, setServerHello] = useState("");
    const [authStatus, setAuthStatus] = useState("Loading...");
    const [loadingLogin, setLoadingLogin] = useState(false);

    // TESTING: Fetch server hello message
    useEffect(() => {
        const fetchServer = async () => {
            try {
                const res = await api.get("/");
                setServerHello(res.message);
            } catch (err) {
                console.error(err);
            }
        };

        fetchServer();
    }, []);

    // TESTING: Check auth status on mount
    useEffect(() => {
        (async () => {
            try {
                const res = await api.get("/auth/status");
                if (res.authenticated) {
                    setAuthStatus("You are logged in");
                } else {
                    setAuthStatus("You are not logged in");
                }
            } catch (err) {
                setAuthStatus("Error getting auth status");
            }
        })();
    }, []);

    // TESTING: Trigger login flow
    const handleLogin = async () => {
        setLoadingLogin(true);
        window.location.href = `${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}/auth/login`;
    };

    return (
        <>
            <h2>{serverHello}</h2>
            <div className="card">
                <p>{authStatus}</p>
                {authStatus === "You are not logged in" && (
                    <button onClick={handleLogin} disabled={loadingLogin}>
                        {loadingLogin ? "Redirecting to Spotify..." : "Login with Spotify"}
                    </button>
                )}
            </div>
        </>
    );
};
