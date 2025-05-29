import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import "./Budget.css";

const Budget = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [budget, setBudget] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/budgets/${id}/`, {
          withCredentials: true, 
        });
        setBudget(response.data);
        setError(null);
      } catch (err) {
        if (err.response?.status === 401) {
          alert("Unauthorized, please login again.");
          navigate("/login");
        } else {
          setError("Failed to load budget details.");
        }
      }
    };

    fetchBudget();
  }, [id, navigate]);

  if (error) return <div>{error}</div>;
  if (!budget) return <div>Loading...</div>;

  const totalSpent = budget.categories.reduce((sumCategories, category) => {
    const sumPayments = category.payments.reduce((sum, payment) => sum + payment.amount, 0);
    return sumCategories + sumPayments;
  }, 0);

  return (
    <div style={{ display: "flex" }}>
      <aside className="budget-menu_left">
        <div className="budget-logo_left">
          <a>BudgetFlow</a>
        </div>
        <div className="budget-menu_options">
          <a onClick={() => navigate("/dashboard")}>Powrót</a>
        </div>
      </aside>

      <div className="budget-container">
        <div className="budget-amount_container">
          <h1>{budget.title}</h1>
          <a>
            Wykorzystanie budżetu: {totalSpent} zł
          </a>
        </div>
        <div className="budget-info_container">
          {budget.categories.map((category) => (
            <div key={category.id}>
              <h3>{category.name}</h3>
              <div className="budget-data_container">
                {category.payments.length === 0 ? (
                  <p>No payments</p>
                ) : (
                  category.payments.map((payment) => (
                    <div key={payment.id} className="budget-category_container">
                      <div className="budget-payments_container">
                        <a>
                          {payment.payment_title} - {payment.amount} zł
                        </a>
                      </div>
                      <div className="budget-date_container">
                        <a>Kolejna Płatność: {payment.date}</a>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Budget;
