## Área de Login e Cadastro

### Cadastro
Área responsável pelo cadastro dos usuários, podendo se cadastrar quem é ou não da Umadjaf da mesma forma que seja ou não da Adjaf.

Para realizar o cadastro, o usuário deve informar os seguintes dados:
- Nome
- Data de Nascimento
- Número de Telefone
- Congregação (Disponível a opção “Outras” para não membros)
- Indicação se pertence ou não à Umadjaf
- Senha

### Login
Área responsável pelo login dos usuários. Usuários com permissões especiais não necessitam de login secundário, um login pra tudo.

Para realizar o login, o usuário deve informar:
- Número de Telefone
- Senha

**Obs:** Em breve implementação de sistema de recuperação de senha.

## Perfil

### Meu Perfil
Todos os usuários cadastrados possuem perfil, seja membro ou não. Membros da UMADJAF têm a aba de galeria no perfil no qual exibe fotos dos eventos nas quais o usuário solicitou a marcação. Não membros só terão a aba devocionais que mostrará os devocionais escritos e aprovados.

Usuários com a permissão "Coordinator" ou "Admin" terão uma aba extra chamada membros, ela vai exibir os membros da Umadjaf que fazem parte da sua congregação. Usuários com a permissão "Admin" terão um botão no lado esquerdo do menu responsável por abrir o painel de administração.

Todos os usuários têm a aba de ajustes para troca de foto, telefone, nome, congregação, senha e biografia.

**Abas encontradas no perfil:**
- Devocionais
- Galeria (Só para UMADJAF)
- Membros (Só para Coordenador e Adm)
- Ajustes
- Adm (Só para Adm)

### Outro Perfil
Perfis de outros usuários possuem basicamente a mesma ideia. Membros possuem as abas Devocionais e Galeria visíveis a todos, não membros não possuem a aba galeria pois não podem solicitar marcação nas fotos dos eventos.

Usuários com a permissão "Coordinator" ou "Admin" terão um botão no lado direito do menu que mostra o ícone do WhatsApp, sendo clicado, leva direto ao bate-papo com o usuário.

**Abas encontradas no perfil:**
- Devocionais
- Galeria (Só para UMADJAF)
- Whatsapp (Só para Coordenador e Adm)