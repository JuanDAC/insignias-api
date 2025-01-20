param (
    [string]$action,
    [switch]$help
)

function Show-Usage {
    Write-Host "
Uso: .\$($MyInvocation.MyCommand.Name) [-h] [-a action]

Opciones:
    -h, --help        Mostrar esta ayuda
    -a, --action      Ejecutar un comando

Flag details: .\$($MyInvocation.MyCommand.Name) [-a | --action] [actions]:
    Description: 
    - This flag is used to specify the desired action to be performed by the script or command.
    Options: 
    - .\$($MyInvocation.MyCommand.Name) -a dev
    - .\$($MyInvocation.MyCommand.Name) -a dev:bare_metal
    - .\$($MyInvocation.MyCommand.Name) -a deploy:aws
    - .\$($MyInvocation.MyCommand.Name) -a deploy:bare_metal
    - .\$($MyInvocation.MyCommand.Name) -a start:aws:db
    - .\$($MyInvocation.MyCommand.Name) -a start:bare_metal:db
    - .\$($MyInvocation.MyCommand.Name) -a docker
"
}

function Install-Python {
    $PYTHON_VERSION = "3.13"
    $INSTALLER_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-amd64.exe"
    $INSTALLER_PATH = "$env:TEMP\python-installer.exe"

    Invoke-WebRequest -Uri $INSTALLER_URL -OutFile $INSTALLER_PATH
    Start-Process -FilePath $INSTALLER_PATH -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $INSTALLER_PATH
    Write-Host "Python $PYTHON_VERSION instalado."
}

function Perform-Action {
    switch ($action) {
        'dev' {
            & docker-compose up -d --build
        }
        'dev:bare_metal' {
            if (-not (Get-Command "python3" -ErrorAction SilentlyContinue)) {
                Install-Python
            }

            $APP_DIR = Get-Location
            $PYTHON = "python"

            & $PYTHON -m venv "$APP_DIR\venv"
            & "$APP_DIR\venv\Scripts\Activate.ps1"
            Write-Host "Virtual environment created and activated successfully."
            & pip install -r requirements.txt
            & $PYTHON -m uvicorn app.pesentation.api.main:app --reload
        }
        'deploy:aws' {
            & docker build -t insignia-app:latest .
            & docker push insignia-app:latest

            aws ecs create-service `
                --cluster $env:AWS_CLUSTER_NAME `
                --service-name $env:AWS_SERVICE_NAME `
                --task-definition $env:AWS_TASK_DEFINITION `
                --desired-count 1
        }
        'deploy:bare_metal' {
            Start-Service -Name "insignias_uvicorn_service"
            Set-Service -Name "insignias_uvicorn_service" -StartupType Automatic
        }
        'start:aws:db' {
            aws rds start-db-instance --db-instance-identifier $env:AWS_DB_INSTANCE
        }
        'start:bare_metal:db' {
            $DB_USER = $env:DB_USER -or "postgres"
            $PORT = 5432             # Puerto de conexión
            $DB_PASSWORD = $env:DB_PASSWORD -or "mysecretpassword"
            $DB_DATA_DIR = $env:DB_DATA_DIR -or "C:\ProgramData\PostgreSQL\Data"

            if (-not $DB_USER -or -not $DB_PASSWORD -or -not $DB_DATA_DIR) {
                Write-Host "Error: Las variables de entorno DB_USER, DB_PASSWORD y DB_DATA_DIR deben estar definidas."
                exit 1
            }

            if (-not (Get-Command "postgresql" -ErrorAction SilentlyContinue)) {
                Write-Host "Instalando PostgreSQL..."
                $POSTGRES_INSTALLER_URL = "https://get.enterprisedb.com/postgresql/postgresql-13.4-1-windows-x64.exe"
                $POSTGRES_INSTALLER_PATH = "$env:TEMP\postgresql-installer.exe"

                Invoke-WebRequest -Uri $POSTGRES_INSTALLER_URL -OutFile $POSTGRES_INSTALLER_PATH
                Start-Process -FilePath $POSTGRES_INSTALLER_PATH -ArgumentList "--mode unattended" -Wait
                Remove-Item $POSTGRES_INSTALLER_PATH
            }

            Start-Service -Name "postgresql-x64-13"

            if (-not (& pg_isready -U $DB_USER -h localhost)) {
                Write-Host "Error: No se pudo iniciar la base de datos PostgreSQL."
                exit 1
            }

            & "C:\Program Files\PostgreSQL\13\bin\psql.exe" -U postgres -c "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
            & "C:\Program Files\PostgreSQL\13\bin\psql.exe" -U postgres -c "CREATE USER IF NOT EXISTS $DB_USER WITH PASSWORD '$DB_PASSWORD';"
            & "C:\Program Files\PostgreSQL\13\bin\psql.exe" -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
            $dbUri = "postgres://${DB_NAME}:${DB_PASSWORD}@hostname:$PORT/$DB_NAME"
            Write-Host "URI de conexión: $dbUri"
            $env:SQLALCHEMY_DATABASE_URI=$dbUri
        }
        'docker' {
            & docker $args
        }
        default {
            Write-Host "Acción inválida: $action" -ForegroundColor Red
            Show-Usage
            exit 1
        }
    }
}

if ($help) {
    Show-Usage
    exit 0
}

if (-not $action) {
    Write-Host "Error: Se debe especificar una acción." -ForegroundColor Red
    Show-Usage
    exit 1
}

Perform-Action