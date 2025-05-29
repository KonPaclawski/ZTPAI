import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { handleAuthError } from "../utils/auth";


const Settings = () => {
  const userRole = localStorage.getItem("userRole");
  const [usernameToDelete, setUsernameToDelete] = useState("");
  const [message, setMessage] = useState("");
  const [messageColor, setMessageColor] = useState("red");
  const navigate = useNavigate();

  const handleDeleteUser = async () => {
  if (!usernameToDelete.trim()) {
    setMessage("⚠️ Wprowadź nazwę użytkownika.");
    setMessageColor("red");
    return;
  }

  const confirmDelete = window.confirm(
    `Na pewno chcesz usunąć użytkownika "${usernameToDelete}"?`
  );
  if (!confirmDelete) return;

  try {
    await axios.delete(
      `http://localhost:8000/api/admin/delete-user/${usernameToDelete}/`,
      {
        withCredentials: true,
      }
    );
    setMessage(`✅ Użytkownik "${usernameToDelete}" został usunięty.`);
    setMessageColor("green");
    setUsernameToDelete("");
  } catch (error) {
    if (error.response?.status === 404) {
      setMessage("❌ Użytkownik nie został znaleziony.");
    } else if (error.response?.status === 403) {
      setMessage("⛔ Brak uprawnień do wykonania tej operacji.");
    } else if (error.response?.status === 401) {
      await handleAuthError(
      () => handleDeleteUser(),
      () => {
        setMessage("🔒 Sesja wygasła. Zaloguj się ponownie.");
        navigate("/login");
      }
    );
    } else {
      setMessage("⚠️ Wystąpił błąd podczas usuwania użytkownika.");
    }
    setMessageColor("red");
  }
};


  const styles = {
    container: {
      maxWidth: "480px",
      margin: "2rem auto",
      padding: "2rem",
      boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
      borderRadius: "10px",
      backgroundColor: "#fff",
    },
    heading: {
      marginBottom: "1.5rem",
      color: "#4F6CCB",
      textAlign: "center",
    },
    label: {
      display: "block",
      marginBottom: "0.5rem",
      fontWeight: "600",
      color: "#333",
    },
    input: {
      width: "100%",
      padding: "0.5rem",
      borderRadius: "6px",
      border: "1px solid #ccc",
      fontSize: "1rem",
      marginBottom: "1rem",
      boxSizing: "border-box",
    },
    button: {
      backgroundColor: "#cc0000",
      color: "#fff",
      padding: "0.6rem 1.2rem",
      border: "none",
      borderRadius: "6px",
      cursor: "pointer",
      fontWeight: "600",
      fontSize: "1rem",
      width: "100%",
      transition: "background-color 0.3s ease",
    },
    buttonHover: {
      backgroundColor: "#a30000",
    },
    message: {
      marginTop: "1rem",
      fontWeight: "600",
      textAlign: "center",
    },
    logoutBtn: {
      marginTop: "2rem",
      display: "block",
      width: "100%",
      backgroundColor: "#4F6CCB",
      color: "white",
      border: "none",
      padding: "0.6rem",
      borderRadius: "6px",
      fontWeight: "600",
      cursor: "pointer",
      textAlign: "center",
      textDecoration: "none",
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Ustawienia konta</h1>

      {userRole === "admin" ? (
        <>
          <h2 style={{ ...styles.heading, fontSize: "1.25rem" }}>
            Panel administratora
          </h2>

          <label style={styles.label} htmlFor="usernameToDelete">
            Nazwa użytkownika do usunięcia:
          </label>
          <input
            id="usernameToDelete"
            type="text"
            value={usernameToDelete}
            onChange={(e) => setUsernameToDelete(e.target.value)}
            placeholder="np. jan.kowalski"
            style={styles.input}
          />
          <button
            style={styles.button}
            onClick={handleDeleteUser}
            onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#a30000")}
            onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#cc0000")}
          >
            Usuń konto użytkownika
          </button>
          {message && (
            <p style={{ ...styles.message, color: messageColor }}>{message}</p>
          )}
        </>
      ) : (
        <p style={{ textAlign: "center", color: "#cc0000", fontWeight: "600" }}>
          Nie masz uprawnień administratora, aby usuwać konta.
        </p>
      )}

      <button
        style={styles.logoutBtn}
        onClick={() => {
          navigate("/dashboard");
        }}
      >
        Powrót
      </button>
    </div>
  );
};

export default Settings;
