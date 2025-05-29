import React, { useState } from "react";
import axios from "axios";

const Settings = () => {
  const userRole = localStorage.getItem("userRole");
  const [usernameToDelete, setUsernameToDelete] = useState("");
  const [message, setMessage] = useState("");
  const [messageColor, setMessageColor] = useState("red");

  const handleDeleteUser = async () => {
    if (!usernameToDelete) {
      setMessage("⚠️ Wprowadź nazwę użytkownika.");
      setMessageColor("red");
      return;
    }

    const confirmDelete = window.confirm(
      `Na pewno chcesz usunąć użytkownika "${usernameToDelete}"?`
    );
    if (!confirmDelete) return;

    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      setMessage("Brak tokenu dostępu. Zaloguj się ponownie.");
      setMessageColor("red");
      return;
    }

    try {
      const response = await axios.delete(
        `http://localhost:8000/api/admin/delete-user/${usernameToDelete}/`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
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
        setMessage("🔒 Sesja wygasła. Zaloguj się ponownie.");
        localStorage.clear();
        window.location.href = "/login";
      } else {
        setMessage("⚠️ Wystąpił błąd podczas usuwania użytkownika.");
      }
      setMessageColor("red");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Ustawienia konta</h1>

      {userRole === "admin" ? (
        <div>
          <h2 style={{ marginBottom: "1rem" }}>Panel administratora</h2>
          <label>
            Nazwa użytkownika do usunięcia:
            <input
              type="text"
              value={usernameToDelete}
              onChange={(e) => setUsernameToDelete(e.target.value)}
              placeholder="np. jan.kowalski"
              style={{
                marginLeft: "1rem",
                padding: "0.5rem",
                borderRadius: "4px",
                border: "1px solid #ccc",
              }}
            />
          </label>
          <br />
          <button
            onClick={handleDeleteUser}
            style={{
              marginTop: "1rem",
              padding: "0.5rem 1rem",
              backgroundColor: "#cc0000",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Usuń konto użytkownika
          </button>
          {message && (
            <p style={{ color: messageColor, marginTop: "1rem" }}>{message}</p>
          )}
        </div>
      ) : (
        <p>Nie masz uprawnień administratora, aby usuwać konta.</p>
      )}
      <a
            onClick={() => {
              localStorage.clear();
              navigate("/login");
            }}
          >
            Logout
          </a>
    </div>
  );
};

export default Settings;
