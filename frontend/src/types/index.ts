export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  telefone: string;
  foto?: string;
  igreja: string;
  campus?: string;
  nivel_acesso: 'matriz' | 'setorial' | 'congregacao';
  scope_ids: string[];
  is_active: boolean;
  date_joined: string;
}

export interface Igreja {
  id: string;
  nome: string;
  cnpj?: string;
  endereco: string;
  telefone: string;
  email: string;
  site: string;
  logo?: string;
  plano: string;
  limite_membros: number;
  limite_mensagens: number;
  limite_storage: number;
  data_vencimento?: string;
  ativa: boolean;
  created_at: string;
  updated_at: string;
}

export interface Campus {
  id: string;
  igreja: string;
  nome: string;
  nivel: 'matriz' | 'setorial' | 'congregacao';
  campus_pai?: string;
  endereco: string;
  telefone: string;
  email: string;
  responsavel?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface Pessoa {
  id: string;
  nome_completo: string;
  nome_preferencia: string;
  cpf?: string;
  rg?: string;
  data_nascimento?: string;
  idade?: number;
  sexo: 'M' | 'F';
  estado_civil: 'solteiro' | 'casado' | 'divorciado' | 'viuvo';
  estado_civil_display: string;
  endereco: string;
  cep: string;
  cidade: string;
  estado: string;
  telefone: string;
  celular: string;
  email: string;
  profissao: string;
  escolaridade: string;
  status_membro: 'visitante' | 'congregado' | 'membro' | 'inativo';
  status_membro_display: string;
  data_primeira_visita?: string;
  data_conversao?: string;
  data_batismo?: string;
  data_membresia?: string;
  foto?: string;
  observacoes: string;
  campus: string;
  campus_nome: string;
  aceite_lgpd: boolean;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface Grupo {
  id: string;
  nome: string;
  descricao: string;
  tipo: 'celula' | 'classe' | 'ministerio' | 'outro';
  cor: string;
  lider?: string;
  lider_nome?: string;
  campus: string;
  campus_nome: string;
  endereco_reuniao: string;
  dia_semana: number;
  horario_inicio: string;
  horario_fim: string;
  ativo: boolean;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface Evento {
  id: string;
  titulo: string;
  descricao: string;
  tipo: 'culto' | 'conferencia' | 'retiro' | 'curso' | 'outro';
  data_inicio: string;
  data_fim: string;
  horario_inicio: string;
  horario_fim: string;
  local: string;
  endereco: string;
  capacidade_maxima?: number;
  valor_inscricao?: number;
  aceita_inscricoes: boolean;
  publico: boolean;
  campus: string;
  campus_nome: string;
  organizador: string;
  organizador_nome: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface LancamentoFinanceiro {
  id: string;
  tipo: 'receita' | 'despesa';
  descricao: string;
  valor: number;
  data_vencimento: string;
  data_pagamento?: string;
  status: 'pendente' | 'pago' | 'vencido' | 'cancelado';
  categoria: string;
  categoria_nome: string;
  centro_custo?: string;
  centro_custo_nome?: string;
  conta_bancaria?: string;
  conta_bancaria_nome?: string;
  pessoa?: string;
  pessoa_nome?: string;
  observacoes: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface ApiResponse<T> {
  count?: number;
  next?: string;
  previous?: string;
  results: T[];
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}
