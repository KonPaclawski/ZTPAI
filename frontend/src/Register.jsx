import React, { useState } from "react";
import axios from "axios";
import "./Register.css"

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/api/users/", { name, email, password });
      alert("User registered successfully!");
    } catch (error) {
      console.error("Error response:", error.response?.data || error.message);
      alert(`Registration failed! ${error.response?.data?.detail || "Unknown error"}`);
    }
  };
  

  return (
    <div className="register-container">
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Name" onChange={(e) => setName(e.target.value)} required />
        <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Rejestracja</button>
      </form>
      <p><a href="/login">Zaloguj się</a></p>
    </div>
  );
};

export default Register;
