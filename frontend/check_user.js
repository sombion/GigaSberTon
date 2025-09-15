async function load_profile() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/auth/me', {
            method: 'GET',
            credentials: 'include'
        });

        // Проверка авторизации
        if (response.status === 401) {
            window.location.href = '/auth/login.html';
            return;
        }

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }
    } catch (error) {
        showToast(`Ошибка загрузки профиля: ${error}`);
        console.error("Ошибка загрузки профиля:", error);
    }
}

document.addEventListener("DOMContentLoaded", load_profile);
