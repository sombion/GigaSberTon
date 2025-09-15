async function load_application_details() {
    try {
      // берём id из URL
      const params = new URLSearchParams(window.location.search);
      const id = params.get("id");

      if (!id) {
        console.error("ID не найден в URL");
        return;
      }

      let response = await fetch(`http://127.0.0.1:8000/api/applications/detail/${id}`, {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        let data = await response.json();
        showToast(`${data.detail}`);
        throw new Error(`Ошибка запроса: ${response.status}`);
      }

      let application = await response.json();

      // меняем h1
      document.querySelector("h1").textContent = `Заявление №${application.id}`;

      // основные данные
      document.querySelector(".card:nth-of-type(1)").innerHTML = `
        <h3>Основные данные</h3>
        <p><strong>ФИО:</strong> ${application.fio}</p>
        <p><strong>Телефон:</strong> ${application.phone}</p>
        <p><strong>Email:</strong> ${application.email}</p>
        <p><strong>Адрес:</strong> ${application.address}</p>
        <p><strong>Кадастровый номер:</strong> ${application.cadastral_number}</p>
      `;

      // статус
      document.querySelector(".card:nth-of-type(2)").innerHTML = `
        <h3>Статус <span class="badge warn">${application.status}</span></h3>
      `;

      // документ
      const iframe = document.querySelector("iframe");
      const link = document.querySelector(".btn-download");

      iframe.src = `http://127.0.0.1:8000/api/applications/view/${application.id}`;
      link.href = `http://127.0.0.1:8000/api/applications/download/${application.id}`;

    } catch (error) {
      console.error("Ошибка загрузки деталей:", error);
      showToast(`Ошибка загрузки деталей: ${error}`);
    }
}

window.addEventListener("DOMContentLoaded", load_application_details);
