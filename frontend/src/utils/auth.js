import axios from "axios";

export const handleAuthError = async (onSuccess, navigate) => {
  try {
    await axios.post("http://localhost:8000/api/token/refresh/", {}, {
      withCredentials: true,
    });
    if (onSuccess) await onSuccess();
  } catch (err) {
    localStorage.clear();
    alert("Sesja wygasła. Zaloguj się ponownie.");
    navigate("/login");
  }
};

export const logout = (navigate) => {
  localStorage.clear();
  navigate("/login");
};
