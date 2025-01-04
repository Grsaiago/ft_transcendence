GREEN := $(shell printf "\033[32m")
YELLOW := $(shell printf "\033[33m")
BLUE := $(shell printf "\033[34m")
MAGENTA := $(shell printf "\033[35m")
RESET := $(shell printf "\033[0m")

COMPOSE = docker-compose
NAME = 'Transcendence das Minas \(e Saiago\)'

.PHONY: all
all: up
	@printf "\n$(GREEN)✨ Projeto $(NAME) criado com sucesso! ✨$(RESET)\n\n"
	@docker container ls --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
	@printf "\n$(BLUE)📊 Recursos utilizados pelos containers: 📊$(RESET)\n\n"
	@sleep 2
	@docker container stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

.PHONY: asc
asc: ascii_art

.PHONY: up
up: ascii_art
	$(COMPOSE) up -d --build
	@printf "\n$(BLUE)🚀 Inicializando o projeto $(NAME)... 🚀$(RESET)\n\n"

.PHONY: verbose
verbose:
	$(COMPOSE) up
	@printf "\n$(BLUE)🚀 Inicializando o projeto $(NAME)... 🚀$(RESET)\n\n"

.PHONY: start
start:
	$(COMPOSE) start
	@printf "\n$(YELLOW)🔀 Projeto $(NAME) iniciado 🔀$(RESET)\n\n"

.PHONY: down
down: stop
	$(COMPOSE) down -v
	@printf "\n$(MAGENTA)🛑 Projeto $(NAME) parado 🛑$(RESET)\n\n"

.PHONY: re
re: down up
	@printf "\n$(YELLOW)🔁 Projeto $(NAME) recriado 🔁$(RESET)\n\n"

.PHONY: stop
stop:
	$(COMPOSE) stop
	@printf "\n$(MAGENTA)⏸️ Projeto $(NAME) pausado ⏸️$(RESET)\n\n"

.PHONY: restart
restart:
	$(COMPOSE) restart
	@printf "\n$(GREEN)🔁 Projeto $(NAME) recriado 🔁$(RESET)\n\n"

.PHONY: logs
logs:
	$(COMPOSE) logs -f
	@printf "\n$(BLUE)🔍 Logs do projeto Projeto $(NAME) disponíveis 🔍$(RESET)\n\n"

.PHONY: clean
clean:
	$(COMPOSE) down -v
	@printf "\n$(GREEN)🧹 Limpeza concluída 🧹$(RESET)\n\n"

.PHONY: fclean
fclean: clean
	-docker rm -f $$(docker ps -aq)
	-docker rmi -f $$(docker images -aq)
	-docker volume rm -f $$(docker volume ls -q)
	-docker network rm -f $$(docker network ls -q)
	@printf "\n$(YELLOW)💣 Apagou tudo 💣$(RESET)\n\n"


ascii_art:
	@echo  ' _______   ______     ___       _______ .___________.    ___      .__   __.   ______  '
	@echo  '|   ____| /      |   /   \     |   ____||           |   /   \     |  \ |  |  /  __  \ '
	@echo  '|  |__   |  ,----`  /  ^  \    |  |__   `---|  |----`  /  ^  \    |   \|  | |  |  |  |'
	@echo  '|   __|  |  |      /  /_\  \   |   __|      |  |      /  /_\  \   |  . `  | |  |  |  |'
	@echo  '|  |     |  `----./  _____  \  |  |____     |  |     /  _____  \  |  |\   | |  `--`  |'
	@echo  '|__|      \______/__/     \__\ |_______|    |__|    /__/     \__\ |__| \__|  \______/ '
	@echo  '                                                                                      '
	@echo  '  _______      _______.     ___       __       ___       _______   ______             '
	@echo  ' /  _____|    /       |    /   \     |  |     /   \     /  _____| /  __  \            '
	@echo  '|  |  __     |   (----`   /  ^  \    |  |    /  ^  \   |  |  __  |  |  |  |           '
	@echo  '|  | |_ |     \   \      /  /_\  \   |  |   /  /_\  \  |  | |_ | |  |  |  |           '
	@echo  '|  |__| | .----)   |    /  _____  \  |  |  /  _____  \ |  |__| | |  `--`  |           '
	@echo  ' \______| |_______/    /__/     \__\ |__| /__/     \__\ \______|  \______/            '
	@echo  '                                                                                      '
	@echo  ' __   ________      _______.  ______        ___      .______       _______     _______'
	@echo  '|  | |       /     /       | /  __  \      /   \     |   _  \     |   ____|   /       '
	@echo  '|  | `---/  /     |   (----`|  |  |  |    /  ^  \    |  |_)  |    |  |__     |   (----'
	@echo  '|  |    /  /       \   \    |  |  |  |   /  /_\  \   |      /     |   __|     \   \   '
	@echo  '|  |   /  /----.----)   |   |  `--`  |  /  _____  \  |  |\  \----.|  |____.----)   |  '
	@echo  '|__|  /________|_______/     \______/  /__/     \__\ | _| `._____||_______|_______/   '
	@echo  '                                                                                      '
	@echo  '.___  ___.      ___      .______          ___       _______      ___       ______     '
	@echo  '|   \/   |     /   \     |   _  \        /   \     /  _____|    /   \     /  __  \    '
	@echo  '|  \  /  |    /  ^  \    |  |_)  |      /  ^  \   |  |  __     /  ^  \   |  |  |  |   '
	@echo  '|  |\/|  |   /  /_\  \   |      /      /  /_\  \  |  | |_ |   /  /_\  \  |  |  |  |   '
	@echo  '|  |  |  |  /  _____  \  |  |\  \----./  _____  \ |  |__| |  /  _____  \ |  `--`  |   '
	@echo  '|__|  |__| /__/     \__\ | _| `._____/__/     \__\ \______| /__/     \__\ \______/    '

.PHONY: all up start down stop restart logs clean fclean clear re ascii_art
