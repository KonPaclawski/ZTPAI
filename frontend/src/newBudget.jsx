import React, { useState } from "react";
import styles from "./newBudget.module.css";

const NewBudget = () => {
  const [categories, setCategories] = useState([]);

  const addCategory = () => {
    setCategories((prev) => [
      ...prev,
      { id: Date.now(), name: "", payments: [] },
    ]);
  };

  const removeCategory = (id) => {
    setCategories((prev) => prev.filter((cat) => cat.id !== id));
  };

  const addPayment = (categoryId) => {
    setCategories((prev) =>
      prev.map((cat) =>
        cat.id === categoryId
          ? {
              ...cat,
              payments: [
                ...cat.payments,
                { id: Date.now(), title: "", amount: "", date: "" },
              ],
            }
          : cat
      )
    );
  };

  const removePayment = (categoryId, paymentId) => {
    setCategories((prev) =>
      prev.map((cat) =>
        cat.id === categoryId
          ? {
              ...cat,
              payments: cat.payments.filter((p) => p.id !== paymentId),
            }
          : cat
      )
    );
  };

  return (
    <div className={styles["main-container"]}>
      <form
        className={styles["info-container"]}
        onSubmit={(e) => e.preventDefault()}
      >
        <div className={styles["top-inputs"]}>
          <input type="text" name="title" placeholder="TYTUŁ" required />
          <input type="number" name="budget_amount" placeholder="BUDŻET" required />
        </div>

        {categories.map((cat) => (
          <div className={styles["category-group"]} key={cat.id}>
            <div className={styles["category-container"]}>
              <input
                type="text"
                name="category"
                placeholder="KATEGORIA"
                required
                value={cat.name}
                onChange={(e) => {
                  const value = e.target.value;
                  setCategories((prev) =>
                    prev.map((c) => (c.id === cat.id ? { ...c, name: value } : c))
                  );
                }}
              />
              <button
                type="button"
                className={styles["removeBtn"]}
                onClick={() => removeCategory(cat.id)}
              >
                Usuń kategorię
              </button>
            </div>

            <div className={styles["payments-container"]}>
              {cat.payments.map((payment) => (
                <div className={styles["payment-group"]} key={payment.id}>
                  <div className={styles["payment-container"]}>
                    <input
                      type="text"
                      placeholder="TYTUŁ PŁATNOŚCI"
                      required
                      value={payment.title}
                      onChange={(e) => {
                        const value = e.target.value;
                        setCategories((prev) =>
                          prev.map((c) =>
                            c.id === cat.id
                              ? {
                                  ...c,
                                  payments: c.payments.map((p) =>
                                    p.id === payment.id ? { ...p, title: value } : p
                                  ),
                                }
                              : c
                          )
                        );
                      }}
                    />
                    <button
                      type="button"
                      className={styles["removeBtn"]}
                      onClick={() => removePayment(cat.id, payment.id)}
                    >
                      Usuń płatność
                    </button>
                  </div>
                  <div className={styles["info-container"]}>
                    <input
                      type="number"
                      placeholder="KWOTA"
                      required
                      value={payment.amount}
                      onChange={(e) => {
                        const value = e.target.value;
                        setCategories((prev) =>
                          prev.map((c) =>
                            c.id === cat.id
                              ? {
                                  ...c,
                                  payments: c.payments.map((p) =>
                                    p.id === payment.id ? { ...p, amount: value } : p
                                  ),
                                }
                              : c
                          )
                        );
                      }}
                    />
                    <input
                      type="date"
                      placeholder="DATA PŁATNOŚCI"
                      required
                      value={payment.date}
                      onChange={(e) => {
                        const value = e.target.value;
                        setCategories((prev) =>
                          prev.map((c) =>
                            c.id === cat.id
                              ? {
                                  ...c,
                                  payments: c.payments.map((p) =>
                                    p.id === payment.id ? { ...p, date: value } : p
                                  ),
                                }
                              : c
                          )
                        );
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className={styles["info-container"]}>
              <button
                type="button"
                className={styles["addPaymentBtn"]}
                onClick={() => addPayment(cat.id)}
              >
                Dodaj Płatność
              </button>
            </div>
          </div>
        ))}

        <button
          type="button"
          className={styles["addCategoryBtn"]}
          onClick={addCategory}
        >
          Dodaj Nową Kategorię
        </button>

        <div className={styles["submit-container"]}>
          <a
            className={styles["buttonSecondary"]}
            href="/dashboard"
            style={{ color: "#700002" }}
          >
            COFNIJ
          </a>
          <button
            className={styles["buttonPrimary"]}
            type="submit"
            style={{ color: "#006c1e" }}
          >
            STWÓRZ
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewBudget;
