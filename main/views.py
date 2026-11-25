
# Importa as funções necessárias do Flask.
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    current_app
)

# Importa o recurso para exigir que o usuário esteja autenticado.
from flask_login import login_required

# Importa recursos para trabalhar com datas.
from datetime import datetime
from zoneinfo import ZoneInfo

# Importa o formulário de cadastro.
from forms import FormularioAluno

# Importa os modelos da aplicação.
from app.models import User, Role, EmailEnviado

# Importa a instância compartilhada do banco de dados.
from app.extensions import db

# Importa o serviço de envio de e-mails.
from services.email_service import enviar_email_mailgun

# Importa o Blueprint principal.
from main import main


# Página inicial da aplicação.
@main.route('/')
def index():
    return redirect(url_for('main.avaliacao_semestral'))






# Página da avaliação semestral.
@main.route('/avaliacao-semestral')
def avaliacao_semestral():
    # Obtém a data e a hora atual de São Paulo.
    data_hora = datetime.now(ZoneInfo('America/Sao_Paulo'))

    # Exibe os dados do aluno na página de avaliação.
    return render_template(
        'avaliacao_semestral.html',
        aluno='Jhonatan Mendes',
        prontuario='PT3026931',
        data_hora=data_hora
    )

# Rota para cadastrar e listar usuários.
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    # Cria uma instância do formulário.
    form = FormularioAluno()

    # Busca todos os usuários cadastrados.
    usuarios_banco = User.query.all()

    # Verifica se o formulário foi enviado.
    if request.method == 'POST':

        # Valida os campos preenchidos.
        if not form.validate():
            return render_template(
                'index.html',
                form=form,
                nome='',
                mensagem='Verifique os campos preenchidos.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Obtém o nome informado no formulário.
        nome = (
            form.usuario.data.strip()
            if form.usuario.data
            else ''
        )

        # Obtém o e-mail informado no formulário.
        email_informado = (
            form.email.data.strip()
            if form.email.data
            else ''
        )

        # Cria o username a partir do nome.
        username = nome.lower().replace(' ', '')

        # Verifica se o usuário já está cadastrado.
        usuario_existente = User.query.filter(
            User.username.ilike(username)
        ).first()

        if usuario_existente:
            return render_template(
                'index.html',
                form=form,
                nome=usuario_existente.name,
                mensagem='Este usuário já está cadastrado.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Busca a função padrão dos usuários.
        funcao_user = Role.query.filter_by(
            name='User'
        ).first()

        # Verifica se a função padrão existe.
        if not funcao_user:
            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Erro: a função User não foi encontrada no banco.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Cria um novo usuário.
        novo_usuario = User(
            username=username,
            name=nome,
            email=email_informado,
            role=funcao_user
        )

        try:
            # Adiciona o usuário ao banco de dados.
            db.session.add(novo_usuario)

            # Salva as alterações.
            db.session.commit()

        except Exception:

            # Desfaz as alterações em caso de erro.
            db.session.rollback()

            # Registra o erro no terminal.
            current_app.logger.exception(
                'Erro ao cadastrar usuário.'
            )

            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Erro ao cadastrar o usuário.',
                users=User.query.all(),
                current_time=datetime.utcnow()
            )

        # Atualiza a relação de usuários.
        usuarios_banco = User.query.all()

        # Envia a notificação por e-mail.
        sucesso_email, resultado_email = enviar_email_mailgun(
            username=username,
            nome=nome,
            email_informado=email_informado
        )

        # Verifica se o envio foi realizado.
        if sucesso_email:

            try:
                # Registra o e-mail enviado no banco de dados.
                novo_email = EmailEnviado(
                    username=username,
                    nome=nome,
                    prontuario='PT3026931',
                    destinatario=', '.join(
                        resultado_email['destinatarios']
                    ),
                    assunto=resultado_email['assunto'],
                    status='Enviado'
                )

                # Adiciona o registro.
                db.session.add(novo_email)

                # Salva o registro.
                db.session.commit()

            except Exception:

                # Desfaz as alterações em caso de erro.
                db.session.rollback()

                # Registra o erro no terminal.
                current_app.logger.exception(
                    'Erro ao registrar o e-mail no banco.'
                )

            return render_template(
                'index.html',
                form=form,
                nome=nome,
                mensagem='Usuário cadastrado e notificação aceita pelo Mailgun.',
                users=usuarios_banco,
                current_time=datetime.utcnow()
            )

        # Informa que o usuário foi cadastrado,
        # mas que houve um problema no envio do e-mail.
        return render_template(
            'index.html',
            form=form,
            nome=nome,
            mensagem=(
                'Usuário cadastrado, mas não foi possível enviar o e-mail: '
                f'{resultado_email}'
            ),
            users=usuarios_banco,
            current_time=datetime.utcnow()
        )

    # Exibe a página de cadastro.
    return render_template(
        'index.html',
        form=form,
        users=usuarios_banco,
        current_time=datetime.utcnow()
    )


# Rota para visualizar os e-mails enviados.
@main.route('/emails-enviados')
def emails_enviados():

    # Busca os e-mails enviados, ordenando pelos mais recentes.
    emails = EmailEnviado.query.order_by(
        EmailEnviado.data_envio.desc()
    ).all()

    # Exibe a página de e-mails enviados.
    return render_template(
        'emails_enviados.html',
        emails=emails
    )


# Rota para visualizar todos os usuários cadastrados.
@main.route('/usuarios')
@login_required
def usuarios():

    # Busca todos os usuários, sem filtrar pela confirmação do e-mail.
    usuarios_banco = User.query.order_by(
        User.name.asc()
    ).all()

    # Exibe a página com a relação de usuários.
    return render_template(
        'usuarios.html',
        usuarios=usuarios_banco
    )

# Importa os recursos necessários para cadastrar cursos.
from flask import flash, redirect, url_for
from forms import FormularioCurso
from app.models import Curso

# Rota responsável por cadastrar e listar os cursos.
@main.route('/cursos', methods=['GET', 'POST'])
def cursos():
    # Cria o formulário de cadastro.
    form = FormularioCurso()

    # Verifica se o formulário foi enviado e preenchido corretamente.
    if form.validate_on_submit():

        # Cria um novo registro com os dados informados.
        novo_curso = Curso(
            nome=form.nome.data.strip(),
            descricao=form.descricao.data.strip() if form.descricao.data else ''
        )

        try:
            # Salva o curso no banco de dados.
            db.session.add(novo_curso)
            db.session.commit()
            flash('Curso cadastrado com sucesso!')
            return redirect(url_for('main.cursos'))

        except Exception:
            # Desfaz a operação caso ocorra algum erro.
            db.session.rollback()
            current_app.logger.exception('Erro ao cadastrar curso.')
            flash('Não foi possível cadastrar o curso.')

    # Busca os cursos cadastrados para exibi-los na página.
    cursos_banco = Curso.query.order_by(Curso.nome.asc()).all()

    # Exibe o formulário e a relação de cursos.
    return render_template(
        'cursos.html',
        form=form,
        cursos=cursos_banco,
        current_time=datetime.now()
    )


# Rota para os módulos que ainda não estão disponíveis.
@main.route('/<modulo>')
def indisponivel(modulo):
    # Define os módulos que podem apresentar a mensagem.
    modulos = {
        'professores': 'Cadastro de professores',
        'disciplinas': 'Cadastro de Disciplinas',
        'alunos': 'Cadastro de alunos',
        'ocorrencias': 'Cadastro de ocorrências'
    }

    # Verifica se o módulo solicitado está na lista permitida.
    if modulo not in modulos:
        return 'Página não encontrada.', 404

    # Exibe a página informando que o módulo não está disponível.
    return render_template(
        'indisponivel.html',
        nome_modulo=modulos[modulo]
    )
