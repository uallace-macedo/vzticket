import asyncio
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import select

from pwdlib import PasswordHash

from vzticket.core.database import AsyncSessionLocal
from vzticket.modules.users.model import User, UserRole
from vzticket.modules.wallet.model import WalletTransaction, TransactionType
from vzticket.modules.events.model import Event, EventStatus

password_hasher = PasswordHash.recommended()


async def seed_database():
    async with AsyncSessionLocal() as session:
        print("🌱 Iniciando o seed do banco de dados...")
        password_hash = password_hasher.hash("secret")

        users_data = [
            {
                "email": "client@example.com",
                "name": "Cliente Exemplo",
                "role": UserRole.CLIENT,
            },
            {
                "email": "organizer@example.com",
                "name": "Organizador Exemplo",
                "role": UserRole.ORGANIZER,
            },
            {
                "email": "gatekeeper@example.com",
                "name": "Portaria Exemplo",
                "role": UserRole.GATEKEEPER,
            },
        ]

        created_users = {}

        for u in users_data:
            stmt = select(User).where(User.email == u["email"])
            res = await session.execute(stmt)
            existing_user = res.scalar_one_or_none()

            if not existing_user:
                user = User(
                    name=u["name"],
                    email=u["email"],
                    password=password_hash,
                    role=u["role"],
                    image_url=None,
                    pending_balance=Decimal("0.00"),
                )
                user.balance = Decimal("900.00")

                session.add(user)
                await session.flush()
                created_users[u["role"]] = user
                print(f"✅ Usuário criado: {u['email']} ({u['role'].value})")
            else:
                created_users[u["role"]] = existing_user
                print(f"⚠️ Usuário já existe: {u['email']}")

        for role, user in created_users.items():
            stmt = select(WalletTransaction).where(
                WalletTransaction.user_id == user.id,
                WalletTransaction.type == TransactionType.DEPOSIT,
                WalletTransaction.amount == Decimal("900.00"),
            )
            res = await session.execute(stmt)
            if not res.scalar_one_or_none():
                deposit_tx = WalletTransaction(
                    user_id=user.id,
                    type=TransactionType.DEPOSIT,
                    amount=Decimal("900.00"),
                    description="Depósito inicial via PIX (Seed)",
                    event_id=None,
                    ticket_id=None,
                )
                session.add(deposit_tx)
                print(f"💵 Depósito de R$ 900.00 vinculado a {user.email}")

        organizer = created_users[UserRole.ORGANIZER]

        events_data = [
            {
                "title": "O Hobbit: Uma Jornada Inesperada",
                "available_tickets": 45,
                "ticket_price": Decimal("15.00"),
                "service_fee": Decimal("2.40"),
                "event_date": datetime(2026, 8, 24, 1, 17, 0, tzinfo=timezone.utc),
                "description": "Maratona Middle-Earth: Acompanhe a jornada de Bilbo Bolseiro e a comitiva dos anões para retomar a Montanha Solitária. Exibição especial remasterizada.",
                "banner_url": "https://image.tmdb.org/t/p/w500/xyXmtuvsoM5J3yNad0nvcetpBdY.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/lZtmn2pLw1kgDYj4Ig4s3DYBQCD.jpg",
                "location_name": "Cinesesc - Av Paulista",
                "cep": "01310-100",
                "address": "Avenida Paulista",
                "number": "119",
                "neighborhood": "Bela Vista",
                "city": "São Paulo",
                "city_slug": "sao-paulo",
                "state": "SP",
                "maps_url": "https://maps.google.com/?q=Cinesesc+Av+Paulista+119+Sao+Paulo",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 14, 27, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 8, 24, 1, 17, 0, tzinfo=timezone.utc),
            },
            {
                "title": "O Hobbit: A Desolação de Smaug",
                "available_tickets": 50,
                "ticket_price": Decimal("18.00"),
                "service_fee": Decimal("2.58"),
                "event_date": datetime(2026, 8, 24, 22, 15, 0, tzinfo=timezone.utc),
                "description": "Na segunda parte da trilogia, a comitiva enfrenta os perigos da Floresta das Trevas e o temível dragão Smaug.",
                "banner_url": "https://image.tmdb.org/t/p/w500/5ZYxL6k4ZHrEmrFvmY4HZVzerxG.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/ws5z2UmmVzRDD8hZtHTHfcqTOAW.jpg",
                "location_name": "Cinesesc - Av Paulista",
                "cep": "01310-100",
                "address": "Avenida Paulista",
                "number": "119",
                "neighborhood": "Bela Vista",
                "city": "São Paulo",
                "city_slug": "sao-paulo",
                "state": "SP",
                "maps_url": "https://maps.google.com/?q=Cinesesc+Av+Paulista+119+Sao+Paulo",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 15, 20, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 8, 24, 22, 15, 0, tzinfo=timezone.utc),
            },
            {
                "title": "O Hobbit: A Batalha dos Cinco Exércitos",
                "available_tickets": 49,
                "ticket_price": Decimal("20.00"),
                "service_fee": Decimal("2.70"),
                "event_date": datetime(2026, 8, 25, 22, 15, 0, tzinfo=timezone.utc),
                "description": "O desfecho épico da trilogia do Hobbit. Uma batalha colossal pelo futuro da Terra-média na tela grande.",
                "banner_url": "https://image.tmdb.org/t/p/w500/3UbaCMmqOd7mca4Y5DOzY2ZVTyX.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/wRKwrfQ7p0ttrb09G3mcOSyN1pk.jpg",
                "location_name": "Cinesesc - Av Paulista",
                "cep": "01310-100",
                "address": "Avenida Paulista",
                "number": "119",
                "neighborhood": "Bela Vista",
                "city": "São Paulo",
                "city_slug": "sao-paulo",
                "state": "SP",
                "maps_url": "https://maps.google.com/?q=Cinesesc+Av+Paulista+119+Sao+Paulo",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 15, 59, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 8, 25, 22, 15, 0, tzinfo=timezone.utc),
            },
            {
                "title": "O Senhor dos Anéis: A Sociedade do Anel",
                "available_tickets": 80,
                "ticket_price": Decimal("25.00"),
                "service_fee": Decimal("3.00"),
                "event_date": datetime(2026, 8, 28, 22, 16, 0, tzinfo=timezone.utc),
                "description": "Sessão noturna especial de 25 anos do clássico absoluto da fantasia sob a direção de Peter Jackson.",
                "banner_url": "https://image.tmdb.org/t/p/w500/mWDdRXTivGE7aaY2vo1Ie0PfCX5.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/tlvsNCwWEIgwAM23aNzTmMIcPEZ.jpg",
                "location_name": "Cine Odeon - Praça Floriano",
                "cep": "20031-040",
                "address": "Rua Evaristo da Veiga",
                "number": "7",
                "neighborhood": "Centro",
                "city": "Rio de Janeiro",
                "city_slug": "rio-de-janeiro",
                "state": "RJ",
                "maps_url": "https://maps.google.com/?q=Cine+Odeon+Praca+Floriano+7+Rio+de+Janeiro",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 16, 37, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 8, 28, 22, 16, 0, tzinfo=timezone.utc),
            },
            {
                "title": "Interestelar",
                "available_tickets": 100,
                "ticket_price": Decimal("30.00"),
                "service_fee": Decimal("3.30"),
                "event_date": datetime(2026, 8, 30, 22, 17, 0, tzinfo=timezone.utc),
                "description": "Imersão nas profundezas do espaço e do tempo. Sessão especial com projeção de alta qualidade sonora e visual.",
                "banner_url": "https://image.tmdb.org/t/p/w500/vgnoBSVzWAV9sNQUORaDGvDp7wx.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/6ricSDD83BClJsFdGB6x7cM0MFQ.jpg",
                "location_name": "Cine Theatro Brasil - Av Amazonas",
                "cep": "30130-010",
                "address": "Praça Sete de Setembro",
                "number": "315",
                "neighborhood": "Centro",
                "city": "Belo Horizonte",
                "city_slug": "belo-horizonte",
                "state": "MG",
                "maps_url": "https://maps.google.com/?q=Cine+Theatro+Brasil+Av+Amazonas+315+Belo+Horizonte",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 17, 18, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 8, 30, 22, 17, 0, tzinfo=timezone.utc),
            },
            {
                "title": "A Noite do Horror",
                "available_tickets": 39,
                "ticket_price": Decimal("22.00"),
                "service_fee": Decimal("2.82"),
                "event_date": datetime(2026, 9, 4, 22, 17, 0, tzinfo=timezone.utc),
                "description": "Exibição de clássicos do horror moderno seguida de debate com críticos de cinema e cineastas locais.",
                "banner_url": "https://image.tmdb.org/t/p/w500/3yrMRWb0XE8oUiQdzjhGKChQcpi.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/viKVTov33TtO2BOSSN9nkAQJlJR.jpg",
                "location_name": "Cine Passeio - R Riachuelo",
                "cep": "80020-030",
                "address": "Travessa Oliveira Bello",
                "number": "410",
                "neighborhood": "Centro",
                "city": "Curitiba",
                "city_slug": "curitiba",
                "state": "PR",
                "maps_url": "https://maps.google.com/?q=Cine+Passeio+Rua+Riachuelo+410+Curitiba",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 18, 2, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 9, 4, 22, 17, 0, tzinfo=timezone.utc),
            },
            {
                "title": "Cyberpunk: Mercenários",
                "available_tickets": 59,
                "ticket_price": Decimal("35.00"),
                "service_fee": Decimal("3.60"),
                "event_date": datetime(2026, 9, 5, 22, 18, 0, tzinfo=timezone.utc),
                "description": "Show ao vivo performando as trilhas sonoras mais marcantes do cinema sci-fi e dos games cyberpunk.",
                "banner_url": "https://image.tmdb.org/t/p/w500/bRE6zX4iOAejLOQCHryoV5WNu8G.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/nWvAY8yHE873adMws83XqBPf7W2.jpg",
                "location_name": "Espaço Cultural Barroquinha - R das Mouras",
                "cep": "40026-280",
                "address": "Largo do Pelourinho",
                "number": "1",
                "neighborhood": "Centro Histórico",
                "city": "Salvador",
                "city_slug": "salvador",
                "state": "BA",
                "maps_url": "https://maps.google.com/?q=Espaco+Cultural+Barroquinha+Rua+das+Mouras+Salvador",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 19, 3, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 9, 5, 22, 18, 0, tzinfo=timezone.utc),
            },
            {
                "title": "Festival Studio Ghibli: A Viagem de Chihiro",
                "available_tickets": 45,
                "ticket_price": Decimal("12.00"),
                "service_fee": Decimal("2.22"),
                "event_date": datetime(2026, 9, 10, 22, 19, 0, tzinfo=timezone.utc),
                "description": "Abertura da semana cultural dedicada ao lendário Studio Ghibli, com exibição dublada e legendada.",
                "banner_url": "https://image.tmdb.org/t/p/w500/dyJvKsNs2KP8qQnAXbRwDjblViy.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/hhoKhsyJ3hFaxEm5pMdZRiTu2lJ.jpg",
                "location_name": "Casa de Cultura Mario Quintana - R dos Andradas",
                "cep": "90010-190",
                "address": "Rua Sete de Setembro",
                "number": "736",
                "neighborhood": "Centro Histórico",
                "city": "Porto Alegre",
                "city_slug": "porto-alegre",
                "state": "RS",
                "maps_url": "https://maps.google.com/?q=Casa+de+Cultura+Mario+Quintana+Rua+dos+Andradas+736+Porto+Alegre",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 19, 53, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 9, 10, 22, 19, 0, tzinfo=timezone.utc),
            },
            {
                "title": "Batman: O Cavaleiro das Trevas",
                "available_tickets": 70,
                "ticket_price": Decimal("16.00"),
                "service_fee": Decimal("2.46"),
                "event_date": datetime(2026, 9, 12, 22, 20, 0, tzinfo=timezone.utc),
                "description": "Reexibição da obra-prima dos filmes de herói em celebração à atuação inesquecível de Heath Ledger.",
                "banner_url": "https://image.tmdb.org/t/p/w500/9FE5eD92WfVCiivM9Pq9GVSrlWk.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/4lj1ikfsSmMZNyfdi8R8Tv5tsgb.jpg",
                "location_name": "Cine Brasília - EQS 106/107",
                "cep": "70070-200",
                "address": "Setor SCTN",
                "number": "106",
                "neighborhood": "Zona Cívico-Administrativa",
                "city": "Brasília",
                "city_slug": "brasilia",
                "state": "DF",
                "maps_url": "https://maps.google.com/?q=Cine+Brasilia+EQS+106/107+Brasilia",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 20, 43, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 9, 12, 22, 20, 0, tzinfo=timezone.utc),
            },
            {
                "title": "Spirit: O Corcel Indomável",
                "available_tickets": 23,
                "ticket_price": Decimal("15.00"),
                "service_fee": Decimal("2.40"),
                "event_date": datetime(2026, 8, 24, 2, 50, 0, tzinfo=timezone.utc),
                "description": "No final do século XVII em pleno Oeste norte-americano vive Spirit, um cavalo que resiste a ser domado pelo homem. Ele se apaixona por uma égua local, chamada Chuva, e desenvolve uma grande amizade com um jovem índio Lakota chamado Pequeno Rio.",
                "banner_url": "https://image.tmdb.org/t/p/w500/b8hPBW0NJmiIVzvQjT3CwIpAdzl.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/jycgp5AdZFKj2Qh2VACG9ilK93l.jpg",
                "location_name": "Cine Odeon - Praça Floriano",
                "cep": "01310-100",
                "address": "Avenida Paulista",
                "number": "119",
                "neighborhood": "Bela Vista",
                "city": "São Paulo",
                "city_slug": "sao-paulo",
                "state": "SP",
                "maps_url": "https://maps.google.com/?q=Cine+Odeon+Praca+Floriano+7+Rio+de+Janeiro",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 22, 46, 35, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 8, 24, 2, 50, 0, tzinfo=timezone.utc),
            },
            {
                "title": "Oprah e Viola: Um Evento Especial Netflix",
                "available_tickets": 11,
                "ticket_price": Decimal("25.00"),
                "service_fee": Decimal("3.00"),
                "event_date": datetime(2026, 8, 24, 0, 20, 0, tzinfo=timezone.utc),
                "description": "Neste evento especial, Oprah Winfrey conversa com a atriz Viola Davis sobre seu livro de memórias.",
                "banner_url": "https://image.tmdb.org/t/p/w500/rNmSfJEAYqOuEW90wkVnU8v7IVk.jpg",
                "poster_url": "https://image.tmdb.org/t/p/w500/mL5L97SIV0Zz2Qbc9wgQgSaqjxa.jpg",
                "location_name": "Cinesesc - Av Paulista",
                "cep": "01310-100",
                "address": "Avenida Paulista",
                "number": "119",
                "neighborhood": "Bela Vista",
                "city": "São Paulo",
                "city_slug": "sao-paulo",
                "state": "SP",
                "maps_url": "https://maps.google.com/?q=Cine+Theatro+Brasil+Av+Amazonas+315+Belo+Horizonte",
                "status": EventStatus.ACTIVE,
                "ticket_title": "Ingresso Geral",
                "ticket_description": None,
                "sales_start_at": datetime(2026, 8, 23, 23, 20, 5, tzinfo=timezone.utc),
                "sales_end_at": datetime(2026, 8, 24, 0, 20, 0, tzinfo=timezone.utc),
            },
        ]

        for e in events_data:
            stmt = select(Event).where(Event.title == e["title"])
            res = await session.execute(stmt)
            if not res.scalar_one_or_none():
                event = Event(
                    organizer_id=organizer.id,
                    title=e["title"],
                    description=e["description"],
                    event_date=e["event_date"],
                    available_tickets=e["available_tickets"],
                    ticket_price=e["ticket_price"],
                    service_fee=e["service_fee"],
                    ticket_title=e["ticket_title"],
                    ticket_description=e["ticket_description"],
                    location_name=e["location_name"],
                    cep=e["cep"],
                    address=e["address"],
                    number=e["number"],
                    neighborhood=e["neighborhood"],
                    city=e["city"],
                    city_slug=e["city_slug"],
                    state=e["state"],
                    status=e["status"],
                    poster_url=e["poster_url"],
                    banner_url=e["banner_url"],
                    maps_url=e["maps_url"],
                    sales_start_at=e["sales_start_at"],
                    sales_end_at=e["sales_end_at"],
                )
                session.add(event)
                print(f"🎪 Evento criado: {e['title']}")

        await session.commit()
        print("🚀 Seed concluído com sucesso!")


if __name__ == "__main__":
    asyncio.run(seed_database())
