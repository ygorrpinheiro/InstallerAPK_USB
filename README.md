# InstallerAPK_USB
# Instalador de APKs via ADB

O Instalador de APKs via ADB é uma aplicação de interface gráfica (GUI) em Python que permite instalar arquivos APK em dispositivos Android usando o Android Debug Bridge (ADB).

## Funcionalidades

- Escolha facilmente arquivos APK para instalar.
- Liste dispositivos Android conectados ao computador.
- Instale arquivos APK em um ou mais dispositivos selecionados.
- Desative a depuração USB em dispositivos selecionados.
- Acompanhe o progresso da instalação com uma barra de progresso.

## Como Usar

1. **Configuração Inicial**
   - Abra o programa.
   - Insira o caminho para a pasta do ADB na caixa de texto correspondente.

2. **Escolha Arquivos APK**
   - Clique no botão "Escolher APKs" para selecionar os arquivos APK que você deseja instalar.

3. **Liste Dispositivos**
   - Clique no botão "Listar Dispositivos" para ver os dispositivos Android conectados.

4. **Instalação de APKs**
   - Selecione um ou mais dispositivos da lista.
   - Clique no botão "Instalar APKs" para iniciar o processo de instalação.
   - A barra de progresso mostrará o progresso da instalação.

5. **Desativar Depuração USB**
   - Selecione dispositivos da lista.
   - Clique no botão "Desativar Depuração USB" para desativar a depuração USB nos dispositivos selecionados.

## Criando um Executável

Você pode criar um arquivo executável (.exe) a partir deste programa usando o PyInstaller. Para criar um executável que não abre um terminal, use o seguinte comando:

```bash
pyinstaller --onefile --noconsole seu_arquivo_python.py
