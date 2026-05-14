package logger

import (
	"io"
	"log"
	"os"
)

type Logger struct {
	debug   *log.Logger
	info    *log.Logger
	warning *log.Logger
	err     *log.Logger
	writer  io.Writer
}

const (
	reset  = "\033[0m"
	red    = "\033[31m"
	green  = "\033[32m"
	yellow = "\033[33m"
	blue   = "\033[34m"
)

func New(p string) *Logger {
	writer := io.Writer(os.Stdout)
	lg := log.New(writer, p, log.Ldate|log.Ltime)

	return &Logger{
		debug:   log.New(lg.Writer(), blue+"[DEBUG] "+reset, lg.Flags()),
		info:    log.New(lg.Writer(), green+"[INFO] "+reset, lg.Flags()),
		warning: log.New(lg.Writer(), yellow+"[WARNING] "+reset, lg.Flags()),
		err:     log.New(lg.Writer(), red+"[ERROR] "+reset, lg.Flags()),
		writer:  lg.Writer(),
	}
}

func (l *Logger) Debug(v ...any) {
	l.debug.Println(v...)
}

func (l *Logger) Info(v ...any) {
	l.info.Println(v...)
}

func (l *Logger) Warning(v ...any) {
	l.warning.Println(v...)
}

func (l *Logger) Error(v ...any) {
	l.err.Println(v...)
}

func (l *Logger) FatalError(v ...any) {
	l.err.Println(v...)
	os.Exit(1)
}

func (l *Logger) Debugf(fmts string, v ...any) {
	l.debug.Printf(fmts, v...)
}

func (l *Logger) Infof(fmts string, v ...any) {
	l.info.Printf(fmts, v...)
}

func (l *Logger) Warningf(fmts string, v ...any) {
	l.warning.Printf(fmts, v...)
}

func (l *Logger) Errorf(fmts string, v ...any) {
	l.err.Printf(fmts, v...)
}

func (l *Logger) FatalErrorf(fmts string, v ...any) {
	l.err.Printf(fmts, v...)
	os.Exit(1)
}
