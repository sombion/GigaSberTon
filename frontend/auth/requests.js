document.querySelector("form").addEventListener("submit", async function (e) {
    e.preventDefault(); // отменяем стандартную отправку формы

    let login = document.getElementById("login").value.trim();
    let password = document.getElementById("password").value.trim();

    try {
        let response = await fetch("http://127.0.0.1:8000/api/auth/login", {
            method: "POST",
            credentials: "include", // сохраняем cookie для сессии
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ login, password })
        });

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`); // вывод ошибки с бэка
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let userData = await response.json();
        console.log("Авторизация успешна:", userData);

        // Например: редирект на страницу профиля
        window.location.href = "/applications/applications.html";

    } catch (error) {
        showToast(`Ошибка авторизации: ${error}`);
        console.error("Ошибка авторизации:", error);
    }
});