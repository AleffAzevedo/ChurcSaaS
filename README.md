# Igreja SaaS - Sistema de Gestão para Igrejas

Sistema SaaS completo para gestão de igrejas com recursos de multitenancy, hierarquia organizacional, gestão de membros, eventos, finanças e comunicação.

## Funcionalidades Principais

### MVP (Fase 1)
- ✅ Cadastro de membros, famílias, visitantes e líderes
- ✅ Hierarquia multi-nível (Matriz → Setorial → Congregação)
- ✅ Gestão de grupos e células
- ✅ Agenda e eventos
- ✅ Controle de presenças
- ✅ Financeiro básico (entradas e saídas)
- ✅ Sistema de comunicação
- ✅ Relatórios e dashboards

### Recursos Avançados
- Sistema de permissões granulares (RBAC)
- Multitenancy seguro com isolamento por tenant
- Pipeline de novos membros
- Gestão pastoral e discipulado
- Integração com WhatsApp e Email
- Conformidade com LGPD

## Tecnologias

### Backend
- Django 4.2+ com Django REST Framework
- PostgreSQL (com suporte a multitenancy)
- Celery + Redis (filas e webhooks)
- JWT Authentication

### Frontend
- React 18+ com Next.js 14
- TypeScript
- Tailwind CSS
- Shadcn/UI Components

## Estrutura do Projeto

```
ChurcSaaS/
├── backend/                 # Django API
│   ├── igreja_saas/        # Projeto principal
│   ├── apps/               # Apps Django
│   │   ├── core/          # Modelos base e multitenancy
│   │   ├── members/       # Gestão de membros
│   │   ├── groups/        # Grupos e células
│   │   ├── events/        # Eventos e agenda
│   │   ├── financial/     # Gestão financeira
│   │   ├── communication/ # Sistema de comunicação
│   │   └── reports/       # Relatórios e BI
│   ├── requirements.txt
│   └── manage.py
├── frontend/               # React/Next.js
│   ├── src/
│   │   ├── components/    # Componentes reutilizáveis
│   │   ├── pages/         # Páginas da aplicação
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API services
│   │   └── utils/         # Utilitários
│   ├── package.json
│   └── next.config.js
└── docker-compose.yml      # Ambiente de desenvolvimento
```

## Configuração do Ambiente

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis (para filas)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup (Recomendado)
```bash
docker-compose up -d
```

## Configuração

### Variáveis de Ambiente

#### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/igreja_saas
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
WHATSAPP_API_TOKEN=your-whatsapp-token
```

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Igreja SaaS
```

## Arquitetura

### Multitenancy
- Cada igreja é um tenant isolado
- Row-level security com `tenant_id`
- Hierarquia organizacional: Matriz → Setorial → Congregação
- Permissões baseadas em escopo (`org_level` e `scope_id`)

### Autenticação e Autorização
- JWT tokens para autenticação
- Sistema RBAC com papéis personalizáveis
- Permissões granulares por recurso e ação
- Segregação por nível organizacional

### Modelos Principais
- **Igreja**: Tenant principal
- **Pessoa**: Membros, visitantes, líderes
- **Família**: Agrupamento familiar
- **Ministério**: Departamentos da igreja
- **Grupo**: Células e grupos pequenos
- **Evento**: Cultos, reuniões, atividades
- **Presença**: Controle de frequência
- **LançamentoFinanceiro**: Entradas e saídas

## API Endpoints

### Autenticação
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/refresh/` - Refresh token

### Membros
- `GET /api/members/` - Listar membros
- `POST /api/members/` - Criar membro
- `GET /api/members/{id}/` - Detalhes do membro
- `PUT /api/members/{id}/` - Atualizar membro

### Grupos
- `GET /api/groups/` - Listar grupos
- `POST /api/groups/` - Criar grupo
- `GET /api/groups/{id}/meetings/` - Reuniões do grupo

### Eventos
- `GET /api/events/` - Listar eventos
- `POST /api/events/` - Criar evento
- `POST /api/events/{id}/checkin/` - Check-in no evento

### Financeiro
- `GET /api/financial/transactions/` - Transações
- `POST /api/financial/transactions/` - Nova transação
- `GET /api/financial/reports/` - Relatórios financeiros

## Segurança

### Implementações de Segurança
- HTTPS obrigatório em produção
- Rate limiting nas APIs
- Validação e sanitização de inputs
- Proteção contra CSRF, XSS e SQL Injection
- Criptografia de dados sensíveis
- Logs de auditoria completos

### LGPD Compliance
- Consentimento explícito para coleta de dados
- Portabilidade de dados
- Direito ao esquecimento (soft delete)
- Logs de acesso e exportação
- Bases legais documentadas

## Testes

### Backend
```bash
cd backend
python manage.py test
```

### Frontend
```bash
cd frontend
npm test
```

## Deploy

### Produção
- Backend: Django + Gunicorn + Nginx
- Frontend: Next.js (SSG/SSR)
- Banco: PostgreSQL com backup automático
- Cache: Redis
- Monitoramento: Logs estruturados + métricas

### Ambiente de Desenvolvimento
```bash
docker-compose up -d
```

## Roadmap

### Fase 1 (MVP) ✅
- Gestão básica de membros e famílias
- Hierarquia organizacional
- Grupos e presenças
- Eventos e agenda
- Financeiro básico
- Comunicação por email

### Fase 2 (Em desenvolvimento)
- Escalas de voluntários
- Check-in com QR Code
- Pipeline de novos membros
- Integração com PIX/Boleto
- Dashboards executivos

### Fase 3 (Planejado)
- Portal do membro
- App mobile
- Trilhas de discipulado
- Automações avançadas
- Reserva de recursos

### Fase 4 (Futuro)
- IA para previsões
- Assistente virtual
- Análise de engajamento
- Detecção de risco de evasão

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Suporte

Para suporte técnico ou dúvidas sobre o sistema:
- Email: suporte@igrejasaas.com.br
- Documentação: [docs.igrejasaas.com.br](https://docs.igrejasaas.com.br)
- Issues: [GitHub Issues](https://github.com/AleffAzevedo/ChurcSaaS/issues)

---

Desenvolvido com ❤️ para a comunidade cristã brasileira.
