import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
  const [users, setUsers] = useState([]);
  const [budget, setBudgets ] = useState([]);


  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/users")
      .then(response => setUsers(response.data.users))
      .catch(error => console.error("Error fetching users:", error));
  }, []);
  
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/budgets")
      .then(response => setBudgets(response.data.budgets))
      .catch(error => console.error("Error fetching budgets:", error));
  }
  , []);

  return (
    <div>
      <h1>Lista użytkowników</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name} ({user.email})</li>
        ))}
      </ul>
      <h2>Lista budżetów</h2>
      <ul>
        {budget.map(budget => (
          <li key={budget.id}>{budget.title} {budget.category} {budget.payment_title} {budget.user_id} ({budget.amount})</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
