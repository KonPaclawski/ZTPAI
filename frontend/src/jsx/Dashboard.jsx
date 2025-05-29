import React, { useState, useEffect } from "react";
import axios from "axios";
import "../css/Dashboard.css";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCreditCard } from '@fortawesome/free-solid-svg-icons';
import { handleAuthError, logout } from "../utils/auth";

const Dashboard = () => {
  const navigate = useNavigate();
  const [budgets, setBudgets] = useState([]);
  const [error, setError] = useState(null);

  const fetchBudgets = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/v1/budgets/", {
        withCredentials: true, 
      });
      setBudgets(response.data.budgets);
      setError(null);
    } catch (err) {
      if (err.response?.status === 401) {
        await handleAuthError(fetchBudgets, navigate);
      } else {
        setError("Failed to load budgets.");
      }
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
          <a href="/settings">Ustawienia</a>
          <a onClick={() => logout(navigate)}>Wyloguj</a>
        </nav>
      </aside>

      <main className="main-content">
        <h2>Twoje Budżety</h2>
        {budgets.length === 0 ? (
          <p>Brak budżetów</p>
        ) : (
          budgets.map((budget) => (
            <button
              key={budget.id}
              className="budget-button"
              onClick={() => navigate(`/budgets/${budget.id}`)}
            >
              {budget.title}
            </button>
          ))
        )}
      </main>
    </div>
  );
};

export default Dashboard;
