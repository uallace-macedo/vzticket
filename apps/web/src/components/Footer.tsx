import { Link } from 'react-router-dom'

export function Footer() {
  return (
    <footer className="border-t border-foreground/10 bg-background py-8">
      <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-foreground-muted">
        <div className="flex items-center gap-2">
          <span className="font-bold text-primary text-sm">VzTicket</span>
          <span>© {new Date().getFullYear()} - Todos os direitos reservados.</span>
        </div>
        
        <div className="flex gap-4">
          <Link to="/events" className="hover:text-foreground">Eventos</Link>
          <button className="hover:text-foreground">Termos</button>
          <button className="hover:text-foreground">Privacidade</button>
        </div>
      </div>
    </footer>
  )
}