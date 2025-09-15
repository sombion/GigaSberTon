const API_URL = "http://127.0.0.1:8000/api/notification";

async function loadNotifications() {
  try {
    const res = await fetch(`${API_URL}/all`, {
      credentials: "include" // <-- добавили
    });
    if (!res.ok) throw new Error("Ошибка загрузки уведомлений");
    const data = await res.json();
    renderNotifications(data.notifications);
  } catch (err) {
    console.error(err);
  }
}

function renderNotifications(notifications) {
  const list = document.getElementById("notificationsList");
  list.innerHTML = "";

  notifications.forEach(n => {
    const card = document.createElement("div");
    card.className = "notification-card" + (n.read ? " read" : "");
    card.innerHTML = `
      <span>${n.text}</span>
      <div class="actions">
        <button class="btn-read" data-id="${n.id}">Прочитать</button>
        <button class="btn-delete" data-id="${n.id}">Удалить</button>
      </div>
    `;
    list.appendChild(card);
  });

  list.querySelectorAll(".btn-read").forEach(btn => {
    btn.addEventListener("click", e => markRead(btn.dataset.id, e));
  });

  list.querySelectorAll(".btn-delete").forEach(btn => {
    btn.addEventListener("click", e => deleteNotification(btn.dataset.id, e));
  });

  updateCounter();
}

async function markRead(id, event) {
  try {
    await fetch(`${API_URL}/read`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // <-- добавили
      body: JSON.stringify({ id })
    });

    event.target.closest(".notification-card").classList.add("read");
    updateCounter();
  } catch (err) {
    console.error("Ошибка при чтении уведомления", err);
  }
}

async function deleteNotification(id, event) {
  try {
    await fetch(`${API_URL}/delete`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // <-- добавили
      body: JSON.stringify({ id })
    });

    event.target.closest(".notification-card").remove();
    updateCounter();
  } catch (err) {
    console.error("Ошибка при удалении уведомления", err);
  }
}

async function markAllRead() {
  try {
    // Запрос к API
    const res = await fetch(`${API_URL}/read-all`, {
      method: "GET",
      credentials: "include"
    });

    if (!res.ok) throw new Error("Ошибка при чтении всех уведомлений");

    document.querySelectorAll(".notification-card").forEach(card => {
      card.classList.add("read");
    });

    updateCounter();
  } catch (err) {
    console.error("Ошибка при чтении всех уведомлений", err);
  }
}


function updateCounter() {
  const total = document.querySelectorAll(".notification-card").length;
  const unread = document.querySelectorAll(".notification-card:not(.read)").length;
  document.getElementById("counter").textContent =
    `Всего уведомлений: ${total} | Непрочитанных: ${unread}`;
}

document.addEventListener("DOMContentLoaded", loadNotifications);
