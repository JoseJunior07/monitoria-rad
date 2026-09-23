cat > README.md << 'EOF'
# Sistema de Apoio à Monitoria

## Integrante(s)
- [Seu nome completo aqui]

## Contas de teste

| Usuário | Senha | Papel |
|---|---|---|
| ifpb | [ifpb] | Superusuário |
| Aluno2 | [alunoteste] | Aluno |
| Aluno3 | [alunoteste] | Aluno |
| Monitor4 | [alunoteste] | Monitor |
| Professor5 | [alunoteste] | Professor |

## Disciplinas cadastradas

- Rapid Application Development (RAD01) — monitorada por Monitor4
- Programação Distribuída (PD01) — sem monitor vinculado

## Requisitos implementados

- RF1 a RF9: implementados
- RF5 (assumir): usa método POST, pois altera o estado do sistema — GET deveria
  ser seguro/idempotente e não deveria alterar dados

## Requisitos pendentes

- Nenhum

## Desafio opcional (horários de atendimento)

- Não feito
EOF
