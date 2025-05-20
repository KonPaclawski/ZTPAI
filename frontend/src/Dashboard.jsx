import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Dashboard.css";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  const fetchUsers = async () => {
    const accessToken = localStorage.getItem("accessToken");
    try {
      const response = await axios.get("http://localhost:8000/api/users/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setUsers(response.data.users);
      setError(null);
    } catch (err) {
      if (err.response && err.response.status === 401) {
        const refreshToken = localStorage.getItem("refreshToken");
        if (!refreshToken) {
          alert("Session expired, please login again.");
          navigate("/login");
          return;
        }
        try {
          const refreshResponse = await axios.post(
            "http://localhost:8000/api/token/refresh/",
            { refresh: refreshToken }
          );
          const newAccessToken = refreshResponse.data.access;
          localStorage.setItem("accessToken", newAccessToken);

          const retryResponse = await axios.get(
            "http://localhost:8000/api/users/",
            {
              headers: {
                Authorization: `Bearer ${newAccessToken}`,
              },
            }
          );
          setUsers(retryResponse.data.users);
          setError(null);
        } catch (refreshError) {
          alert("Session expired, please login again.");
          localStorage.clear();
          navigate("/login");
        }
      } else {
        setError("Failed to load users.");
      }
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <>
      <div className="sidebar">
        <h2>SmartFlow</h2>
        <a href="/newBudget">Nowy Budżet</a>
        <a href="/settings">Settings</a>
        <a
          href="#logout"
          onClick={() => {
            localStorage.clear();
            navigate("/login");
          }}
        >
          Logout
        </a>
      </div>
      <div className="main-content">
        <h3>User List</h3>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              {user.name} ({user.email})
            </li>
          ))}
        </ul>
      </div>
    </>
  );
};

export default Dashboard;
