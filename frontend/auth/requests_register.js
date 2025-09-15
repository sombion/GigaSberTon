
document.querySelector("form").addEventListener("submit", async function (e) {
    e.preventDefault(); // отменяем стандартную отправку формы

    let login = document.getElementById("login").value.trim();
    let fio = document.getElementById("fio").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let confirmPassword = document.getElementById("confirmPassword").value.trim();

    // Проверка совпадения паролей
    if (password !== confirmPassword) {
        showToast("Пароли не совпадают");
        return;
    }

    try {
        let response = await fetch("http://127.0.0.1:8000/api/auth/register", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                login: login,
                fio: fio,
                email: email,
                password: password
            })
        });

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`); // вывод ошибки
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let userData = await response.json();
        console.log("Регистрация успешна:", userData);

        showToast("Регистрация прошла успешно!");
        // Редиректим на страницу входа
        window.location.href = "/auth/login.html";

    } catch (error) {
        showToast(`Ошибка регистрации: ${error}`);
        console.error("Ошибка регистрации:", error);
    }
});
