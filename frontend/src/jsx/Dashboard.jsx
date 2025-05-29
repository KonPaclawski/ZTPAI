import React, { useState, useEffect } from "react";
import axios from "axios";
import "../css/Dashboard.css";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCreditCard } from '@fortawesome/free-solid-svg-icons';

const Dashboard = () => {
  const navigate = useNavigate();
  const [budgets, setBudgets] = useState([]);
  const [error, setError] = useState(null);

  const fetchBudgets = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/budgets/", {
        withCredentials: true, 
      });
      setBudgets(response.data.budgets);
      setError(null);
    } catch (err) {
      if (err.response?.status === 401) {
        alert("Unauthorized, please login again.");
        navigate("/login");
      } else {
        setError("Failed to load budgets.");
      }
    }
  };

  const handleAuthError = async () => {
    try {
      await axios.post("http://localhost:8000/api/token/refresh/", {}, {
        withCredentials: true,
      });
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
          <FontAwesomeIcon icon={faCreditCard} style={{ color: '#4f6ccb' }} size="5x" />
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
