from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.core.models import Igreja, Campus, Papel, Permissao, PapelPermissao, UsuarioPapel
from apps.financial.models import Categoria, CentroCusto, ContaBancaria

User = get_user_model()


class Command(BaseCommand):
    help = 'Configura dados iniciais para uma nova igreja'

    def add_arguments(self, parser):
        parser.add_argument('--igreja-nome', type=str, required=True, help='Nome da igreja')
        parser.add_argument('--admin-email', type=str, required=True, help='Email do administrador')
        parser.add_argument('--admin-password', type=str, required=True, help='Senha do administrador')

    def handle(self, *args, **options):
        igreja_nome = options['igreja_nome']
        admin_email = options['admin_email']
        admin_password = options['admin_password']

        self.stdout.write(f'Configurando dados iniciais para: {igreja_nome}')

        igreja, created = Igreja.objects.get_or_create(
            nome=igreja_nome,
            defaults={
                'plano': 'basico',
                'limite_membros': 100,
                'limite_mensagens': 1000,
                'ativa': True
            }
        )

        if created:
            self.stdout.write(f'Igreja "{igreja_nome}" criada com sucesso!')
        else:
            self.stdout.write(f'Igreja "{igreja_nome}" já existe.')

        campus_matriz, created = Campus.objects.get_or_create(
            igreja=igreja,
            nome='Matriz',
            defaults={
                'nivel': 'matriz',
                'endereco': '',
                'telefone': '',
                'email': ''
            }
        )

        if created:
            self.stdout.write('Campus Matriz criado!')

        admin_user, created = User.objects.get_or_create(
            username=admin_email,
            email=admin_email,
            defaults={
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'igreja': igreja,
                'campus': campus_matriz,
                'nivel_acesso': 'matriz',
                'is_staff': True,
                'is_superuser': True,
                'aceite_termos': True,
                'aceite_lgpd': True
            }
        )

        if created:
            admin_user.set_password(admin_password)
            admin_user.save()
            self.stdout.write('Usuário administrador criado!')
        else:
            self.stdout.write('Usuário administrador já existe.')

        papel_admin, created = Papel.objects.get_or_create(
            igreja=igreja,
            nome='Administrador Geral',
            defaults={
                'descricao': 'Acesso completo ao sistema',
                'nivel_minimo': 'matriz'
            }
        )

        if created:
            self.stdout.write('Papel de Administrador criado!')

        permissoes = Permissao.objects.all()
        for permissao in permissoes:
            PapelPermissao.objects.get_or_create(
                papel=papel_admin,
                permissao=permissao,
                defaults={
                    'pode_ler': True,
                    'pode_criar': True,
                    'pode_editar': True,
                    'pode_excluir': True,
                    'pode_aprovar': True
                }
            )

        UsuarioPapel.objects.get_or_create(
            usuario=admin_user,
            papel=papel_admin,
            campus=campus_matriz,
            defaults={
                'data_inicio': timezone.now().date()
            }
        )

        categorias_entrada = [
            ('Dízimos', 'Dízimos dos membros'),
            ('Ofertas', 'Ofertas diversas'),
            ('Campanhas', 'Campanhas especiais'),
            ('Doações', 'Doações gerais'),
        ]

        for nome, descricao in categorias_entrada:
            Categoria.objects.get_or_create(
                igreja=igreja,
                nome=nome,
                defaults={
                    'descricao': descricao,
                    'tipo': 'entrada',
                    'cor': '#28a745'
                }
            )

        categorias_saida = [
            ('Salários', 'Salários e encargos'),
            ('Manutenção', 'Manutenção predial'),
            ('Utilities', 'Água, luz, telefone'),
            ('Material', 'Material de escritório e limpeza'),
            ('Eventos', 'Gastos com eventos'),
        ]

        for nome, descricao in categorias_saida:
            Categoria.objects.get_or_create(
                igreja=igreja,
                nome=nome,
                defaults={
                    'descricao': descricao,
                    'tipo': 'saida',
                    'cor': '#dc3545'
                }
            )

        CentroCusto.objects.get_or_create(
            igreja=igreja,
            nome='Geral',
            defaults={
                'descricao': 'Centro de custo geral',
                'codigo': '001',
                'campus': campus_matriz
            }
        )

        ContaBancaria.objects.get_or_create(
            igreja=igreja,
            nome='Conta Principal',
            defaults={
                'banco': 'Banco do Brasil',
                'agencia': '0000',
                'conta': '00000-0',
                'tipo_conta': 'corrente',
                'saldo_inicial': 0,
                'ativa': True
            }
        )

        self.stdout.write(
            self.style.SUCCESS(f'Configuração inicial concluída para {igreja_nome}!')
        )
        self.stdout.write(f'Login: {admin_email}')
        self.stdout.write(f'Senha: {admin_password}')
