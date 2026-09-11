# Field Copilot — Landing Page · Roteiro / Storyboard
**Estilo:** scroll-driven à la apple.com — página única, fundo escuro, seções "pinadas" onde o scroll controla a animação (scrub), texto entrando em sincronia com o visual.
**Stack prevista:** HTML único + GSAP ScrollTrigger (CDN) · sequências de frames em `<canvas>` (giro/zoom do produto) · `<model-viewer>` para o 3D interativo real (já temos os GLBs) · vídeos MP4 mudos em loop.
**Fontes de mídia:** renders do Blender (produto — fidelidade total ao modelo) + Krea (cenas humanas/contexto de trabalho e vídeos).

---

## Convenções
- **PIN**: seção fica presa na tela enquanto o scroll "toca" a animação.
- **SCRUB**: progresso do scroll = progresso da animação (frame da sequência, posição, opacidade).
- Sequências de frames: 1920×1080, ~90–120 frames, WebP q80 (peso alvo < 6 MB por sequência).
- Vídeos: 1920×1080, 6–10 s, loop, sem áudio, H.264.

---

## S0 · Hero — "o produto flutua"
**Narrativa:** impacto imediato: o conjunto montado girando devagar no escuro. Logo + nome + uma frase.
**Texto:** "Field Copilot" / "Vê o que o técnico vê. Responde no ouvido. Sem tirar as mãos do trabalho."
**Interação:** produto em giro automático lento; ao primeiro scroll, o giro passa a ser controlado (SCRUB da sequência 360°) e a câmera aproxima. Indicador "role para explorar".
**Assets:**
- `seq_hero_360` — sequência 120 frames, headset montado v3 girando 360° (Blender, fundo #101114, luz de estúdio) — **Blender**
- `img_logo_fieldcopilot` — wordmark simples (tipografia, sem gerar)

## S1 · O problema — mãos ocupadas
**Narrativa:** técnico industrial com as duas mãos dentro de um painel; ninguém segura celular/rádio/manual.
**Texto (3 blocos que entram em fade conforme o scroll):** "As duas mãos no trabalho." / "A informação no ouvido." / "O registro acontece sozinho."
**Interação:** vídeo full-bleed em autoplay-loop; blocos de texto sobem com parallax leve; vinheta escurece nas trocas de bloco.
**Assets:**
- `vid_tecnico_painel` — vídeo 8 s: técnico de uniforme azul e capacete branco trabalhando num painel elétrico industrial, ambas as mãos ocupadas, headset discreto na cabeça — **Krea video** (imagem-referência: nosso render do conjunto vestido)
- `img_tecnico_still` — still 4K do mesmo contexto (fallback mobile) — **Krea image**

## S2 · Apresentação do conjunto — giro com callouts
**Narrativa:** o headset por inteiro; nomes das partes aparecem apontando.
**Interação:** PIN + SCRUB de giro 360° (sequência); em ângulos-chave, callouts com traço fino: "Módulo câmera" (30°), "Fita de 3 pontos" (90°), "Módulo bateria" (150°), "Fone + microfone" (210°). Callout ativo acompanha 20% do scroll cada.
**Assets:**
- `seq_conjunto_360` — 120 frames do headset_montado_v3 (sem manequim), leve órbita descendente — **Blender**

## S3 · Módulo câmera — o olho
**Narrativa:** zoom na gota da câmera; specs entram como "chips".
**Texto:** "5 MP · autofoco · ~75° de campo" / "Aponta para onde o técnico olha." / "Botão de gravar ao alcance do polegar."
**Interação:** PIN; SCRUB de zoom-in (sequência de aproximação frontal→macro da lente); chips de spec surgem escalonados; ao final, corte para o 3D interativo (model-viewer do módulo, o usuário pode girar livremente — "experimente arrastar").
**Assets:**
- `seq_camera_zoom` — 90 frames: do módulo inteiro ao close da lente — **Blender**
- `mv_modulo_camera` — model-viewer com `novo_modulo_camera_v3.glb` (já existe)

## S4 · Módulo bateria — um turno inteiro
**Narrativa:** energia e luz; a lanterna acende em cena escura.
**Texto:** "Célula 21700 · 5000 mAh · ~9 h" / "Troca sem ferramenta." / "Luz onde a lente precisa — 15 cm fora do eixo, sem reflexo."
**Interação:** PIN; primeira metade do scroll: giro do módulo (sequência); na metade: o fundo escurece e a **lanterna acende** (2 renders cross-fade: LED off→on com glow); chips de spec.
**Assets:**
- `seq_bateria_giro` — 90 frames — **Blender**
- `img_lanterna_off` / `img_lanterna_on` — par para o cross-fade do LED (composição com glow) — **Blender**
- `img_troca_celula` — mão trocando célula 21700 num berço (conceito) — **Krea image**

## S5 · Fone + microfone — uma peça só
**Narrativa:** a peça integrada; o plug entra no jack.
**Texto:** "Gancho, fone e microfone numa peça." / "Um único plug P3." / "Sem cabo pendurado."
**Interação:** PIN + SCRUB de **animação de encaixe**: a peça sobe e o plug P3 desliza para dentro do boss do módulo (sequência renderizada com a peça em 2 posições interpoladas); depois, órbita curta ao redor do gancho na orelha.
**Assets:**
- `seq_fone_encaixe` — 90 frames: peça solta → plug encaixado sob o módulo — **Blender**
- `img_fone_orelha` — pessoa de perfil com o fone no ouvido e mic na boca (contexto humano) — **Krea image** (ref: asm3_lado_dir)

## S6 · Ergonomia — veste com EPI
**Narrativa:** fita de 3 pontos, berços e presilhas; cabe com capacete.
**Texto:** "Fita elástica, três pontos de apoio." / "Passa por baixo do capacete." / "132 g na cabeça — o computador fica no pulso."
**Interação:** split-screen com parallax: esquerda, foto de pessoa vestindo com capacete; direita, render explodido leve (módulos afastados da fita 15 mm) montando conforme o scroll (SCRUB da sequência de montagem).
**Assets:**
- `img_capacete` — trabalhador com capacete branco + headset visível sob a aba (como ref-frente do produto) — **Krea image**
- `seq_montagem_explodida` — 60 frames: berços/presilhas/módulos convergindo na fita — **Blender**

## S7 · Relógio — a interface no pulso
**Narrativa:** o segundo herói; display grande atravessando o punho.
**Texto:** "Android no pulso · 2,8\" legível de relance" / "Bom dia, Carlos." / "Copiloto, nova tarefa, chamado — a um toque."
**Interação:** PIN; o relógio entra girando (sequência); para na tela frontal e os **cards da UI ganham vida** (recriados em HTML sobre o render: saudação, card OS 3798, chips), animando como se a tela ligasse; depois foto humana de pulso erguido.
**Assets:**
- `seq_relogio_giro` — 90 frames do relogio.glb — **Blender**
- `img_relogio_pulso_real` — antebraço de trabalhador com luva parcial e o relógio, painel desfocado ao fundo — **Krea image** (ref: rel_pulso + ref relogio.jpg)

## S8 · O sistema completo — cena real
**Narrativa:** tudo junto em campo: técnico olha o manômetro, pergunta em voz alta, resposta aparece no pulso.
**Interação:** vídeo full-bleed (autoplay loop); legendas-diálogo aparecem sincronizadas por tempo (não scroll): "— Copiloto, registra a leitura." / toast na tela do relógio "Leitura registrada · OS 3798". Ao final, fade para fundo escuro.
**Assets:**
- `vid_cena_completa` — vídeo 10 s: técnico em casa de máquinas, headset + relógio visíveis, fala e consulta o pulso — **Krea video**
- `img_ui_toast` — recorte da UI para overlay (HTML/CSS, não gerar)

## S9 · Especificações — a ficha
**Narrativa:** rigor técnico; tabela sóbria em duas colunas (Cabeça / Pulso) com os números reais.
**Conteúdo:** dimensões dos módulos (121×38,7×44,4), câmera OV5640 5MP, célula 21700 5000mAh ~9h, IP67 do relógio, 2,8" 480×640, pesos, jack P3 único, USB-C. (Fonte: ficha do projeto + nossas medidas.)
**Interação:** entrada simples por fade-up em cascata; sem PIN. Link "ver o modelo 3D completo" → nosso visualizador Pages.
**Assets:** nenhum novo (ícones de linha em SVG inline).

## S10 · Encerramento / CTA
**Narrativa:** produto de perfil no escuro, logo, contato.
**Texto:** "Field Copilot — BravoLabs · Loja Interativa" + botão "Ver no 3D" (visualizador) + contato.
**Assets:**
- `img_final_perfil` — render hero lateral do conjunto no manequim, luz dramática — **Blender**

---

## Resumo de produção de mídia
| # | Asset | Tipo | Ferramenta | Frames/duração |
|---|---|---|---|---|
| 1 | seq_hero_360 | sequência | Blender | 120 |
| 2 | seq_conjunto_360 | sequência | Blender | 120 |
| 3 | seq_camera_zoom | sequência | Blender | 90 |
| 4 | seq_bateria_giro | sequência | Blender | 90 |
| 5 | img_lanterna_off/on | 2 stills | Blender | — |
| 6 | seq_fone_encaixe | sequência | Blender | 90 |
| 7 | seq_montagem_explodida | sequência | Blender | 60 |
| 8 | seq_relogio_giro | sequência | Blender | 90 |
| 9 | img_final_perfil | still | Blender | — |
| 10 | vid_tecnico_painel | vídeo 8s | Krea | — |
| 11 | img_tecnico_still | still | Krea | — |
| 12 | img_troca_celula | still | Krea | — |
| 13 | img_fone_orelha | still | Krea | — |
| 14 | img_capacete | still | Krea | — |
| 15 | img_relogio_pulso_real | still | Krea | — |
| 16 | vid_cena_completa | vídeo 10s | Krea | — |

**Ordem de execução sugerida:** (1) aprovar este roteiro → (2) esqueleto HTML com placeholders cinza e todas as interações de scroll funcionando → (3) renders Blender (sequências) → (4) mídias Krea → (5) montagem final + publicação (mesmo padrão do visualizador: GitHub Pages).
