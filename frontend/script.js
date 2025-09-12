// ==============================
// ЛОГИКА ЗАЯВЛЕНИЙ
// ==============================
const deleteBtn = document.getElementById("deleteApp");
const assignBtn = document.getElementById("assignVisit");

deleteBtn?.addEventListener("click", () => {
  if (confirm("Вы уверены, что хотите удалить заявление?")) {
    alert("Заявление удалено!");
    window.location.href = "applications.html";
  }
});

assignBtn?.addEventListener("click", () => {
  alert("Выезд назначен на 15.09.2025. Уведомления отправлены!");
});

// Проверка ЕГРН
document.getElementById("checkBtn")?.addEventListener("click", () => {
  alert("Эмуляция: проверка ЕГРН прошла успешно!");
});

// Отправка заявления
document.getElementById("applicationForm")?.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Заявление успешно отправлено!");
});

// ==============================
// ЛОГИКА ФИЛЬТРОВ (conclusion.html)
// ==============================
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".app-card");
  const searchInput = document.getElementById("searchInput");
  const foundCount = document.getElementById("foundCount");
  const applyBtn = document.getElementById("applyFilters");
  const clearBtn = document.getElementById("clearFilters");

  const districtBtn = document.getElementById("districtBtn");
  const districtDropdown = document.getElementById("districtDropdown");
  const districtSearch = document.getElementById("districtSearch");
  const districtLabels = document.querySelectorAll("#districtList label");

  // новые элементы календаря
  const dateFromInput = document.getElementById("dateFrom");
  const dateToInput = document.getElementById("dateTo");

  if (!cards.length || !searchInput) return; // нет карточек — не выполняем

  // Открытие/закрытие dropdown
  districtBtn?.addEventListener("click", () => {
    districtDropdown?.parentElement?.classList.toggle("show");
    districtSearch?.focus();
  });

  // Закрытие при клике вне
  window.addEventListener("click", e => {
    if (!e.target.closest(".dropdown")) {
      districtDropdown?.parentElement?.classList.remove("show");
    }
  });

  // Поиск по районам
  districtSearch?.addEventListener("input", () => {
    const filter = districtSearch.value.toLowerCase();
    districtLabels.forEach(label => {
      label.style.display = label.textContent.toLowerCase().includes(filter) ? "block" : "none";
    });
  });

  function filterCards() {
    const searchText = searchInput.value.toLowerCase();
    const checkedDistricts = Array.from(document.querySelectorAll("input[name='district']:checked")).map(cb => cb.value);

    const dateFrom = dateFromInput?.value ? new Date(dateFromInput.value) : null;
    const dateTo = dateToInput?.value ? new Date(dateToInput.value) : null;

    let visibleCount = 0;

    cards.forEach(card => {
      const text = card.textContent.toLowerCase();
      const district = card.dataset.district;
      const cardDateStr = card.dataset.date; // формат YYYY-MM-DD
      const cardDate = cardDateStr ? new Date(cardDateStr) : null;

      const matchesSearch = text.includes(searchText);
      const matchesDistrict = checkedDistricts.length === 0 || checkedDistricts.includes(district);

      let matchesDate = true;
      if (dateFrom && cardDate && cardDate < dateFrom) matchesDate = false;
      if (dateTo && cardDate && cardDate > dateTo) matchesDate = false;

      if (matchesSearch && matchesDistrict && matchesDate) {
        card.style.display = "block";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    foundCount.textContent = visibleCount;
  }

  applyBtn?.addEventListener("click", filterCards);
  clearBtn?.addEventListener("click", () => {
    searchInput.value = "";
    dateFromInput.value = "";
    dateToInput.value = "";
    document.querySelectorAll("input[name='district']").forEach(cb => (cb.checked = false));
    filterCards();
  });

  document.getElementById("searchBtn")?.addEventListener("click", filterCards);

  filterCards(); // начальная фильтрация
});

// ==============================
// ЛОГИКА МОДАЛКИ ПОДПИСАНИЯ
// ==============================
const modal = document.getElementById("modal");
const modalText = document.getElementById("modalText");
const closeBtn = document.querySelector(".close");
const signButtons = document.querySelectorAll(".sign-btn");

function saveSignedDoc(doc) {
  const signed = JSON.parse(localStorage.getItem("signedDocs") || "[]");
  signed.push(doc);
  localStorage.setItem("signedDocs", JSON.stringify(signed));
}

// Открыть модалку
signButtons.forEach(button => {
  button.addEventListener("click", () => {
    const parentCard = button.closest(".app-card");
    const text = parentCard.textContent.replace("Подписать", "").trim();
    modal.dataset.currentDoc = text;
    modalText.textContent = "Документ по заявлению: " + text;
    modal.style.display = "flex";
  });
});

// Кнопки модалки
document.getElementById("approveBtn")?.addEventListener("click", () => {
  const doc = modal.dataset.currentDoc;
  saveSignedDoc(doc);

  document.querySelectorAll(".app-card").forEach(card => {
    if (card.textContent.includes(doc)) card.remove();
  });

  modal.style.display = "none";
});

document.getElementById("rejectBtn")?.addEventListener("click", () => {
  modal.style.display = "none";
});

closeBtn?.addEventListener("click", () => (modal.style.display = "none"));
window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// ==============================
// ЛОГИКА ПРОФИЛЯ
// ==============================
// Предпросмотр аватара
document.getElementById("avatar")?.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (event) => {
    document.getElementById("avatarPreview").src = event.target.result;
  };
  reader.readAsDataURL(file);
});

