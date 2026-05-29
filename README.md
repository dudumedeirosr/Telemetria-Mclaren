# 🏎️ Análise de Telemetria McLaren: Lando Norris vs. Oscar Piastri

Este projeto consiste em um pipeline de Engenharia de Dados desenvolvido para processar e analisar dados brutos de telemetria da McLaren, comparando o desempenho dos pilotos Lando Norris e Oscar Piastri. O objetivo é decifrar, através dos dados, quem leva a melhor em métricas como velocidade final, eficiência de frenagem e consistência de tempo de volta.

Todo o processamento foi desenvolvido utilizando **PySpark** dentro do ambiente **Databricks**, aplicando os conceitos práticos da **Arquitetura Medalhão**.

---

## 🏗️ Arquitetura do Pipeline (Modelo Medalhão)

O projeto foi estruturado em três camadas lógicas para garantir a organização e a qualidade dos dados de telemetria:

*   **🥉 Camada Bronze (Ingestão):** Consumo dos dados brutos diretamente do arquivo de sensores (`mclaren_raw_telemetry.csv`), mantendo o histórico fiel da pista sem nenhuma alteração.
*   **🥈 Camada Silver (Limpeza e Padronização):** Tratamento de valores nulos, conversão de tipos de dados (como formatos de tempo e velocidade), eliminação de duplicadas e separação clara dos registros de cada piloto (Norris vs. Piastri).
*   **🥇 Camada Gold (Agregação de Negócio):** Criação de tabelas analíticas prontas para visualização. Nesta etapa, os dados foram agregados para extrair insights direto das pistas: quem teve a maior velocidade máxima nas retas, quem freou mais tarde e quem foi mais consistente nas curvas.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

*   **Databricks:** Plataforma de dados na nuvem utilizada para o desenvolvimento e execução do pipeline.
*   **PySpark (Apache Spark):** Motor de processamento distribuído para manipulação escalável dos dados de telemetria.
*   **Python:** Linguagem base para construção das regras de negócio do ecossistema da Fórmula 1.
*   **Git & GitHub:** Ferramentas para controle de versão e publicação do projeto de portfólio.

---

## 📁 Estrutura do Repositório

O repositório está organizado de forma simples e direta:
*   `mclaren_raw_telemetry.csv`: A base de dados bruta utilizada como ponto de partida (Camada Bronze).
*   `Telemetria McLaren.py`: O script completo contendo todo o código Spark do pipeline (da Bronze até a Gold).
