export function FeaturesGrid() {
  return (
    <section className="max-w-6xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-background-muted p-8 rounded-2xl border border-foreground/5 space-y-4">
          <span className="text-xs font-bold uppercase text-primary tracking-widest">
            Para quem quer curtir
          </span>
          <h3 className="text-2xl font-black text-foreground">
            Ache o rolê perfeito sem complicação
          </h3>
          <p className="text-foreground-muted text-sm leading-relaxed">
            Navegue por festas, shows e festivais da sua região. Garanta seu
            ingresso em menos de 1 minuto via PIX.
          </p>
        </div>

        <div className="bg-foreground text-background p-8 rounded-2xl space-y-4">
          <span className="text-xs font-bold uppercase text-primary-foreground/70 tracking-widest">
            Para quem organiza ou quer repassar
          </span>
          <h3 className="text-2xl font-black">
            Venda ingressos com taxa mínima
          </h3>
          <p className="text-background/70 text-sm leading-relaxed">
            Não vai conseguir ir no evento ou quer organizar uma festa? Crie
            seu anúncio rapidinho e receba na hora.
          </p>
        </div>
      </div>
    </section>
  )
}