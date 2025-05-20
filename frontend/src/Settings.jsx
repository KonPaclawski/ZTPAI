import React from "react";

const Settings = () => {
  const userRole = localStorage.getItem("userRole");

  const handleDeleteUser = () => {
    // logika usuwania użytkownika — zapytanie do API
    alert("Usuwanie użytkownika (tylko admin może to robić)");
  };

  return (
    <div>
      <h1>Ustawienia konta</h1>

      {userRole === "admin" ? (
        <div>
          <h2>Panel administratora</h2>
          <button onClick={handleDeleteUser}>Usuń konto użytkownika</button>
        </div>
      ) : (
        <p>Nie masz uprawnień administratora, aby usuwać konta.</p>
      )}
    </div>
  );
};

export default Settings;
