# Rolador de Dados D&D

Aplicação cliente-servidor simples com Flask que expõe uma API REST para rolar dados no formato clássico do Dungeons & Dragons e uma interface web em HTML/CSS/JS para consumir a API.

## Como executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicie o servidor:
   ```bash
   python app.py
   ```
3. Acesse `http://localhost:8000` para usar a interface. A API responde em `POST /api/roll` com um corpo JSON contendo a chave `expression`.

4. (Opcional) Rode os testes automatizados:
   ```bash
   pytest
   ```

## Formato das rolagens

- **Simples:** `9d4-4` (`N` dados com `M` lados e modificador opcional).
- **Manter maiores:** `4d6kh3` (mantém os 3 maiores resultados).
- **Manter menores:** `2d20kl1` (mantém o menor resultado, útil para desvantagem).

Observações:
- A quantidade mantida (`kh` ou `kl`) deve ser positiva e não pode exceder a quantidade de dados lançados.
- O retorno inclui os valores individuais, os dados mantidos, o modificador aplicado e o total.
