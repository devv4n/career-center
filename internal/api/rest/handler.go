package rest

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
)

func (s *Server) showIndex(w http.ResponseWriter, r *http.Request) {
	if err := tmpl.ExecuteTemplate(w, "index.html", nil); err != nil {
		http.Error(w, "Ошибка отображения страницы", http.StatusInternalServerError)
	}
}

func (s *Server) showVacancies(w http.ResponseWriter, _ *http.Request) {
	var vacancies []Vacancy
	err := db.Select(&vacancies, "SELECT * FROM vacancies")
	if err != nil {
		http.Error(w, "Ошибка получения данных", http.StatusInternalServerError)
		return
	}
	if err := tmpl.ExecuteTemplate(w, "vacancies.html", map[string]interface{}{"Vacancies": vacancies}); err != nil {
		http.Error(w, "Ошибка отображения страницы", http.StatusInternalServerError)
	}
}

func (s *Server) showEvents(w http.ResponseWriter, _ *http.Request) {
	var events []Event
	err := db.Select(&events, "SELECT * FROM events")
	if err != nil {
		http.Error(w, "Ошибка получения данных", http.StatusInternalServerError)
		return
	}
	if err = tmpl.ExecuteTemplate(w, "events.html", map[string]interface{}{"Events": events}); err != nil {
		http.Error(w, "Ошибка отображения страницы", http.StatusInternalServerError)
	}
}

func (s *Server) showVacancyDetail(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	var vacancy Vacancy
	err := db.Get(&vacancy, "SELECT * FROM vacancies WHERE id = $1", id)
	if err != nil {
		if err == sql.ErrNoRows {
			http.NotFound(w, r)
		} else {
			http.Error(w, "Ошибка получения данных", http.StatusInternalServerError)
		}
		return
	}

	if err = tmpl.ExecuteTemplate(w, "vacancy_detail.html", map[string]interface{}{"Vacancy": vacancy}); err != nil {
		http.Error(w, "Ошибка отображения страницы", http.StatusInternalServerError)
	}
}

func (s *Server) showEventDetail(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	var event Event
	err := db.Get(&event, "SELECT * FROM events WHERE id = $1", id)
	if err != nil {
		if err == sql.ErrNoRows {
			http.NotFound(w, r)
		} else {
			http.Error(w, "Ошибка получения данных", http.StatusInternalServerError)
		}
		return
	}

	if err = tmpl.ExecuteTemplate(w, "event_detail.html", map[string]interface{}{"Event": event}); err != nil {
		http.Error(w, "Ошибка отображения страницы", http.StatusInternalServerError)
	}
}

func (s *Server) newRowHandler(w http.ResponseWriter, r *http.Request) {
	var rowData RowData
	if err := json.NewDecoder(r.Body).Decode(&rowData); err != nil {
		http.Error(w, "Ошибка декодирования данных", http.StatusBadRequest)
		return
	}

	fmt.Printf("Получены данные: %+v\n", rowData)

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Данные получены"))
}
