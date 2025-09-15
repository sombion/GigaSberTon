// Изменение ФИО
async function edit_fio(fio) {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/auth/edit-fio', {
            method: 'POST',
            credentials: 'include',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fio: fio })
        });

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        showToast("ФИО успешно изменено");
        load_profile();
    } catch (error) {
        showToast(`Ошибка изменения ФИО: ${error}`);
        console.error("Ошибка изменения ФИО:", error);
    }
}

// Изменение Email
async function edit_email(email) {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/auth/edit-email', {
            method: 'POST',
            credentials: 'include',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email })
        });

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        showToast("Email успешно изменён");
        load_profile();
    } catch (error) {
        showToast(`Ошибка изменения Email: ${error}`);
        console.error("Ошибка изменения Email:", error);
    }
}

// Изменение пароля
async function edit_password(last_password, new_password, confirm_password) {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/auth/edit-password', {
            method: 'POST',
            credentials: 'include',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                last_password: last_password,
                new_password: new_password,
                confirm_password: confirm_password
            })
        });

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        showToast("Пароль успешно изменён");
    } catch (error) {
        showToast(`Ошибка изменения пароля: ${error}`);
        console.error("Ошибка изменения пароля:", error);
    }
}

// Загрузка данных профиля
async function load_profile() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/auth/me', {
            method: 'GET',
            credentials: 'include'
        });


        if (!response.ok) {
            let data = await response.json();
            if (response.status == 401) {
                window.location.href = '/auth/login.html';
                return 0
            }
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let profile = await response.json();

        // Заполняем блок "Общая информация"
        document.querySelector(".info-section").innerHTML = `
            <p><strong>Логин:</strong> ${profile.login}</p>
            <p><strong>ФИО:</strong> ${profile.fio || "-"}</p>
            <p><strong>Email:</strong> ${profile.email || "-"}</p>
        `;

    } catch (error) {
        showToast(`Ошибка загрузки профиля: ${error}`);
        console.error("Ошибка загрузки профиля:", error);
    }
}

// Навешиваем обработчики
document.addEventListener("DOMContentLoaded", () => {
    
    load_profile();
    
    // Сохранение профиля (ФИО и Email)
    document.querySelector(".edit-section button").addEventListener("click", () => {
        const fio = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();

        if (fio) edit_fio(fio);
        if (email) edit_email(email);
    });

    // Сохранение пароля
    document.querySelector(".save-password-btn").addEventListener("click", () => {
        const lastPass = document.getElementById("old-password").value.trim();
        const newPass = document.getElementById("new-password").value.trim();
        const confirmPass = document.getElementById("confirm-password").value.trim();

        if (!lastPass || !newPass || !confirmPass) {
            showToast("Заполните все поля пароля");
            return;
        }

        if (newPass !== confirmPass) {
            showToast("Новый пароль и подтверждение не совпадают!");
            return;
        }

        edit_password(lastPass, newPass, confirmPass);
    });
});
