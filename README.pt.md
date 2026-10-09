[English](README.md) | [Português](README.pt.md)

# MangaFire Downloader

Uma ferramenta de linha de comando para baixar volumes e capítulos do MangaFire como arquivos CBZ.

**Construído sobre o [`gallery-dl`](https://github.com/mikf/gallery-dl).** O MangaFire Downloader depende do projeto `gallery-dl` para a infraestrutura de extração e download. Este projeto não existiria em sua forma atual sem o trabalho dos desenvolvedores e contribuidores do `gallery-dl`.

> **Última versão:** [v0.5.0](https://github.com/Osanticide/mangafire-dl/releases/tag/v0.5.0). Instale pelo [PyPI](https://pypi.org/project/mangafire-dl/) ou baixe o [ZIP portátil para Windows](https://github.com/Osanticide/mangafire-dl/releases/download/v0.5.0/mangafire-dl-windows-x64-0.5.0.zip).

## Funcionalidades

- Baixar volumes ou capítulos individuais diretamente por suas URLs do MangaFire.
- Selecionar volumes ou capítulos em uma página de mangá por número, intervalo ou combinação dos dois.
- Salvar os downloads como arquivos CBZ.
- Escolher um diretório de saída personalizado.
- Usar a interface de linha de comando em ambientes Python compatíveis ou a versão portátil para Windows sem instalar Python.

## Instalação

### Windows — ZIP portátil

1. Abra [GitHub Releases](https://github.com/Osanticide/mangafire-dl/releases).
2. Baixe o arquivo `mangafire-dl-windows-x64-<version>.zip` da versão desejada.
3. Extraia o ZIP para uma pasta.
4. Para usar o assistente interativo, dê dois cliques em `Executar.bat`. Ele solicita a URL do MangaFire e as opções de download, e mantém o terminal aberto para que você possa ler o resultado.
5. Para usar a interface de linha de comando diretamente, execute `mangafire-dl.exe` pelo PowerShell ou Prompt de Comando e informe a URL e as opções descritas abaixo.

O ZIP portátil inclui o executável e os arquivos necessários. Mantenha `mangafire-dl.exe`, `Executar.bat` e a pasta `_internal` juntos. Não mova nem distribua apenas o EXE.

### Python — pipx

Depois que o pacote for publicado no PyPI, instale a aplicação de linha de comando com:

```powershell
pipx install mangafire-dl
```

Para atualizá-la posteriormente:

```powershell
pipx upgrade mangafire-dl
```

### Python — pip

É necessário Python 3.10 ou superior. Recomendamos utilizar um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install mangafire-dl
```

No Linux ou macOS, ative o ambiente com `source .venv/bin/activate` em vez do comando de ativação do PowerShell.

## Início rápido

Substitua a URL de exemplo ou as seleções pelo recurso do MangaFire que deseja baixar.

### Baixar diretamente uma URL de volume ou capítulo

Uma URL direta de volume ou capítulo pode ser usada sozinha:

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach/volume/144857"
```

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach/chapter/6056551"
```

URLs diretas de recursos não podem ser combinadas com `--lang`, `--volumes` ou `--chapters`.

### Baixar volumes selecionados de uma página de mangá

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach" --lang pt-br --volumes "1-5"
```

### Baixar capítulos selecionados de uma página de mangá

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach" --lang en --chapters "1-5, 10, 12-15"
```

### Escolher o diretório de saída

Adicione `--output` a qualquer comando compatível:

```powershell
mangafire-dl "https://mangafire.to/title/027-bleach" --lang pt-br --volumes "1-5" --output "D:\Mangas"
```

Por padrão, os arquivos baixados são salvos no diretório Downloads do sistema operacional.

## Uso

### Sintaxe da linha de comando

```text
mangafire-dl URL [--lang LANGUAGE] [--volumes SELECTION | --chapters SELECTION] [--output PATH]
```

### Opções

| Opção | Descrição |
| --- | --- |
| `URL` | Página de mangá, URL de volume ou URL de capítulo do MangaFire. Obrigatória. |
| `--lang LANGUAGE` | Código do idioma dos recursos selecionados a partir de uma página de mangá. Obrigatório para downloads de páginas de mangá. Exemplos: `pt-br`, `en`. |
| `--volumes SELECTION` | Volumes a baixar a partir de uma página de mangá. Não pode ser usado junto com `--chapters`. |
| `--chapters SELECTION` | Capítulos a baixar a partir de uma página de mangá. Não pode ser usado junto com `--volumes`. |
| `--output PATH` | Diretório de saída. Por padrão, usa o diretório Downloads do sistema operacional. |
| `--help` | Exibe a ajuda da linha de comando. |
| `--version` | Exibe a versão instalada. |

Para uma URL de página de mangá, informe `--lang` e exatamente uma das opções `--volumes` ou `--chapters`. Para uma URL direta de volume ou capítulo, informe somente a URL e, opcionalmente, `--output`.

### Sintaxe das seleções

As seleções aceitam números individuais, intervalos e combinações separados por vírgula:

```text
1
1-5
1, 6, 12
1-5, 8, 12-15
```

Use aspas ao redor de uma seleção nos comandos do terminal, especialmente quando houver vírgulas ou espaços.

## Estrutura de saída

Os downloads são organizados por mangá e tipo de recurso. Por exemplo:

```text
Downloads/
└── Bleach/
    ├── volumes/
    │   ├── Bleach - Volume 01.cbz
    │   └── Bleach - Volume 02.cbz
    └── chapters/
        ├── Bleach - Chapter 001.cbz
        └── Bleach - Chapter 002.cbz
```

Os números dos volumes normalmente são preenchidos com dois dígitos, e os números dos capítulos com três. Capítulos decimais preservam a parte decimal. A pasta do mangá e os nomes dos arquivos são derivados do título do recurso.

## Requisitos

- **Pacote Python:** Python 3.10 ou superior.
- **Dependências de execução:** `gallery-dl` e `requests` são declaradas pelo pacote e instaladas automaticamente pelo `pip` ou `pipx`.
- **ZIP portátil para Windows:** não requer instalação separada do Python ou do `gallery-dl`. Mantenha o EXE e sua pasta `_internal` juntos.

## Solução de problemas

- **O terminal fecha depois de dar dois cliques no EXE:** o EXE é uma aplicação de linha de comando e espera receber uma URL. Use `Executar.bat` para abrir o prompt interativo ou execute `mangafire-dl.exe` em um terminal já aberto, informando a URL e as opções.
- **Uma URL de página de mangá é rejeitada:** inclua `--lang` e uma das opções `--volumes` ou `--chapters`.
- **Uma URL direta de volume ou capítulo é rejeitada quando opções são fornecidas:** URLs diretas não podem ser combinadas com `--lang`, `--volumes` ou `--chapters`.
- **Nenhum recurso é encontrado:** confira o idioma selecionado e os números de volumes ou capítulos disponíveis no MangaFire.
- **Uma requisição falha:** confira a conexão com a internet e se o MangaFire está acessível; depois, tente novamente. As respostas do site e os recursos disponíveis podem mudar.
- **A versão portátil não inicia:** extraia o ZIP completo e mantenha `mangafire-dl.exe`, `Executar.bat` e `_internal` na mesma pasta.

## Limitações

- A ferramenta depende do comportamento atual do site MangaFire e dos recursos disponíveis; mudanças no site podem exigir atualizações.
- A interface de linha de comando ainda não oferece uma interface gráfica.
- A versão portátil para Windows é distribuída como uma pasta compactada em ZIP, não como instalador do Windows.

## Para desenvolvedores

### Preparar o ambiente de desenvolvimento

Clone o repositório e crie um ambiente virtual:

```powershell
git clone https://github.com/Osanticide/mangafire-dl.git
cd mangafire-dl
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

No Linux, ative o ambiente com `source .venv/bin/activate`.

### Executar os testes

```powershell
python -m pytest
```

### Construir os artefatos de lançamento

```powershell
python scripts/build_release.py
```

O script executa a suíte de testes e constrói o wheel Python e a distribuição de código-fonte. Quando executado no Windows, também constrói a pasta standalone e gera o ZIP portátil. Execute o script em cada sistema operacional de destino; o PyInstaller não compila um executável Windows a partir do Linux nem um executável Linux a partir do Windows.

Os artefatos são gravados em `dist/`. O script prepara os arquivos localmente; ele não os publica no PyPI nem cria automaticamente uma GitHub Release.

## Contribuições

Relatos de bugs, sugestões e pull requests são bem-vindos. Antes de abrir um pull request, execute a suíte de testes e descreva o comportamento afetado pela alteração.

## Licença

O projeto original MangaFire Downloader é licenciado sob a [Licença MIT](LICENSE). Componentes de terceiros, incluindo o [`gallery-dl`](https://github.com/mikf/gallery-dl), continuam sujeitos às suas respectivas licenças.

## Agradecimentos

O MangaFire Downloader utiliza o [`gallery-dl`](https://github.com/mikf/gallery-dl) como componente de download subjacente. Muito obrigado aos desenvolvedores e contribuidores por criarem e manterem esse projeto.

## Aviso legal

O MangaFire Downloader é um projeto independente de terceiros e não é afiliado, endossado ou mantido pelo MangaFire nem pelo projeto `gallery-dl`. Os usuários são responsáveis por cumprir as leis aplicáveis, os requisitos de direitos autorais e os termos que se aplicam aos sites e conteúdos que acessam.
