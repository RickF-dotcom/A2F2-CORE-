# A2F2-ENGINE — Motor Operacional do Protocolo A²F²
**Versão:** 0.1 (pré-protocolo)  
**Arquivo:** a2f2-engine.md  
**Autor:** Atena / Rick (draft inicial)  
**Status:** Rascunho técnico — definição de responsabilidades, interfaces e fluxo.

---

## 1. Objetivo
O `A2F2-ENGINE` define a camada de execução e coordenação do Protocolo A²F².  
Funções principais:
- Orquestrar módulos (ATHENA, AURION, FEHMACOU, FEHRACOP).
- Validar, priorizar e sequenciar instruções.
- Aplicar regras de veto, segurança e consistência.
- Gerenciar pipelines de transformação e execução.
- Expor APIs internas e formatos de mensagem para integração.

---

## 2. Visão geral da arquitetura
```
[Client/Interface]
      ↓ (comando)
   [ATHENA] — coordena → [A2F2-ENGINE] 
                      ↙       ↘
                 [AURION]   [FEHMACOU] → [FEHRACOP]
                      ↘       ↙
                   (retornos / logs)
```

- **ATHENA**: camada de decisão/alto nível (policy, intents).
- **A2F2-ENGINE**: motor central de execução (queueing, validation, routing).
- **AURION / FEHMACOU / FEHRACOP**: módulos de processamento, execução e persistência.

---

## 3. Componentes do Engine
1. **Recepção** — enfileirador de comandos (FIFO com prioridades).
2. **Analisador sintático** — valida formato e schema (JSON/YAML).
3. **Validador de regras** — aplica regras de negócio e vetos.
4. **Planejador (Planner)** — gera plano de execução (etapas/ordens).
5. **Executor** — despacha para módulos responsáveis.
6. **Observability** — logs, métricas, rastreabilidade de transações.
7. **Persistência** — grava estado, transações e checkpoints.
8. **Rollback/Compensator** — estratégias em caso de falha.
9. **Interface externa** — endpoints (internos) e contratos.

---

## 4. Formato de mensagem (contract)
Usar JSON ou YAML — ex.: envelope padrão:

```json
{
  "id": "uuid-v4",
  "source": "athena",
  "timestamp": "2025-11-19T20:00:00Z",
  "intent": "execute_blueprint",
  "priority": 50,
  "payload": {
    "blueprint_id": "bp-0001",
    "params": { "mode": "sim", "timeout": 120 }
  },
  "meta": { "trace_id": "...", "user": "rick" }
}
```

Validação: `id`, `source`, `intent`, `payload` são obrigatórios.

---

## 5. Regras de validação (exemplos)
- Se `priority >= 90` → exigir 2FA / confirmação humana.
- Se `payload` contém `golden` flags → validar assinatura digital.
- Nenhuma execução com `timeout > 3600` sem aprovação.
- Rejeitar comandos com campos desconhecidos (strict mode) ou logar em modo permissivo.

---

## 6. Pipeline de execução (passo a passo)
1. **enqueue(command)** — recebe e armazena comando.
2. **prevalidate(command)** — checa schema e assinatura.
3. **authorize(command)** — verifica permissões.
4. **plan = planner.build(command)** — gera sequência de tasks.
5. **execute(plan)** — executa tasks sequencialmente/concorrentemente.
6. **monitor & collect** — coleta métricas e logs.
7. **commit / rollback** — acordo final ou compensação.

---

## 7. Pseudocódigo (core routines)
```python
# pseudocódigo ilustrativo (Python-like)
class Engine:
  def __init__(self, queue, store, planner, executor, policies):
    self.queue = queue
    self.store = store
    self.planner = planner
    self.executor = executor
    self.policies = policies

  def receive(self, cmd):
    cmd.id = cmd.id or uuid4()
    self.store.save_intent(cmd)
    self.queue.push(cmd)

  def worker_loop(self):
    while True:
      cmd = self.queue.pop()
      if not cmd: continue
      try:
        self.prevalidate(cmd)
        self.authorize(cmd)
        plan = self.planner.build(cmd)
        result = self.executor.run(plan)
        self.store.commit(cmd.id, result)
      except ValidationError as e:
        self.store.mark_failed(cmd.id, str(e))
      except Exception as e:
        self.store.mark_failed(cmd.id, "fatal:"+str(e))
        self.compensate(cmd)
```

