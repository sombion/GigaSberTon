async function load_applications() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/applications/all', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let applications_data = await response.json();
        let count = applications_data.count
        let applications = applications_data.applications

        let foundCount = document.getElementById('foundCount')
        let textSearch = document.getElementById('textSearch')
        let word = document.getElementById('word')
        
        foundCount.textContent = count
        textSearch.textContent = "Всего: "
        word.textContent = declension(count)

        const applicationsList = document.getElementById("applicationsList");
        applicationsList.innerHTML = "";

        if (count == 0) {
            const emptyBlock = document.createElement("div");
            emptyBlock.className = "empty-block";
            emptyBlock.textContent = "Список заявлений пуст.";
            applicationsList.appendChild(emptyBlock);
        } else {
            applications.forEach(application => {
                const card = document.createElement("div");
                card.className = "app-card";
                card.dataset.district = application.district;
                
                let formatted;
                if (application.departure_date != null) {
                    formatted = new Date(application.departure_date).toLocaleDateString("ru-RU").replace(/\./g, "-");
                } else {
                    formatted = "Не назначена"
                }
                card.innerHTML = `
                    <div class="application" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span> ${application.id}</span>
                        <span><b>ФИО:</b> ${application.fio}</span>
                        <span><b>Адрес:</b> ${application.street}</span>
                        <span><b>Телефон:</b> ${application.phone}</span>
                        <span><b>Дата выезда:</b> ${formatted}</span>
                    </div>
                    <a href="application_details.html?id=${application.id}" class="btn-details">Подробнее</a>
                `;

                applicationsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки заявок: ${error}`);
        console.error("Ошибка загрузки заявок:", error);
    }
}

async function load_street() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/applications/street', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let streetData = await response.json();
        let streets = streetData.streets

        const districtList = document.getElementById("districtList");
        districtList.innerHTML = "";

        
        streets.forEach(street => {
            const streetCard = document.createElement("label");
            streetCard.dataset.district = street.street;

            // создаём чекбокс
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.name = "district";
            checkbox.value = street.street;

            // добавляем чекбокс и текст
            streetCard.appendChild(checkbox);
            streetCard.appendChild(document.createTextNode(" " + street.street));

            districtList.appendChild(streetCard);
        });
        

    } catch (error) {
        showToast(`Ошибка загрузки заявок: ${error}`);
        console.error("Ошибка загрузки заявок:", error);
    }
}

function declension(num) {
  num = Math.abs(num) % 100;
  const n1 = num % 10;
  if (num > 10 && num < 20) return "заявлений";
  if (n1 > 1 && n1 < 5) return "заявления";
  if (n1 === 1) return "заявление";
  return "заявлений";
}

async function search_applications() {
    try {
        let searchInput = document.getElementById("searchInput")
        text = searchInput.value
        let response = await fetch(`http://127.0.0.1:8000/api/applications/search/${text}`, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let applications_data = await response.json();
        let count = applications_data.count
        let applications = applications_data.applications

        let foundCount = document.getElementById('foundCount')
        let textSearch = document.getElementById('textSearch')
        let word = document.getElementById('word')
        
        foundCount.textContent = count
        textSearch.textContent = "Найдено: "
        word.textContent = declension(count)

        const applicationsList = document.getElementById("applicationsList");
        applicationsList.innerHTML = "";

        if (count == 0) {
            const emptyBlock = document.createElement("div");
            emptyBlock.className = "empty-block";
            emptyBlock.textContent = "Ничего не найдено по вашему запросу.";
            applicationsList.appendChild(emptyBlock);
        } else {
            applications.forEach(application => {
                const card = document.createElement("div");
                card.className = "app-card";
                card.dataset.district = application.district;

                let formatted;
                if (application.departure_date != null) {
                    formatted = new Date(application.departure_date).toLocaleDateString("ru-RU").replace(/\./g, "-");
                } else {
                    formatted = "Не назначена"
                }
                card.innerHTML = `
                    <div class="application" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span> ${application.id}</span>
                        <span><b>ФИО:</b> ${application.fio}</span>
                        <span><b>Адрес:</b> ${application.street}</span>
                        <span><b>Телефон:</b> ${application.phone}</span>
                        <span><b>Дата выезда:</b> ${formatted}</span>
                    </div>
                    <a href="application_details.html?id=${application.id}" class="btn-details">Подробнее</a>
                `;

                applicationsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки заявок: ${error}`);
        console.error("Ошибка загрузки заявок:", error);
    }
}

async function apply_filters() {
    try {
        // Собираем выбранные районы
        const street = [...document.querySelectorAll("input[name='district']:checked")]
            .map(cb => cb.value);

        // Даты
        const dateFrom = document.getElementById("dateFrom").value;
        const dateTo = document.getElementById("dateTo").value;

        // Чекбокс "Назначен выезд"
        const is_departure = document.getElementById("filterVisit").checked;

        // Формируем query параметры
        const params = new URLSearchParams();
        if (street.length > 0) params.append("street", street.join(","));
        if (dateFrom) params.append("date_from", dateFrom);
        if (dateTo) params.append("date_to", dateTo);
        if (is_departure) params.append("is_departure", "true");

        // Отправляем запрос
        let response = await fetch(`http://127.0.0.1:8000/api/applications/filter?${params.toString()}`, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            const data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let applications_data = await response.json();
        let count = applications_data.count;
        let applications = applications_data.applications;

        let foundCount = document.getElementById('foundCount');
        let textSearch = document.getElementById('textSearch');
        let word = document.getElementById('word');
        
        foundCount.textContent = count;
        textSearch.textContent = "Найдено: ";
        word.textContent = declension(count);

        const applicationsList = document.getElementById("applicationsList");
        applicationsList.innerHTML = "";

        if (count === 0) {
            const emptyBlock = document.createElement("div");
            emptyBlock.className = "empty-block";
            emptyBlock.textContent = "Ничего не найдено по выбранным фильтрам.";
            applicationsList.appendChild(emptyBlock);
        } else {
            applications.forEach(application => {
                const card = document.createElement("div");
                card.className = "app-card";
                card.dataset.district = application.district;

                let formatted;
                if (application.departure_date != null) {
                    formatted = new Date(application.departure_date).toLocaleDateString("ru-RU").replace(/\./g, "-");
                } else {
                    formatted = "Не назначена"
                }
                card.innerHTML = `
                    <div class="application" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span> ${application.id}</span>
                        <span><b>ФИО:</b> ${application.fio}</span>
                        <span><b>Адрес:</b> ${application.street}</span>
                        <span><b>Телефон:</b> ${application.phone}</span>
                        <span><b>Дата выезда:</b> ${formatted}</span>
                    </div>
                    <a href="application_details.html?id=${application.id}" class="btn-details">Подробнее</a>
                `;

                applicationsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки фильтров: ${error}`);
        console.error("Ошибка загрузки фильтров:", error);
    }
}

async function setDeparture(applications_id, departure_date) {
    try {
        let response = await fetch("http://127.0.0.1:8000/api/applications/departure", {
            method: "PATCH",
            headers: {
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                applications_id: applications_id,
                departure_date: departure_date
            })
        });

        let data = await response.json();

        if (!response.ok) {
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        showToast(data.detail);
        load_applications();

        document.getElementById("applicationsInput").value = "";
        document.getElementById("assignDate").value = "";

    } catch (error) {
        showToast(`Ошибка назначения выезда: ${error}`);
        console.error("Ошибка назначения выезда:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Загрузка заявлений
    load_applications();
    // Загрузка регионов
    load_street();

    // Поиск
    const searchBtn = document.getElementById("searchBtn");
    searchBtn.addEventListener("click", async () => {
        await search_applications();
    });

    // Применение фильтров
    const applyFilters = document.getElementById("applyFilters");
    applyFilters.addEventListener("click", async () => {
        await apply_filters();
    });


    const dateFrom = document.getElementById("dateFrom");
    const dateTo = document.getElementById("dateTo");

    const clearFiltersBtn = document.getElementById("clearFilters");
    
    const filterVisit = document.getElementById("filterVisit");

    // --- Сброс фильтров ---
    clearFiltersBtn.addEventListener("click", () => {
        // Сбрасываем чекбоксы
        document.querySelectorAll("input[name='district']").forEach(ch => ch.checked = false);

        // Сбрасываем даты
        dateFrom.value = "";
        dateTo.value = "";

        // Возвращаем текст кнопки выбора районов
        districtBtn.textContent = "Выберите районы ▾";

        filterVisit.checked = false
        load_applications();
    });

    // Назначить дату
    document.getElementById("assignBtn").addEventListener("click", () => {
        const apps = document.getElementById("applicationsInput").value;
        const date = document.getElementById("assignDate").value;
        if (apps == '') {
            showToast("Укажите номер заявления");
            return 0;
        }
        if (date == '') {
            showToast("Заполните дату");
            return 0;
        }
        setDeparture(apps, date);
  });
});
