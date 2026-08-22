# ruff: noqa: E501, PLR2004
from datetime import datetime

from vzticket.modules.wallet_claim_tokens.schemas import ClaimTokenResponse

CLAIM_TYPE_CONFIG = {
    "deposit": {
      "title": "Depósito Confirmado",
      "subtitle": "O saldo já está disponível na sua carteira!",
      "amount_label": "Valor Depositado",
      "badge_text": "Saldo Adicionado",
    },
    "ticket_purchase": {
      "title": "Ingresso Garantido",
      "subtitle": "Sua compra foi confirmada com sucesso!",
      "amount_label": "Valor Pago",
      "badge_text": "Compra Realizada",
    },
    "event_fee": {
      "title": "Taxa Processada",
      "subtitle": "O pagamento da taxa do evento foi confirmado!",
      "amount_label": "Valor da Taxa",
      "badge_text": "Taxa de Evento",
    },
}


def render_deposit_success_html(claim_data: ClaimTokenResponse) -> str:
    claim_type_str = str(getattr(claim_data, "type", "deposit")).lower()
    config = CLAIM_TYPE_CONFIG.get(
        claim_type_str, CLAIM_TYPE_CONFIG["deposit"]
    )

    try:
        amount_float = float(claim_data.amount)
        formatted_amount = f"R$ {amount_float:,.2f}".replace(
        ",", "X"
        ).replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        formatted_amount = f"R$ {claim_data.amount}"

    raw_date = claim_data.claimed_at
    formatted_date = "---"
    if raw_date:
        try:
            dt = datetime.fromisoformat(str(raw_date).replace("Z", "+00:00"))
            formatted_date = dt.strftime("%d/%m/%Y às %H:%M")
        except ValueError:
            formatted_date = str(raw_date)

    claim_id = str(claim_data.id)
    short_id = (
        f"{claim_id[:8]}...{claim_id[-4:]}"
        if len(claim_id) > 12
        else claim_id
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{config['title']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
      :root {{
        --app-bg: #FAFAFA;
        --app-fg: #202020;
        --app-fg-muted: #595959;
        --app-bg-muted: #F3F3EF;
        --app-primary: #0634CA;
        --app-primary-fg: #FFFFFF;
        --app-emerald: #10B981;
        --app-emerald-bg: rgba(16, 185, 129, 0.1);
        --app-border: rgba(0, 0, 0, 0.08);
        --font-sans: 'Sora', sans-serif;
      }}

      * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: var(--font-sans);
      }}

      body {{
        background-color: var(--app-bg);
        color: var(--app-fg);
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        padding: 1rem;
      }}

      .card {{
        background-color: #FFFFFF;
        border: 1px solid var(--app-border);
        border-radius: 1.25rem;
        width: 100%;
        max-width: 420px;
        padding: 2rem 1.75rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
      }}

      .icon-container {{
        width: 3.5rem;
        height: 3.5rem;
        background-color: var(--app-emerald-bg);
        color: var(--app-emerald);
        border-radius: 9999px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.25rem;
      }}

      .icon-container svg {{
        width: 1.75rem;
        height: 1.75rem;
      }}

      .header {{
        text-align: center;
        margin-bottom: 1.5rem;
      }}

      .badge {{
        display: inline-block;
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--app-primary);
        background-color: rgba(6, 52, 202, 0.08);
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        margin-bottom: 0.75rem;
      }}

      .title {{
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        text-transform: uppercase;
        color: var(--app-fg);
      }}

      .subtitle {{
        font-size: 0.8125rem;
        color: var(--app-fg-muted);
        margin-top: 0.35rem;
        font-weight: 500;
      }}

      .details-box {{
        background-color: var(--app-bg-muted);
        border: 1px solid var(--app-border);
        border-radius: 0.875rem;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
      }}

      .detail-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.625rem 0;
        font-size: 0.8125rem;
        border-bottom: 1px solid var(--app-border);
      }}

      .detail-row:last-child {{
        border-bottom: none;
      }}

      .detail-label {{
        color: var(--app-fg-muted);
        font-weight: 600;
      }}

      .detail-value {{
        color: var(--app-fg);
        font-weight: 700;
      }}

      .detail-value.amount {{
        font-size: 1.125rem;
        color: var(--app-fg);
        font-weight: 800;
      }}

      .detail-value.mono {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.75rem;
        color: var(--app-fg-muted);
      }}

      .footer {{
        text-align: center;
        font-size: 0.75rem;
        color: var(--app-fg-muted);
        font-weight: 500;
      }}
    </style>
  </head>
  <body>
    <div class="card">
      <div class="icon-container">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="3">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>

      <div class="header">
        <span class="badge">{config['badge_text']}</span>
        <h1 class="title">{config['title']}</h1>
        <p class="subtitle">{config['subtitle']}</p>
      </div>

      <div class="details-box">
        <div class="detail-row">
          <span class="detail-label">{config['amount_label']}</span>
          <span class="detail-value amount">{formatted_amount}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Método</span>
          <span class="detail-value">PIX</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">ID da Operação</span>
          <span class="detail-value mono" title="{claim_id}">{short_id}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Data e Hora</span>
          <span class="detail-value">{formatted_date}</span>
        </div>
      </div>

      <div class="footer">
        <p>Você já pode fechar esta aba com segurança.</p>
      </div>
    </div>
  </body>
</html>"""
