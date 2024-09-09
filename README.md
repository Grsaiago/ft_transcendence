# ft_transcendence
Transcending in django

## Configuração do Pre-commit

Este projeto utiliza o [pre-commit](https://pre-commit.com/) para garantir a qualidade do código e a conformidade com os padrões estabelecidos. O `pre-commit` é uma ferramenta que executa ganchos (hooks) automaticamente antes de cada commit, garantindo que seu código esteja formatado e lintado de acordo com as regras definidas.

### Ferramentas Configuradas

A configuração atual do `pre-commit` inclui as seguintes ferramentas:

- **[Black](https://black.readthedocs.io/en/stable/)**: Um formatador de código para Python que garante uma formatação consistente do código.
- **[isort](https://pycqa.github.io/isort/)**: Um organizador de imports para Python que mantém os imports ordenados e organizados.
- **[flake8](https://flake8.pycqa.org/)**: Uma ferramenta de linting para Python que verifica a conformidade com o PEP 8 e outros padrões de qualidade.
- **[djlint](https://djlint.readthedocs.io/en/latest/)**: Um linting e formatador para templates Django, garantindo que os arquivos HTML estejam formatados corretamente.

### Instalação e Atualização do Pre-commit

Para garantir que os ganchos do `pre-commit` funcionem corretamente, siga estas etapas:

1. **Instale o pre-commit**:
   Se ainda não tiver o `pre-commit` instalado, você pode instalá-lo usando pip (certifique-se que está fora do ambiente virtual do Poetry):

   ```bash
   pip install pre-commit
   ```

2. **Instale os ganchos definidos**:
Navegue até a raiz do projeto e execute o seguinte comando para instalar os ganchos definidos no arquivo `.pre-commit-config.yaml`:
```bash
pre-commit install
```

### Notas Adicionais

Esses passos farão o `pre-commit` rodar e formatar o seu código automaticamente ao fazer um commit. O `pre-commit` pode falhar e automaticamente fazer as formatações necessárias, mostrando uma mensagem sobre os arquivos que foram alterados. Nesse caso, você precisará fazer um novo `git add` e commitar novamente.

Se o `pre-commit` falhar mostrando erros de formatação dos linters (como a norminette), você precisará fazer as alterações recomendadas. Após corrigir os erros, faça um novo `git add` e commite novamente.

### Executando o Pre-commit Manualmente

Você pode rodar o `pre-commit` manualmente antes de fazer um commit usando o comando:

```bash
pre-commit run --all-files
```

Este comando executará todos os ganchos configurados no arquivo `.pre-commit-config.yaml` em todos os arquivos do projeto. Note que, se houver alterações nos arquivos após a execução do `pre-commit run`, você precisará fazer um novo `git add` e executar o comando novamente antes de prosseguir com o commit.
