# Versicle to Image
Script em python para gerar imagens dos versículos que usamos em nossos cultos pelo YouTube.

## Como usar
Tendo o python instalado tudo o que precisa fazer é instalar a biblioteca pillow.

Então rode: `python vers2img.py <referência>`.

Use o seguinte formato para a referência, ambos iniciados com a abreviatura do livro: 
- <livro>_<capitulo>_<versículo> - Ex: gn\_1\_1
- <livro>_<capítulo>_<versículo>-<versículo> - Versículos em sequência - Ex: rm\_1\_1\-8

Opcões extras:
- --version: selecione a versão da bíblia a ser usada. Disponíveis: AA, ACF e NVI. Por padrão a NVI é selecionada.
- --output: caminho onde deseja exportar as imagens

## Material
- Versões da bíblia vem do projeto ["Bíblia XML + SQL + JSON"](https://github.com/thiagobodruk/biblia)
- Fontes de uso livre

## Licença
Veja o arquivo LICENSE.txt


# English Version
Python script to generate versicle images that are used on our YouTube services.

## How to use
With python already installed you need to add the pillow library.

Then you will be able to run: `python vers2img <reference>`

You need to use the following format for the reference, both started with the book abbreviation:
- <book>_<chapter>_<verscile> - Eg: gn\_1\_1
- <book>_<chapter>_<verscile>-<versicle> - Range of versicles - Eg: rm\_1\_1\-8

Extra options:
- --version: select a bible version. You will need to download a bible version from the project mentioned below (This project was only released with version in portuguese).
- --output: path to where you want the images exported

## Material
- You can get bible versions from ["Bible: XML and JSON"](https://github.com/thiagobodruk/bible)
- Free fonts

## License
Please check the file LICENSE.txt for more information.
