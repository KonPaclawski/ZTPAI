import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import "../css/Budget.css";

const Budget = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [budget, setBudget] = useState(null);
  const [error, setError] = useState(null);
  const [noteInputs, setNoteInputs] = useState({});

  useEffect(() => {
    const fetchBudgetAndNotes = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/budgets/${id}/`, {
          withCredentials: true,
        });
        setBudget(response.data);
        setError(null);

        const notesPromises = response.data.categories.flatMap(category =>
          category.payments.map(payment =>
            axios
              .get(`http://localhost:8000/api/notes/${payment.id}/`, {
                withCredentials: true,
              })
              .then(res => ({ paymentId: payment.id, content: res.data.content }))
              .catch(() => null)
          )
        );

        const notesResults = await Promise.all(notesPromises);
        const initialNotes = {};
        notesResults.forEach(note => {
          if (note) {
            initialNotes[note.paymentId] = note.content;
          }
        });
        setNoteInputs(initialNotes);
      } catch (err) {
        if (err.response?.status === 401) {
          alert("Unauthorized, please login again.");
          navigate("/login");
        } else {
          setError("Failed to load budget details.");
        }
      }
    };

    fetchBudgetAndNotes();
  }, [id, navigate]);

  const handleNoteChange = (paymentId, value) => {
    setNoteInputs(prev => ({
      ...prev,
      [paymentId]: value,
    }));
  };

  const handleNoteSave = async paymentId => {
    const content = noteInputs[paymentId] || "";
    try {
      const existingNote = budget.categories
        .flatMap(cat => cat.payments)
        .find(p => p.id === paymentId)?.note;

      if (existingNote) {
        await axios.put(
          `http://localhost:8000/api/notes/${paymentId}/`,
          { content },
          { withCredentials: true }
        );
      } else {
        await axios.post(
          `http://localhost:8000/api/notes/`,
          { payment_id: paymentId, content },
          { withCredentials: true }
        );
      }

      setBudget(prevBudget => {
        const updatedCategories = prevBudget.categories.map(category => ({
          ...category,
          payments: category.payments.map(payment => {
            if (payment.id === paymentId) {
              return { ...payment, note: { content } };
            }
            return payment;
          }),
        }));
        return { ...prevBudget, categories: updatedCategories };
      });

      setNoteInputs(prev => ({
        ...prev,
        [paymentId]: content,
      }));

      alert("Notatka zapisana.");
    } catch (err) {
      console.error("Błąd przy zapisie notatki:", err);
      alert("Błąd zapisu notatki.");
    }
  };

  const handleDeleteBudget = async () => {
    if (window.confirm("Czy na pewno chcesz usunąć ten budżet?")) {
      try {
        await axios.delete(`http://localhost:8000/api/budgets/${id}/`, {
          withCredentials: true,
        });
        alert("Budżet został usunięty.");
        navigate("/dashboard");
      } catch (err) {
        console.error("Błąd podczas usuwania budżetu:", err);
        alert("Nie udało się usunąć budżetu.");
      }
    }
  };

  if (error) return <div>{error}</div>;
  if (!budget) return <div>Loading...</div>;

  const totalSpent = budget.categories.reduce((sumCategories, category) => {
    const sumPayments = category.payments.reduce((sum, payment) => sum + parseFloat(payment.amount), 0);
    return sumCategories + sumPayments;
  }, 0);

  return (
    <div style={{ display: "flex" }}>
      <aside className="budget-menu_left">
        <div className="budget-logo_left">
          <a>SmartFlow</a>
        </div>
        <div className="budget-menu_options">
          <button
            onClick={handleDeleteBudget}
            style={{
              marginTop: "10px",
              backgroundColor: "#e74c3c",
              color: "white",
              padding: "8px 12px",
              borderRadius: "5px",
              border: "none",
              cursor: "pointer"
            }}
          >
            Usuń budżet
          </button>
          <a onClick={() => navigate("/dashboard")}>Powrót</a>
        </div>
      </aside>

      <div className="budget-container">
        <div className="budget-amount_container">
          <h1>{budget.title}</h1>
          <a>Wykorzystanie budżetu: {totalSpent.toFixed(2)} zł</a>
      
        </div>

        <div className="budget-info_container">
          {budget.categories.map(category => (
            <div key={category.id}>
              <h3>{category.name}</h3>
              <div className="budget-data_container">
                {category.payments.length === 0 ? (
                  <p>No payments</p>
                ) : (
                  category.payments.map(payment => (
                    <div key={payment.id} className="budget-category_container">
                      <div className="budget-top-row">
                        <div className="budget-payments_container">
                          <a>{payment.payment_title} - {payment.amount} zł</a>
                        </div>
                        <div className="budget-date_container">
                          <a>Kolejna Płatność: {payment.date}</a>
                        </div>
                      </div>

                      <div className="budget-note_container">
                        <textarea
                          placeholder="Dodaj notatkę..."
                          value={noteInputs[payment.id] || ""}
                          onChange={(e) => handleNoteChange(payment.id, e.target.value)}
                          rows={3}
                          style={{ maxHeight: "60px" }}
                        />
                        <br />
                        <button onClick={() => handleNoteSave(payment.id)}>Zapisz notatkę</button>
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
