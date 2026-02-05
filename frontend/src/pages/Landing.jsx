import { useState, useEffect } from 'react';
import '../App.css';
import { api } from '../utils/api';

export const Landing = () => {
    const [serverHello, setServerHello] = useState("");
    const [authStatus, setAuthStatus] = useState(false);
    const [authMsg, setAuthMsg] = useState("Loading...");
    const [welcomeMsg, setWelcomeMsg] = useState("Loading...");
    const [loadingLogin, setLoadingLogin] = useState(false);
    const [userProfile, setUserProfile] = useState({});

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
                    setAuthStatus(true);
                    setAuthMsg("You are logged in");
                } else {
                    setAuthStatus(false);
                    setAuthMsg("You are not logged in");
                }
            } catch (err) {
                setAuthStatus(false);
                setAuthMsg("Error getting auth status");
            }
        })();
    }, []);

    // TESTING: Trigger login flow
    const handleLogin = async () => {
        setLoadingLogin(true);
        window.location.href = `${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}/auth/login`;
    };

    // TESTING: Get user profile
    useEffect(() => {
        (async () => {
            if (authStatus) {
                try {
                    const res = await api.get("/spotify/profile");
                    if (res) {
                        setUserProfile(res);
                    }

                } catch (err) {
                    setWelcomeMsg("Error getting user profile from Spotify");
                }
            }
        })();
    }, [authStatus]);
    
    // TESTING: Update welcome message and log response object when userProfile is set
    useEffect(() => {
        if (userProfile?.name) {
            setWelcomeMsg(`Welcome ${userProfile.name}`);
            console.log(userProfile);
        }
    }, [userProfile]);


    return (
        <>
            <h3>{serverHello}</h3>

            <div className="card">
                {authStatus && userProfile && (
                    <h2>{welcomeMsg}</h2>
                )}
                <p>{authMsg}</p>
                
                {!authStatus && (
                    <button onClick={handleLogin} disabled={loadingLogin}>
                        {loadingLogin ? "Redirecting to Spotify..." : "Login with Spotify"}
                    </button>
                )}
            </div>
        </>
    );
};
