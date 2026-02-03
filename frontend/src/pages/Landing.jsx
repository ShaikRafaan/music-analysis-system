import { useState, useEffect } from 'react'
import '../App.css'
import { api } from '../utils/api'

export const Landing = () => {
    const [serverHello, setServerHello] = useState("");
    useEffect(() => {
        const fetchServer = async () => {
        try {
            const res = await api.get("/");
            setServerHello(res.message);

        } catch (err) {
            console.error(err);
        };
        };

        fetchServer();
    }, []);

    return (
        <>
            <h2>{serverHello}</h2>
            <p>You are logged in</p>
        </>
    )
}
