# Portal Umadjaf

## Sumário
1. [Home](#home)
2. [Carrossel](#carrossel)
3. [Banner](#banner)
4. [Devocionais](#devocionais)
5. [Área de Login e Cadastro](#área-de-login-e-cadastro)
6. [Perfil](#perfil)
7. [Eventos](#eventos)
8. [Galeria](#galeria)
9. [Painel ADM](#painel-adm)

## Home

### Carrossel
Área responsável por mostrar os banners dos eventos, ações e etc.

**Permissões necessárias para manipulação:**
- Admin
- MediaManager

### Banner
Área responsável por mostrar banner referente ao evento geral mais próximo, tendo nele um botão responsável por levar usuário ao calendário de eventos.

**Permissões necessárias para manipulação:**
- Admin
- MediaManager
- Coordinator

**Obs:** Pessoas com a permissão "Coordinator" só conseguirão registrar eventos locais, os quais não irão aparecer na tela inicial.

## Devocionais
Área responsável por exibir os devocionais escritos por membros e não membros da UMADJAF. Serão exibidos somente devocionais verificados.

**Permissões necessárias para manipulação:**
- Admin
- DevotionManager
- Coordinator

**Obs:** Mais detalhes sobre as verificações e publicações ficaram na seção de devocionais.

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

## Devocionais

### Criação de Devocionais
Todos os usuários podem criar devocionais, mas somente membros da Umadjaf terão os mesmos publicados no ato da criação, não membros terão seus devocionais validados primeiro.

**Necessário para criação:**
- Tema
- Referência bíblica
- Texto do devocional
- Banner

### Área de Verificação
Devocionais de membros por mais que sejam publicados no ato eles não recebem o “selo azul”, os mesmos só recebem após validação feita por um "DevotionManager", "Coordinator" ou "Admin".

Devocionais de não membros recebem o “selo azul” após a análise e validação feita por um "DevotionManager" ou "Admin", dessa forma não se faz necessário duas validações.

Somente "DevotionManager" ou "Admin" conseguem remover a validação de um devocional.

**Permissões necessárias para manipulação:**
- Admin
- DevotionManager
- Coordinator

**Obs:** Para coordenador fazer a validação, só basta abrir o devocional de um membro e validar. O acesso ao painel de gerenciamento é restrito a "DevotionManager" e "Admin".

## Eventos

### Adição de eventos
Usuários com a permissão "MediaManager", "Coordinator" ou "Admin" podem adicionar um evento ao calendário, sendo só permitido a adição de eventos gerais para "MediaManager" e "Admin".

Após a adição de um evento, a edição dele, seja correção gramatical ou troca de banner, só pode ser feita também por "MediaManager" e "Admin". Então, caso necessário editar algo, solicite tais.

**Necessário para criação:**
- Título (Nome do evento)
- Tema
- Data
- Horário
- Congregação
- Banner

### Detalhes sobre o banner
O banner é composto por duas partes, sendo o background e a logo. Foi feito dessa forma para melhor transição entre aparelhos de diferentes telas sem distorções.

**Proporções:**
- Logo (Resolução ideal de 960x720)
- Background (Resolução ideal de 2560x720)

## Galeria

### Visualização
Todos os usuários terão acesso à galeria independente de serem membros ou não. Mas somente membros da Umadjaf conseguem solicitar marcação em fotos, dessa forma tais fotos irão aparecer em seu perfil após ser aprovado pela equipe de mídia.

No topo da galeria terá uma barra de filtragem, onde o usuário seleciona o evento, caso o evento não esteja lá basta selecionar os não listados.

O membro poderá remover a foto do próprio perfil na galeria posteriormente caso queira.

### Checagem de marcação
Após o membro solicitar a marcação em uma foto, ele aguardará um "MediaManager" ou "Admin" fazer a checagem da foto, verificando se a pessoa estava ou não na foto, é feito o devido processo de liberação ou remoção da solicitação.

### Adição de foto
A adição de foto só pode ser feita por um "MediaManager" ou "Admin". Por enquanto é necessário ser feita a adição de fotos individualmente. A foto é atrelada ao evento através da lista de eventos já cadastrados, caso o evento não esteja cadastrado, mesmo já tendo passado, é possível criar o evento para tal função ou selecionar a opção não listado e colocar a data do evento. A foto é adicionada na proporção original dela, não requer ajuste.

## Painel ADM

### Funções no painel
Dentro do painel ADM o usuário terá acesso a todos os cadastros, lista de congregações, eventos, devocionais, fotos, gerenciamento das permissões e gerenciamento de todos os membros da Umadjaf.

O usuário será responsável por conferir cadastros fazendo então a checagem dos membros da Umadjaf, dessa forma liberando o acesso dos mesmos às funcionalidades exclusivas. Também será responsável por manter atualizada a lista de congregações, tanto o nome quanto o endereço das mesmas, além disso, poderá e se possível, realizará o restante das funções acima citadas.

**Funções do painel:**
- Gerenciamento de usuários
- Gerenciamento de congregações
- Gerenciamento de membros Umadjaf
- Gerenciamento de permissões da equipe
- Gerenciamento de eventos
- Gerenciamento de devocionais
- Gerenciamento de Marcações (Galeria)

**Obs.:** Tudo que é feito é registrado o id de quem fez, independente da função, isso para mantermos o bom andamento do projeto.