// Сохранение профиля
document.getElementById("profileForm")?.addEventListener("submit", (e) => {
  e.preventDefault();

  const fullname = document.getElementById("fullname").value;
  const phone = document.getElementById("phone").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  if (password && password !== confirmPassword) {
    alert("Пароли не совпадают!");
    return;
  }

  const notifEmail = document.getElementById("notifEmail")?.checked;
  const notifSMS = document.getElementById("notifSMS")?.checked;
  const notifPush = document.getElementById("notifPush")?.checked;

  alert(
    `Профиль сохранён!
ФИО: ${fullname}
Телефон: ${phone}
Email: ${email}
Уведомления: ${(notifEmail ? "Email " : "") + (notifSMS ? "SMS " : "") + (notifPush ? "Push" : "")}`
  );
});

document.querySelector('.toggle-password-btn')
    .addEventListener('click', function () {
      const section = document.querySelector('.password-section');
      section.style.display = section.style.display === 'none' ? 'block' : 'none';
    });

  document.querySelector('.save-password-btn')
    .addEventListener('click', function () {
      const oldPass = document.getElementById('old-password').value;
      const newPass = document.getElementById('new-password').value;
      const confirmPass = document.getElementById('confirm-password').value;

      if (!oldPass || !newPass || !confirmPass) {
        alert("Пожалуйста, заполните все поля.");
        return;
      }

      if (newPass !== confirmPass) {
        alert("Новые пароли не совпадают!");
        return;
      }

      alert("Пароль успешно изменён!");
    });

// ==============================
// ЗАГРУЗКА ПОДПИСАННЫХ ДОКУМЕНТОВ (signed.html)
// ==============================
if (document.getElementById("signedList")) {
  const signedList = document.getElementById("signedList");
  const signed = JSON.parse(localStorage.getItem("signedDocs") || "[]");

  if (signed.length === 0) {
    signedList.innerHTML = "<p>Пока нет подписанных документов</p>";
  } else {
    signed.forEach(doc => {
      const div = document.createElement("div");
      div.className = "app-card";
      div.textContent = doc;
      signedList.appendChild(div);
    });
  }
}


document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");
  const applicationsList = document.getElementById("applicationsList");
  const totalCountEl = document.getElementById("totalCount");
  const foundCountEl = document.getElementById("foundCount");
  const wordEl = document.getElementById("word");

  const appCards = Array.from(applicationsList.querySelectorAll(".app-card"));

  // Установим общее количество
  totalCountEl.textContent = appCards.length;

  // Склонение слова "заявление"
  function declension(num) {
    num = Math.abs(num) % 100;
    const n1 = num % 10;
    if (num > 10 && num < 20) return "заявлений";
    if (n1 > 1 && n1 < 5) return "заявления";
    if (n1 === 1) return "заявление";
    return "заявлений";
  }

  function updateCounter(count) {
    foundCountEl.textContent = count;
    wordEl.textContent = declension(count);
  }

  // Поиск
  function doSearch() {
    const query = searchInput.value.trim().toLowerCase();
    let found = 0;

    appCards.forEach(card => {
      const text = card.textContent.toLowerCase();
      if (text.includes(query)) {
        card.style.display = "flex";
        found++;
      } else {
        card.style.display = "none";
      }
    });

    updateCounter(found);
  }

  searchBtn.addEventListener("click", doSearch);

  // Поиск по Enter
  searchInput.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      doSearch();
    }
  });

  // При загрузке страницы
  updateCounter(appCards.length);
});