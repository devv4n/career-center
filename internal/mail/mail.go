package mail

import (
	"bytes"
	"github.com/devv4n/career-center/internal/config"
	"gopkg.in/gomail.v2"
	"html/template"
	"log"
)

type Mailer struct {
	cfg    config.Config
	dialer *gomail.Dialer
}

func NewMailer(cfg config.Config) *Mailer {
	return &Mailer{
		cfg:    cfg,
		dialer: gomail.NewDialer(cfg.Mail.Host, cfg.Mail.Port, cfg.Mail.User, cfg.Mail.Pass),
	}
}

func (m *Mailer) sendEmail(data map[string]string) {
	msg := gomail.NewMessage()
	msg.SetHeader("From", m.cfg.Mail.User)
	msg.SetHeader("To", m.cfg.Mail.CareerCentreMail)
	msg.SetHeader("Subject", "New Vacancy Data")

	t, err := template.ParseFiles("templates/mail.html")
	if err != nil {
		log.Printf("Ошибка при загрузке шаблона: %v", err)
		return
	}

	var body bytes.Buffer
	if err = t.Execute(&body, data); err != nil {
		log.Printf("Ошибка при выполнении шаблона: %v", err)
		return
	}

	msg.SetBody("text/html", body.String())

	if err = m.dialer.DialAndSend(msg); err != nil {
		log.Printf("Ошибка отправки email: %v", err)
	}
}
