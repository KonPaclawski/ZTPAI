import React from "react";
import ReactDOM from "react-dom/client"; 
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import App from "./jsx/App";
import Register from "./jsx/Register";
import Login from "./jsx/Login";
import Dashboard from "./jsx/Dashboard";
import Settings from "./jsx/Settings";
import NewBudget from "./jsx/newBudget";
import Budget from "./jsx/Budget";

const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement); 

root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/newBudget" element={<NewBudget />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/budgets/:id" element={<Budget />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
