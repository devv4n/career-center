package rest

import (
	"context"
	"errors"
	"fmt"
	"html/template"
	"log/slog"
	"net/http"
	"time"

	"github.com/devv4n/career-center/internal/config"
	"github.com/devv4n/career-center/internal/service"
)

type Server struct {
	Service *service.Service
	cfg     *config.Config
	db      Storage
	server  *http.Server
}

type Storage interface {
}

const DefaultReadHeaderTimeout = 5 * time.Second

var tmpl *template.Template

// NewServer создаёт новый server.
func NewServer(s *service.Service, cfg *config.Config) *Server {
	return &Server{Service: s, cfg: cfg}
}

func (s *Server) Serve() {
	tmpl = template.Must(template.ParseGlob("templates/*.html"))

	mux := http.NewServeMux()

	mux.HandleFunc("GET /", s.showIndex)

	mux.HandleFunc("GET /vacancies", s.showVacancies)
	mux.HandleFunc("GET /vacancies/{id}", s.showVacancyDetail)

	mux.HandleFunc("GET /events", s.showEvents)
	mux.HandleFunc("GET /events/{id}", s.showEventDetail)

	mux.HandleFunc("POST /api/new-row", s.newRowHandler)
	mux.HandleFunc("GET /api/add-vacancy/{id}", s.newRowHandler)

	s.server = &http.Server{
		Addr:              fmt.Sprintf(":%d", s.cfg.Port),
		Handler:           LogMiddleware(mux),
		ReadHeaderTimeout: DefaultReadHeaderTimeout,
	}

	slog.Info("server starting", "address", s.server.Addr)

	if err := s.server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		slog.Error("error starting server", "error", err)
	}
}

func (s *Server) Shutdown(ctx context.Context) error {
	slog.Info("shutting down server gracefully")
	return s.server.Shutdown(ctx)
}