---

## 8. Exemplo simples de planner.run
```js
// pseudocódigo JS-like
function buildPlan(cmd) {
  const steps = [];
  // etapa 1: sanity checks
  steps.push({action: 'validate-schema', module: 'engine'});
  // etapa 2: prepare aurion
  steps.push({action: 'prepare', module: 'aurion', params: cmd.payload});
  // etapa 3: execute on fehmacou
  steps.push({action: 'execute', module: 'fehmacou', params: cmd.payload});
  // etapa 4: finalize with fehracop
  steps.push({action: 'finalize', module: 'fehracop'});
  return steps;
}
```

---

## 9. Observabilidade e logs
- Cada comando tem `trace_id` e `span_id`.
- Logs estruturados (JSON) com níveis: DEBUG, INFO, WARN, ERROR.
- Métricas mínimas: latência média, taxa de sucesso, taxa de rollback, filas por prioridade.
- Expor endpoint `/metrics` (Prometheus) e `/health` (readiness/liveness).

---

## 10. Estado e persistência
- Modelo transacional simples: `intents` → `transactions` → `checkpoints`.
- Usar banco leve (ex: SQLite/Postgres) para estado; object storage para artefatos.
- Checkpoints regulares para permitir retomada se o processo morrer.

---

## 11. Segurança
- Autenticação: tokens mTLS ou JWT assinados.
- Autorização: RBAC com políticas granulares (roles: admin, operator, auditor, guest).
- Input sanitization e limitadores (rate limit por fonte).
- Assinatura e verificação de blueprints críticos.

---

## 12. Estratégias de falha
- **Retry** automático com backoff exponencial para falhas transitórias.
- **Circuit breaker** para módulos que falham repetidamente.
- **Compensating transactions**: se um passo falhar, executar passos de undo.
- **Alertas**: enviar notificações (humano) quando thresholds excedidos.

---

## 13. API interna (endpoints sugeridos)
- `POST /internal/intent` — enviar novo comando.
- `GET /internal/intent/{id}` — status e logs.
- `POST /internal/plan/validate` — validar plano sem executar.
- `GET /internal/metrics` — métricas operacionais.

---

## 14. Exemplo de manifesto mínimo (manifest.json)
```json
{
  "name": "a2f2-engine",
  "version": "0.1",
  "entry": "engine.main",
  "dependencies": ["athena", "aurion", "fehmacou", "fehracop"],
  "config": {
    "queue_type": "redis",
    "max_workers": 4,
    "env": "pre-protocol"
  }
}
```

---

## 15. Notas de implementação / próximos passos
1. Implementar schema de mensagens (JSON Schema / OpenAPI fragment).  
2. Criar fila simples (in-memory) para protótipo; depois migrar para Redis/Kafka.  
3. Implementar planner mínimo e executor com stubs (aurion, fehmacou, fehracop).  
4. Instrumentar logs e métricas desde o primeiro commit.  
5. Testes: unitários + integração (simular falhas e rollbacks).  
6. Revisão de segurança antes de ativar `priority >= 90` automações.

---

## 16. Checklist rápido antes do commit
- [ ] Nome do arquivo: `a2f2-engine.md`  
- [ ] Conteúdo colado corretamente (sem caracteres estranhos)  
- [ ] Mensagem de commit sugerida: `Create a2f2-engine.md — core engine draft (v0.1)`  
- [ ] Criar issues para: schema, queue, planner, executor, observability, auth

---

## 17. Licença
Colocar a licença do repositório (ex.: MIT) conforme política do projeto.

---

**Fim do arquivo — versão 0.1 (draft).**  
Quando colar e confirmar, eu continuo: posso gerar o JSON Schema do contrato, um `openapi.yaml` para os endpoints internos, e os stubs (pseudocódigo) para o planner/executor. Quer que eu já gere o `JSON Schema` e o `openapi.yaml` agora?
