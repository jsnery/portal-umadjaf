# Portal Umadjaf

## Descrição

Este é um portal web para o Grupo de Jovens da Igreja UMADJAF. O portal permite a divulgação, interação e comércio dentro da UMADJAF. O projeto é construído com Django e enfatiza a modularidade para facilitar as mudanças.

## Estrutura do Projeto

O projeto é organizado em várias pastas, cada uma responsável por uma parte específica do portal:

- `home`: Responsável pela página inicial (`home.html`). Herda a navbar, footer, head e o carrossel de imagens do template global.
- `cart`: Responsável pela Loja Online. Gera `store.html` (Página dos produtos) e `product.html` (Página do produto escolhido). Herda a navbar, footer, head e o carrossel de imagens do template global.
- `profiles`: Responsável pela página de perfil, login e cadastro do usuário. Gera `profile.html`, `login.html` e `register.html`. Herda a navbar, footer, head e o carrossel de imagens do template global.
- `articles`: (Ainda não aplicada) Será responsável pelos artigos postados.
- `resources`: Pasta responsável pelos statics e templates globais, por exemplo `navbar.html`, `head.html`, `carousel.html` e `footer.html`.
- `utils`: No momento, referente a gerar teste fakes, gerar os produtos e dados do perfil randomicamente.

## Licença

(Adicione informações sobre a licença aqui)