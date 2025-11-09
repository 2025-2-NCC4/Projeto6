# Projeto 06 - 💰 Money BR (Antiga Fecap Money)

---

## 🏫 FECAP - Fundação de Comércio Álvares Penteado

<p align="center">
<a href= "https://www.fecap.br/"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhZPrRa89Kma0ZZogxm0pi-tCn_TLKeHGVxywp-LXAFGR3B1DPouAJYHgKZGV0XTEf4AE&usqp=CAU" alt="FECAP - Fundação de Comércio Álvares Penteado" border="25.0px"></a>
</p>

---

## 👨‍💻 Integrantes: [André dos Santos](https://www.linkedin.com/in/andr%C3%A9-dos-santos-greg%C3%B3rio-025a402ba/), [Guilherme Fogolin](https://www.linkedin.com/in/guilhermefogolin/), [Pedro Lemos](https://www.linkedin.com/in/pedrohnlemos/) e [Yan Cezareto](https://www.linkedin.com/in/yan-cezareto-792ba22b8/)

---

## 👨‍🏫 Professores Orientadores: [Eduardo Savino Gomes](https://www.linkedin.com/in/eduardo-savino/), [Lucy Mari Tabuti](https://www.linkedin.com/in/lucymari/), [Mauricio Lopes Da Cunha](https://www.linkedin.com/in/mauricio-lopes-da-cunha-5630492a/) e [Rodnil da Silva Moreira Lisboa](https://www.linkedin.com/in/professorrodnil/)
---

## 📄 Descrição

<p align="center">
  <img src="./imagens/moneybr-branco.png" alt="Logo Money BR" width="200">
</p>

Com a missão de promover a **democratização de dados**, extração de insights e decisões certeiras, nasceu a **Money BR**. O projeto tem o propósito de auxiliar a empresa [Pic Money](https://www.picmoney.shop/), parceira da FECAP, com a análise de dados dos seus negócios. Dessa forma, trabalhamos continuamente em trazer visões que possibilitassem entender a volumetria de transações dos cupons, dados demográficos dos clientes, lojas com maior rentabilidade, receita bruta, receita líquida, ticket médio e demais. Com isso, fizemos uma divisão entre CEO (Chief Executive Officer) e CFO (Chief Financial Officer), com dados gerais e dados financeiros, respectivamente. 

---

## 📋 Detalhes

📊 O projeto Money BR implementou um dashboard de business intelligence (BI) e visualização de dados, sendo o produto resultante desta atividade desenvolvido em Python e construído, principalmente, com a biblioteca Streamlit.

As funcionalidades essenciais incluem:

🎲 Processamento e integração de dados: Recebimento, limpeza e processamento de diversos bancos de dados (clientes, lojas, cupons, geolocalização) fornecidos pela Pic Money para transformar dados brutos em conhecimento visual e acionável.

📈 Criação de visões estratégicas distintas: Implementação de diferentes módulos de visualização dentro do painel, fornecendo insights específicos para as necessidades do CEO e do CFO.

🔑 Visualização de métricas-chave: O dashboard permite à liderança visualizar métricas estratégicas em tempo real, cobrindo tanto métricas de engajamento e negócio (visão do CEO) quanto métricas de performance financeira (visão do CFO).

💡 Análise de desempenho: Permite o acompanhamento da performance do engajamento dos clientes (coleta de cupons, conversão em compras, etc.) e a rentabilidade e o desempenho das parcerias com as lojas.

---

## 🗂️ Estrutura de pastas

```
├── 🗂️ documentos/
│   ├── 📁 Entrega01
│   │  └── 📂 Analise_Inferencial
│   │  └── 📂 Contabilidade
│   │  └── 📂 Engenharia_Software
│   │  └── 📂 Projeto
│   ├── 📁 Entrega02
│   │  └── 📂 Analise_Inferencial
│   │  └── 📂 Contabilidade
│   │  └── 📂 Engenharia_Software
│   │  └── 📂 Projeto
├── 🗂️ imagens/
├── 🗂️ src/
│   ├── 📁 Entrega01
│   │  └── 📂 Backend
│   │  └── 📂 Frontend
│   ├── 📁 Entrega02
│   │  └── 📂 Backend
│   │  └── 📂 Frontend
└── 📄 readme.md
```

README.MD: Arquivo que serve como guia e explicação geral sobre o projeto.

Além disso, há outras pastas com os devidos arquivos em cada período de entrega:

⛲ [src](./src): Pasta que contém arquivos do frontend e backend da Money BR, divididos por entregas conforme cronograma da FECAP.

📄 [documentos](/documentos): Devidos documentos do projeto e arquivos relacionados as matérias de Análise Inferencial de Dados, Contabilidade, Engenharia de Software e Projeto Interdisiciplinar.

📸 [img](/imagens): Reunião de imagens utilizadas no projeto.

---

## 🛠️ Tutoriais de instalação

- Para funcionamento completo da aplicação, deverá ser instalado previamente as dependências utilizadas nesse projeto. Para isso rode o comando abaixo no terminal:
```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r src/Entrega02/Frontend/requirements.txt
```

---

## ⚙️ Ferramentas e tecnologias

### Desenvolvimento principal
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)	
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)	
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)

### Visualização de dados

![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-2C3E50?style=for-the-badge&logo=plotly&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

### Limpeza e análise de dados auxiliar

![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=google-colab&logoColor=white)	
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)	

### Prototipação e estilização

![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)	

### Oganização

![Scrum](https://img.shields.io/badge/Scrum-007bff?style=for-the-badge&logo=scrumalliance&logoColor=white)	
![Kanban](https://img.shields.io/badge/Kanban-373a3c?style=for-the-badge&logo=trello&logoColor=white)
![GitHub Projects](https://img.shields.io/badge/GitHub%20Projects-121013?style=for-the-badge&logo=github&logoColor=white)

### Versionamento

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

---

## 📋 Licença

Money BR © 2025 by André Gregório dos Santos, Guilherme Reis Fogolin de Godoy, Pedro Henrique Nascimento Lemos, Yan Cezareto Ramos is licensed under CC BY-NC-ND 4.0

---

## 🎓 Referências 

1. ALURA (São Paulo). **Storytelling com dados: transforme seus dados em narrativas envolventes**. Disponível em: https://www.alura.com.br/artigos/storytelling-com-dados. Acesso em: 05 ago. 2025.

2. Python Software Foundation. **Python 3.14.0 documentation**. 2025. Disponível em: https://docs.python.org/3/. Acesso em: 11 set. 2025.

3. **STREAMLIT documentation**. 2025. Disponível em: https://docs.streamlit.io/. Acesso em: 27 ago. 2025.

4. XAVIER, Amanda; NARIMATSU, Gustavo; CAROLINA, Larissa; GONZAGA, Matheus; LUNA, Adrian. **Manual Rcommander**. Disponível em: https://www.est.ufmg.br/~monitoria/Material/Manual_Rcmdr.pdf. Acesso em: 03 set. 2025.

---
