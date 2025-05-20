import React, { useState } from "react";
import axios from "axios";
import "./Register.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCreditCard } from '@fortawesome/free-solid-svg-icons';
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/api/register/", { name, email, password });

      alert("Rejestracja zakończone sukcesem!");
    } catch (error) {
      console.error("Registration error:", error.response?.data || error.message);
      alert(`Rejestracja nie powiodła się: ${error.response?.data?.error || "Błąd nieznany"}`);
    }
  };

  return (
    <>
      <div className="register-header">
        <h1>SmartFlow</h1>
        <FontAwesomeIcon icon={faCreditCard} style={{ color: '#4f6ccb' }} size="5x" />
      </div>
      <div className="register-container">
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Name" onChange={(e) => setName(e.target.value)} required />
          <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} required />
          <button type="submit">Rejestracja</button>
        </form>
        <p><a href="/login">Zaloguj się</a></p>
      </div>
    </>
  );
};

export default Register;
