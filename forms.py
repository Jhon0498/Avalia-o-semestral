
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class FormularioAluno(FlaskForm):

    # Nome do usuário
    usuario = StringField(
        'Qual é o seu nome?:',
        validators=[DataRequired()]
    )

    # E-mail para envio de notificação do novo usuário
    email = StringField(
        'Qual é o seu email (Envio de notificação do novo usuário)?',
        validators=[DataRequired(), Email()],
        render_kw={
            'placeholder': 'Digite seu e-mail'
        }
    )

    # Prontuário do usuário
    prontuario = StringField(
        'Qual é o seu prontuário?:',
        validators=[DataRequired()],
        default='PT3026931'
    )

    # Checkbox para escolher se deseja enviar e-mail
    enviar_email = BooleanField(
        'Deseja enviar e-mail para flaskaulasweb@zohomail.com?'
    )

    # Botão que envia o formulário
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    # Campo de e-mail
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={
            'placeholder': 'Email'
        }
    )

    # Campo de senha
    senha = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'Password',
        }
    )

    # Opção para manter o usuário conectado
    remember_me = BooleanField('Keep me logged in')

    # Botão de envio
    submit = SubmitField('Log In')


# Formulário utilizado para cadastrar novos cursos.
class FormularioCurso(FlaskForm):

    # Campo obrigatório para informar o nome do curso.
    nome = StringField(
        'Qual é o nome do curso?',
        validators=[DataRequired(), Length(max=120)]
    )

    # Campo opcional para descrever o curso, limitado a 250 caracteres.
    descricao = TextAreaField(
        'Descrição (250 caracteres)',
        validators=[Length(max=250)]
    )

    # Botão para enviar o formulário.
    submit = SubmitField('Cadastrar')
