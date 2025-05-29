import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Dashboard.css";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();
  const [budgets, setBudgets] = useState([]);
  const [error, setError] = useState(null);

  const fetchBudgets = async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      alert("No access token found, please login");
      navigate("/login");
      return;
    }

    try {
      const response = await axios.get("http://localhost:8000/api/budgets/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setBudgets(response.data.budgets);
      setError(null);
    } catch (err) {
      if (err.response?.status === 401) {
        await handleAuthError();
      } else {
        setError("Failed to load budgets.");
      }
    }
  };

  const handleAuthError = async () => {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
      alert("Session expired, please login again.");
      localStorage.clear();
      navigate("/login");
      return;
    }

    try {
      const refreshResponse = await axios.post("http://localhost:8000/api/token/refresh/", {
        refresh: refreshToken,
      });
      localStorage.setItem("accessToken", refreshResponse.data.access);
      await fetchBudgets();
    } catch {
      alert("Session expired, please login again.");
      localStorage.clear();
      navigate("/login");
    }
  };

  useEffect(() => {
    fetchBudgets();
  }, []);

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>SmartFlow</h2>
        </div>
        <nav className="sidebar-links">
          <a href="/newBudget">Nowy Budżet</a>
          <a href="/settings">Settings</a>
          <a
            onClick={() => {
              localStorage.clear();
              navigate("/login");
            }}
          >
            Logout
          </a>
        </nav>
      </aside>

      <main className="main-content">
        <h2>Twoje Budżety</h2>
        {budgets.map((budget) => (
          <button
            key={budget.id}
            className="budget-button"
            onClick={() => navigate(`/budgets/${budget.id}`)}
          >
            {budget.title}
          </button>
        ))}
      </main>

    </div>
  );
};

export default Dashboard;