# A2F2 — Inteligência Estratégica

**Versão:** 0.1  
**Arquivo:** a2f2-inteligencia-estrategica.md  
**Autor:** Rick / A²F² — Atena

---

## 1. Finalidade

A **Inteligência Estratégica (IE)** define a camada de planejamento de alto nível do Protocolo A²F².  
Sua função é transformar objetivos de longo prazo, restrições e políticas em planos acionáveis que a **Inteligência Operacional** executará.

Ela controla:
- definição de metas e sub-objetivos;
- priorização de ações;
- alocação de recursos (tempo, atenção, orçamento virtual);
- avaliação de risco e trade-offs;
- geração de políticas e diretrizes (soft rules e hard rules).

---

## 2. Escopo

Inclui:
- Módulos de planejamento (curto, médio e longo prazo);
- Motor de priorização e scoring de oportunidades;
- Simulação de cenários e previsão de impacto;
- Regras de governança estratégica;
- Interface para criação/atualização de objetivos pelo usuário (Rick) e por agentes do sistema.

Exclui:
- Execução de baixo nível (delegada à Inteligência Operacional);
- Persistência física de logs (apenas define contratos; armazenamento é responsabilidade do Engine).

---

## 3. Principais responsabilidades

1. **Receber objetivos** — via UI, API ou eventos internos.  
2. **Modelar cenários** — avaliar alternativas com simulações rápidas.  
3. **Gerar planos** — sequências priorizadas de ações (planos primários e fallback).  
4. **Produzir políticas** — regras que afetam tomada de decisão (ex.: limite de gasto, aceitabilidade de risco).  
5. **Enviar ordens estratégicas** para a camada operacional (com meta, prazo e critérios de sucesso).  
6. **Avaliar resultados** e realimentar o ciclo (aprendizado).

---

## 4. Interfaces e contratos

### 4.1 Input (o que a IE consome)
- `objetivo.criar` — payload: { id, descrição, prioridade, horizonte, restrições }  
- `evento.contexto` — sinais do ambiente (mercado, usuário, sistema)  
- `dados_analíticos` — históricos, simulações, previsões

### 4.2 Output (o que a IE emite)
- `plano.gerado` — { plano_id, ações[], prioridades, métricas_esperadas, critérios_sucesso }  
- `politica.atualizada` — regras que alteram comportamento operacional  
- `alerta_estrategico` — recomendações humanas (ex.: revisão política)

### 4.3 API / Contrato RPC (exemplo)
- `POST /ie/objetivos` — criar objetivo  
- `GET /ie/planos/{id}` — recuperar plano  
- `POST /ie/simular` — solicitar simulação de cenário  
- `WS /ie/events` — transmissões em tempo real de decisões e alertas

(Implementação técnica e schemas em `openapi.yaml` do projeto.)

---

## 5. Integração com Inteligência Operacional

- **Handshake:** a IE publica `plano.gerado` com `SLAs` e critérios; a IO (operacional) confirma recebimento e solicita clarificações se necessário.  
- **Fallback:** se a IO reportar impossibilidade, a IE replaneja ou envia política de escalonamento.  
- **Métricas:** IE define métricas de sucesso (KPIs) que a IO reporta periodicamente.

---

## 6. Processo de decisão estratégica (fluxo resumido)

1. Recebe objetivo / sinal.  
2. Coleta dados relevantes.  
3. Gera N cenários (simulações).  
4. Avalia trade-offs com heurísticas/políticas.  
5. Seleciona plano preferido e planos alternativos.  
6. Publica `plano.gerado`.  
7. Monitora execução e ajusta se necessário.

---

## 7. Mecanismos de priorização (exemplo)

Cada proposta recebe um score calculado por:
- `impacto_estimado * confiança` ÷ `(custo_estimado ^ alfa)`

Parâmetros:
- `impacto_estimado` — benefício projetado.  
- `confiança` — qualidade dos dados/simul.  
- `custo_estimado` — recursos necessários.  
- `alfa` — fator de aversão a custo (configurável por governança).

---

## 8. Gestão de restrições e políticas

- Políticas são representadas como regras booleanas e soft-weights.  
- Regras hard (ex.: "não exceder X") bloqueiam planos que as infrinjam.  
- Regras soft aplicam penalties no scoring (reduzem prioridade).

---

## 9. Segurança e governança

- Todas decisões estratégicas devem ser logadas com: quem/sistema gerou, justificativa, versões de modelos e dados usados.  
- Versões das políticas devem ter controle semântico (semântica versionada) para permitir auditoria.  
- Mudanças em políticas críticas exigem aprovação (ou dupla assinatura) conforme `a2f2-governança.md`.

---

## 10. Exemplo simples de payloads

**Criar objetivo**
```json
{
  "id": "obj-20251119-001",
  "descricao": "Aumentar taxa de reutilização das apostas A até 20% em 3 meses",
  "prioridade": "alta",
  "horizonte": "90d",
  "restricoes": {
    "custo_max": 30,
    "evitar": ["reuso_total"]
  }
}
