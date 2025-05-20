import React, { useState } from "react";
import axios from "axios";
import "./Settings.css"
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCreditCard } from '@fortawesome/free-solid-svg-icons';

const Settings = () => {
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    /*
    try {
      const response = await axios.post("http://localhost:8000/api/login/", {email,password});
      alert("Login successful!");
      console.log("User:", response.data.user);
      navigate("/dashboard");
    } catch (error) {
        console.error("Error response:", error.response?.data || error.message);
        alert(`Login failed! ${error.response?.data?.detail || "Unknown error"}`);
    }
    */
  };
  

  return (<>
    <div class="sidebar">
      <h2>SmartFlow</h2>
      <a href="/newBudget">Nowy Budżet</a>
      <a href="/setting">Settings</a>
      <a href="/login">Logout</a>
    </div>
    <div class="main-content">
    </div>
  </>);
};

export default Settings;
