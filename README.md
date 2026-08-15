#### Guia de Desenvolvimento e Utilização

**Execução Multiambiente**
- **Local / Databricks**: Execute o script de entrada diretamente via terminal ou job:
    - `python entrypoints/run_exemplo.py`
- **Airflow**: Acesse a interface web do Airflow, ative a DAG `exemplo_pipeline_dag` e execute a task manualmente ou aguarde o agendamento.

<hr>

##### 1. Criação do Pipeline (POO)
Escreva a classe com a lógica de negócio em `include/pipelines/exemplo_extractor.py` herdando de `BaseExtractor`:

```py
# include/pipelines/exemplo_extractor.py
from include.src.core.base_extractor import BaseExtractor

class ExemploExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()

    def execute(self) -> None:
        print("Executando extração de dados...")
```

##### 2. Criação do Entrypoint
Crie o script de entrada em `entrypoints/run_exemplo.py` instanciando e executando a classe criada:

```py
# entrypoints/run_exemplo.py
from include.pipelines.exemplo_extractor import ExemploExtractor

if __name__ == "__main__":
    pipeline = ExemploExtractor()
    pipeline.execute()
```

##### 3. Criação da DAG no Airflow
Instancie uma tarefa em `dags/exemplo_dag.py` utilizando o `BashOperator` para acionar o entrypoint correspondente:

```py
# dags/exemplo_dag.py
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="exemplo_pipeline_dag",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_exemplo_pipeline",
        bash_command="python /usr/local/airflow/entrypoints/run_exemplo.py",
    )
```

<hr>

##### Estrutura de Diretórios
```sh
├── .dockerignore               # Arquivos e pastas ignorados na construção da imagem Docker
├── .env                        # Variáveis de ambiente e credenciais locais
├── .env.example                # Modelo de referência para as variáveis de ambiente
├── .gitignore                  # Arquivos e pastas ignorados pelo Git
├── Dockerfile                  # Imagem Docker customizada do projeto
├── LICENSE                     # Licença de uso e distribuição do projeto
├── README.md                   # Documentação principal e instruções do projeto
├── airflow_settings.yaml       # Configurações do ambiente Airflow (Astro CLI / Local)
├── docker-compose.override.yml # Configurações locais adicionais/sobreposições do Docker Compose
├── docker-compose.yaml         # Orquestração de containers para ambiente local
├── packages.txt                # Pacotes de nível de sistema operacional (Debian/Ubuntu)
├── requirements.txt            # Dependências Python do projeto
├── dags/                       # Definições das DAGs do Airflow
├── dashboard/                  # Arquivos de visualização e relatórios (ex: .pbix)
├── docs/                       # Documentação técnica e arquivos de mídia associados
├── entrypoints/                # Pontos de entrada (scripts para execução no Databricks ou Jobs)
├── include/                    # Código-fonte principal e recursos compartilhados
│   ├── assets/                 # Arquivos estáticos e dados de suporte (JSON, PKL, etc.)
│   ├── pipelines/              # Lógica de execução dos fluxos de dados
│   ├── sql/                    # Queries e scripts SQL
│   └── src/                    # Módulos Python reutilizáveis
│       ├── config/             # Configurações do projeto e variáveis
│       ├── core/               # Abstrações e classes base (ex: extractors, loaders)
│       ├── engines/            # Conectores e processadores de dados
│       └── utils/              # Utilitários gerais (logs, manipulação de caminhos, etc.)
├── plugins/                    # Plugins customizados para o Airflow
├── tests/                      # Testes unitários e de integração
└── tmp/                        # Armazenamento temporário de arquivos de execução local
```

- `include/src/`: Núcleo do projeto contendo a classe base (`core/base_extractor.py`), configurações e utilitários (`utils/paths.py`, `utils/utils.py`).
- `include/pipelines/`: Classes orientadas a objetos com as regras de negócio e rotinas de extração/transformação (`instagram_feed_extractor.py`, `proxy_update_list.py`).
- `entrypoints/`: Scripts Python de ponto de entrada (`run_instagram_feed.py`, `run_instagram_profile.py`) que executam os pipelines no ambiente local, Airflow ou Databricks.
- `dags/`: DAGs do Airflow (`instagram_etl_full.py`) que orquestram a execução utilizando `BashOperator` para acionar os entrypoints.
- `include/assets/`: Chaves GCP (`sa_gcp.json`), cookies (`ig_cookie.pkl`) e arquivos de proxies.
- `include/sql/`: Schemas DDL para tabelas Silver e Gold (`ddl_silver_candidaturas.psql`, `ddl_gold_candidaturas.psql`).
- `powerbi/`: Dashboards e temas do Power BI (`dashboard2026.pbix`).
- `tmp/`: Armazenamento temporário de dados brutos (`feed_user_posts/jsons/`, imagens).
- `docs/`: Imagens da arquitetura, relatórios e especificações do projeto.

<hr>

##### 🚀 Astronomer (Astro CLI)

Instalação:
```sh
curl -sSL install.astronomer.io | sudo bash -s
astro version
```

Comandos úteis:
```sh
astro dev start   # iniciar ambiente
astro dev stop    # parar ambiente
astro dev restart # reiniciar ambiente
```

##### 🐋 Docker

Subir containers:
```sh
docker compose up -d --build
```

Usando compose específico
```sh
docker compose -f docker-compose.yml up -d --build
```

Ver containers em execução:
```sh
docker ps
```

Logs:
```sh
docker compose logs
docker compose logs -f
```