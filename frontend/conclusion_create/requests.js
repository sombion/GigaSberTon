async function load_statements() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/applications/filter?is_departure=true', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            let data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let applications_data = await response.json();
        let applications = applications_data.applications || applications_data; // на случай если бэк возвращает массив

        const statementSelect = document.getElementById("statement");
        statementSelect.innerHTML = `<option value="">Выберите заявление</option>`; // сбрасываем старые опции

        if (applications.length === 0) {
            const option = document.createElement("option");
            option.value = "";
            option.disabled = true;
            option.textContent = "Заявлений нет";
            statementSelect.appendChild(option);
        } else {
            applications.forEach(application => {
                const option = document.createElement("option");
                option.value = application.id;
                option.textContent = `${application.id}: ${application.fio} — ${application.street}`;
                statementSelect.appendChild(option);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки заявлений: ${error}`);
        console.error("Ошибка загрузки заявлений:", error);
    }
}

async function fetch_users() {
    let response = await fetch('http://127.0.0.1:8000/api/auth/all', {
        method: 'GET',
        credentials: 'include'
    });

    if (!response.ok) {
        let data = await response.json();
        showToast(`${data.detail}`);
        throw new Error(`Ошибка запроса: ${response.status}`);
    }

    let users_data = await response.json();
    return users_data.users || []; // возвращаем массив пользователей
}

// Заполняем select для председателя
async function load_chairman() {
    try {
        let users = await fetch_users();
        const chairmanSelect = document.getElementById("chairman");
        chairmanSelect.innerHTML = `<option value="">Выберите председателя</option>`; // сбрасываем старые опции

        users.forEach(user => {
            const option = document.createElement("option");
            option.value = user.id; // важное — ID для отправки на бэк
            option.textContent = user.fio;
            chairmanSelect.appendChild(option);
        });
    } catch (error) {
        showToast(`Ошибка загрузки председателей: ${error}`);
        console.error("Ошибка загрузки председателей:", error);
    }
}

// Заполняем select для членов комиссии
async function load_members() {
    try {
        let users = await fetch_users();
        const membersSelect = document.getElementById("members");
        membersSelect.innerHTML = ""; // сбрасываем старые опции

        users.forEach(user => {
            const option = document.createElement("option");
            option.value = user.id; // важное — ID для отправки на бэк
            option.textContent = user.fio;
            membersSelect.appendChild(option);
        });
    } catch (error) {
        showToast(`Ошибка загрузки членов комиссии: ${error}`);
        console.error("Ошибка загрузки членов комиссии:", error);
    }
}

document.addEventListener("DOMContentLoaded", function() {
  $('#members').select2({
    placeholder: "Выберите членов комиссии"
  });

  // Автоматическая установка сегодняшней даты
  const dateInput = document.getElementById("date");
  if (dateInput) {
    let today = new Date().toISOString().split("T")[0];
    dateInput.value = today;
  }

  // Обработчик отправки формы
  const form = document.querySelector("form");
  form.addEventListener("submit", async function (event) {
    event.preventDefault(); // отключаем перезагрузку страницы

    try {
      const applications_id = document.getElementById("statement").value;
      const date = document.getElementById("date").value;
      const chairman_id = document.getElementById("chairman").value;
      const members_id = Array.from(document.getElementById("members").selectedOptions).map(opt => opt.value);
      const documents = document.getElementById("documents").value.trim();
      const justification = document.getElementById("inspection").value.trim();
      const conclusion = document.getElementById("conclusion").value.trim();

      // Валидация (минимальная)
      if (!applications_id) {
        showToast("Выберите заявление!");
        return;
      }
      if (!chairman_id) {
        showToast("Выберите председателя!");
        return;
      }
      if (members_id.length === 0) {
        showToast("Выберите хотя бы одного члена комиссии!");
        return;
      }

      const payload = {
        applications_id: Number(applications_id),
        date: new Date(date).toISOString(),
        chairman_id: Number(chairman_id),
        members_id: members_id.map(id => Number(id)), // массив чисел
        justification: justification,
        documents: documents,
        conclusion: conclusion
      };

      let response = await fetch('http://127.0.0.1:8000/api/conclusion/create', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        let data = await response.json();
        showToast(`Ошибка: ${data.detail || response.status}`);
        throw new Error(`Ошибка запроса: ${response.status}`);
      }

      showToast("Заключение успешно создано");
      form.reset(); // очищаем форму
      $('#members').val(null).trigger('change'); // сбрасываем select2
    } catch (error) {
      showToast(`Ошибка отправки: ${error}`);
      console.error("Ошибка отправки заключения:", error);
    }
  });
});

// Вызываем обе функции при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
    load_statements();
    load_chairman();
    load_members();
});