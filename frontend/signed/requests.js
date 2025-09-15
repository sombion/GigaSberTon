async function load_signets() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/signature/all', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let signets_data = await response.json();
        let count = signets_data.count
        let signets = signets_data.signatures

        let foundCount = document.getElementById('foundCount')
        let textSearch = document.getElementById('textSearch')
        let word = document.getElementById('word')
        
        foundCount.textContent = count
        textSearch.textContent = "Всего: "
        word.textContent = declension(count)

        const signetsList = document.getElementById("applicationsList");
        signetsList.innerHTML = "";

        if (count == 0) {
            const emptyBlock = document.createElement("div");
            emptyBlock.className = "empty-block";
            emptyBlock.textContent = "Список заявлений пуст.";
            signetsList.appendChild(emptyBlock);
        } else {
            signets.forEach(signet => {
                const card = document.createElement("div");
                card.className = "app-card";
                
                card.innerHTML = `
                    <div class="signet" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span> ${signet.conclusion_id}</span>
                        <span><b>ФИО:</b> ${signet.fio}</span>
                        <span><b>Адрес:</b> ${signet.address}</span>
                        <span><b>Кадастровый номер:</b> ${signet.cadastral_number}</span>
                    </div>
                    <a href="http://127.0.0.1:8000/api/conclusion/download/${signet.conclusion_id}" class="btn-details">Скачать</a>
                `;

                signetsList.appendChild(card);
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
        let response = await fetch(`http://127.0.0.1:8000/api/signature/search/${text}`, {
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
        let applications = applications_data.signatures

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

                card.innerHTML = `
                    <div class="signet" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span> ${application.conclusion_id}</span>
                        <span><b>ФИО:</b> ${application.fio}</span>
                        <span><b>Адрес:</b> ${application.address}</span>
                        <span><b>Кадастровый номер:</b> ${application.cadastral_number}</span>
                    </div>
                    <a href="http://127.0.0.1:8000/api/conclusion/download/${application.conclusion_id}" class="btn-details">Скачать</a>
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

        // Формируем query параметры
        const params = new URLSearchParams();
        if (street.length > 0) params.append("street", street.join(","));
        if (dateFrom) params.append("date_from", dateFrom);
        if (dateTo) params.append("date_to", dateTo);

        // Отправляем запрос
        let response = await fetch(`http://127.0.0.1:8000/api/signature/filter?${params.toString()}`, {
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
        let applications = applications_data.signatures;

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

                card.innerHTML = `
                    <div class="signet" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span> ${application.conclusion_id}</span>
                        <span><b>ФИО:</b> ${application.fio}</span>
                        <span><b>Адрес:</b> ${application.address}</span>
                        <span><b>Кадастровый номер:</b> ${application.cadastral_number}</span>
                    </div>
                    <a href="http://127.0.0.1:8000/api/conclusion/download/${application.conclusion_id}" class="btn-details">Скачать</a>
                `;

                applicationsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки фильтров: ${error}`);
        console.error("Ошибка загрузки фильтров:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    load_signets();
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
    
    // --- Сброс фильтров ---
    clearFiltersBtn.addEventListener("click", () => {
        // Сбрасываем чекбоксы
        document.querySelectorAll("input[name='district']").forEach(ch => ch.checked = false);

        // Сбрасываем даты
        dateFrom.value = "";
        dateTo.value = "";

        // Возвращаем текст кнопки выбора районов
        districtBtn.textContent = "Выберите районы ▾";

        load_signets();
    });

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
});