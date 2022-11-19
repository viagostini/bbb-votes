
MAKE += --no-print-directory RECURSIVE=1

ifndef VERBOSE
COMPOSE_ARGS := 2>/dev/null
COMPOSE_BUILD_ARGS := -q
endif

COMPOSE := docker-compose ${COMPOSE_ARGS}
COMPOSE_BUILD := ${COMPOSE} build ${COMPOSE_BUILD_ARGS}
COMPOSE_UP := ${COMPOSE} up -d
COMPOSE_EXEC := ${COMPOSE} exec

################################################################################
##                                   COLORS                                   ##
################################################################################

RES := \033[0m
MSG := \033[1;36m
ERR := \033[1;31m
SUC := \033[1;32m
WRN := \033[1;33m
NTE := \033[1;34m

################################################################################
##                                 AUXILIARY                                  ##
################################################################################

define message
printf "${MSG}%s${RES}\n" $(strip $1)
endef

define success
(printf "${SUC}%s${RES}\n" $(strip $1); exit 0)
endef

define note
(printf "${NTE}%s${RES}\n" $(strip $1); exit 0)
endef

wait-%:
	@sleep $*

build:
	@$(call message,"Building images")
	@$(COMPOSE_BUILD) 

start-redpanda:
	@$(call message,"Starting Redpanda")
	@$(COMPOSE_UP) redpanda
	@$(MAKE) wait-2

create-votes-topic:
	@$(call message,"Creating votes topic")
	@$(COMPOSE_EXEC) redpanda rpk topic create votes -p 10

start-api:
	@$(call message,"Starting API")
	@$(COMPOSE_UP) api

start-processors:
	@$(call message,"Starting vote processors")
	@$(COMPOSE_UP) vote_processor_1
	@$(COMPOSE_UP) vote_processor_2

start:
	@$(call note,"Starting all containers")
	@$(MAKE) start-redpanda
	@$(MAKE) wait-2
	@$(MAKE) create-votes-topic
	@$(MAKE) start-api
	@$(MAKE) start-processors
	@$(call success,"Ready")

stop:
	@$(call note,"Stopping all containers")
	@$(COMPOSE) down -v
	@$(call success,"Done")