async function subscribe_signature(conclusionId) {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/signature/subscribe', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ conclusion_id: conclusionId })
        });

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let result = await response.json();
        showToast("Подписка успешно оформлена");
        console.log("Результат подписки:", result);

        return result;

    } catch (error) {
        showToast(`Ошибка подписки: ${error}`);
        console.error("Ошибка подписки:", error);
    }
}


document.addEventListener("DOMContentLoaded", function () {
  const districtBtn = document.getElementById("districtBtn");
  const districtList = document.getElementById("districtList");

  districtList.addEventListener("change", function () {
    const checked = [...districtList.querySelectorAll("input[type=checkbox]:checked")];
    if (checked.length === 0) {
      districtBtn.textContent = "Выберите районы ▾";
    } else if (checked.length <= 3) {
    const names = checked.map(cb => cb.value).join(", ");
      districtBtn.textContent = names + " ▾";
    } else {
        districtBtn.textContent = `Выбрано ${checked.length} районов`;
    }
  });

  // --- модалка ---
  const modal = document.getElementById("modal");
  const previewFrame = document.getElementById("previewFrame");
  const closeBtn = document.querySelector(".close");
  const approveBtn = document.getElementById("approveBtn");
  const rejectBtn = document.getElementById("rejectBtn");

  let currentId = null; // будем хранить id текущего заявления

  // Делегирование событий: ловим клики по кнопкам "Подписать"
  document.getElementById("applicationsList").addEventListener("click", (e) => {
    if (e.target.classList.contains("sign-btn")) {
      currentId = e.target.id; // сохраняем id кнопки
      console.log("Открыто заявление с id:", currentId);

      // вставляем id в src iframe
      previewFrame.src = `http://127.0.0.1:8000/api/conclusion/view/${currentId}`;

      // показываем модалку
      modal.style.display = "flex";
    }
  });

  // Обработка кнопки "Подписать"
  approveBtn.addEventListener("click", () => {
    if (currentId) {
      console.log("Заявление подписано:", currentId);
      subscribe_signature(currentId);
      modal.style.display = "none";
    }
  });

  // Обработка кнопки "Отклонить"
  rejectBtn.addEventListener("click", () => {
    if (currentId) {
      modal.style.display = "none";
    }
  });

  // Закрытие модалки
  closeBtn.addEventListener("click", () => modal.style.display = "none");
  window.addEventListener("click", e => {
    if (e.target === modal) modal.style.display = "none";
  });


});
