useNavigate
import { ArrowRight, ShieldCheck } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function HeroSection() {
  const navigate = useNavigate()

  return (
    <section className="max-w-6xl mx-auto px-4 py-12 md:py-20 grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
      <div className="md:col-span-5 flex justify-center relative">
        <div className="relative w-64 h-96 rounded-3xl overflow-hidden shadow-2xl border-4 border-background -rotate-3 hover:rotate-0 transition duration-300">
          <img
            src="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80"
            alt="Pessoas em um show"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-linear-to-t from-black/80 via-transparent to-transparent flex flex-col justify-end p-5 text-white">
            <span className="text-xs font-bold uppercase tracking-wider text-primary-foreground/80 select-none">
              Em Destaque
            </span>
            <p className="font-extrabold text-lg leading-snug select-none">
              Sua próxima melhor memória
            </p>
          </div>
        </div>
      </div>

      <div className="md:col-span-7 space-y-6 text-center md:text-left">
        <h1 className="text-3xl sm:text-5xl font-black uppercase tracking-tight text-foreground leading-tight">
          Sua plataforma de{' '}
          <span className="text-primary underline decoration-wavy decoration-2">
            experiências
          </span>{' '}
          do seu jeito.
        </h1>

        <p className="text-foreground-muted text-base sm:text-lg max-w-lg mx-auto md:mx-0">
          Compre ingressos para os melhores rolês ou venda seus bilhetes com
          facilidade, taxa justa e QR Code direto no celular.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center md:justify-start gap-3 pt-2">
          <button
            onClick={() => navigate('/events')}
            className="w-full sm:w-auto bg-primary text-primary-foreground font-bold px-6 py-3.5 rounded-xl hover:bg-primary/90 transition flex items-center justify-center gap-2 cursor-pointer"
          >
            Explorar eventos
            <ShieldCheck className="w-4 h-4" />
          </button>

          <button
            onClick={() => {/* create event */}}
            className="w-full sm:w-auto bg-background-muted text-foreground border border-foreground/10 font-bold px-6 py-3.5 rounded-xl hover:bg-foreground/5 transition flex items-center justify-center gap-2 cursor-pointer"
          >
            Anunciar ingresso
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </section>
  )
}