import React, { useState } from "react";
import axios from "axios";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCreditCard } from '@fortawesome/free-solid-svg-icons';

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await axios.post("http://localhost:8000/api/login/", {
      email,
      password,
    });
    console.log("Login response:", response.data);

    const { access, refresh, user } = response.data;

    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
    localStorage.setItem("userId", user.id);
    localStorage.setItem("userEmail", user.email);
    localStorage.setItem("userRole", user.role);
    localStorage.setItem("userName", user.name);

    console.log("accessToken after login:", localStorage.getItem("accessToken"));
    console.log("refreshToken after login:", localStorage.getItem("refreshToken"));

    alert("Zalogowano pomyślnie!");
    navigate("/dashboard");
  } catch (error) {
    console.error("Login error:", error.response?.data || error.message);
    alert(`Login failed! ${error.response?.data?.error || "Unknown error"}`);
  }
};


  return (
    <>
      <div className="login-header">
        <h1>SmartFlow</h1>
        <FontAwesomeIcon icon={faCreditCard} style={{ color: '#4f6ccb' }} size="5x" />
      </div>

      <div className="login-container">
        <form onSubmit={handleSubmit}>
          <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} required />
          <button type="submit">Zaloguj się</button>
        </form>
        <p><a href="/register">Utwórz Konto</a></p>
      </div>
    </>
  );
};

export default Login;
