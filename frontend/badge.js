// badge.js

document.addEventListener("DOMContentLoaded", async () => {
    // Функция обновления цифры непрочитанных уведомлений
    async function updateBadge() {
        try {
            // Здесь делаем запрос к API на получение всех уведомлений текущего пользователя
            let response = await fetch("http://127.0.0.1:8000/api/notification/all", {
                method: "GET",
                credentials: "include"
            });

            if (!response.ok) {
                console.error("Ошибка запроса уведомлений:", response.status);
                return;
            }

            let data = await response.json();
            // Считаем только непрочитанные
            let unreadCount = data.notifications.filter(n => !n.read).length;

            const badge = document.querySelector(".notifications .badge");
            if (badge) {
                badge.textContent = unreadCount;
                badge.style.display = unreadCount > 0 ? "inline-block" : "none";
            }
        } catch (error) {
            console.error("Ошибка обновления бейджа уведомлений:", error);
        }
    }

    // Вызываем сразу при загрузке страницы
    updateBadge();

    // Пример: если на странице есть кнопки "Прочитать" или "Удалить", можно обновлять цифру после действия
    document.addEventListener("click", (e) => {
        const btn = e.target;
        if (btn.matches(".btn-read, .btn-delete, .mark-all-btn")) {
            // Немного задержки, чтобы изменения успели произойти на бэке
            setTimeout(updateBadge, 100);
        }
    });

    // Можно вызывать updateBadge() периодически, если уведомления могут приходить в реальном времени
    // setInterval(updateBadge, 30000); // например каждые 30 секунд
});