'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { Evento } from '@/types';
import apiClient from '@/lib/api';
import { formatDate, formatDateTime } from '@/lib/utils';
import { Calendar, Plus, MapPin, Clock, Users, DollarSign } from 'lucide-react';

export default function EventosPage() {
  const [eventos, setEventos] = useState<Evento[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [tipoFilter, setTipoFilter] = useState('');

  useEffect(() => {
    loadEventos();
  }, []);

  const loadEventos = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<{ results: Evento[] }>('/api/events/eventos/');
      setEventos(response.results || []);
    } catch (error) {
      console.error('Erro ao carregar eventos:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredEventos = eventos.filter(evento => {
    const matchesSearch = evento.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         evento.descricao.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTipo = !tipoFilter || evento.tipo === tipoFilter;
    return matchesSearch && matchesTipo;
  });

  const stats = [
    {
      title: 'Total de Eventos',
      value: eventos.length.toString(),
      description: 'Cadastrados no sistema',
      icon: Calendar,
    },
    {
      title: 'Cultos',
      value: eventos.filter(e => e.tipo === 'culto').length.toString(),
      description: 'Cultos programados',
      icon: Calendar,
    },
    {
      title: 'Conferências',
      value: eventos.filter(e => e.tipo === 'conferencia').length.toString(),
      description: 'Eventos especiais',
      icon: Calendar,
    },
    {
      title: 'Este Mês',
      value: eventos.filter(e => {
        const eventDate = new Date(e.data_inicio);
        const now = new Date();
        return eventDate.getMonth() === now.getMonth() && eventDate.getFullYear() === now.getFullYear();
      }).length.toString(),
      description: 'Eventos programados',
      icon: Calendar,
    },
  ];

  const getTypeColor = (tipo: string) => {
    const colors: Record<string, string> = {
      culto: 'bg-blue-100 text-blue-800',
      conferencia: 'bg-purple-100 text-purple-800',
      retiro: 'bg-green-100 text-green-800',
      curso: 'bg-yellow-100 text-yellow-800',
      outro: 'bg-gray-100 text-gray-800',
    };
    return colors[tipo] || 'bg-gray-100 text-gray-800';
  };

  const isEventPast = (dataInicio: string) => {
    return new Date(dataInicio) < new Date();
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Gestão de Eventos</h1>
            <p className="text-gray-600">Gerencie cultos, conferências e atividades</p>
          </div>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Novo Evento
          </Button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.title}
                </CardTitle>
                <stat.icon className="h-4 w-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-gray-500 mt-1">
                  {stat.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <CardTitle>Filtros</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <Input
                  placeholder="Buscar por título ou descrição..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full"
                />
              </div>
              <div className="w-full md:w-48">
                <select
                  value={tipoFilter}
                  onChange={(e) => setTipoFilter(e.target.value)}
                  className="w-full h-10 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Todos os tipos</option>
                  <option value="culto">Culto</option>
                  <option value="conferencia">Conferência</option>
                  <option value="retiro">Retiro</option>
                  <option value="curso">Curso</option>
                  <option value="outro">Outro</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Events Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredEventos.length === 0 ? (
            <div className="col-span-full">
              <Card>
                <CardContent className="text-center py-8">
                  <Calendar className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum evento encontrado</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {searchTerm || tipoFilter ? 'Tente ajustar os filtros.' : 'Comece criando um novo evento.'}
                  </p>
                </CardContent>
              </Card>
            </div>
          ) : (
            filteredEventos.map((evento) => (
              <Card key={evento.id} className={`hover:shadow-md transition-shadow ${
                isEventPast(evento.data_inicio) ? 'opacity-75' : ''
              }`}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(evento.tipo)}`}>
                      {evento.tipo.charAt(0).toUpperCase() + evento.tipo.slice(1)}
                    </span>
                    {isEventPast(evento.data_inicio) && (
                      <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                        Finalizado
                      </span>
                    )}
                  </div>
                  <CardTitle className="text-lg">{evento.titulo}</CardTitle>
                  <CardDescription className="line-clamp-2">
                    {evento.descricao}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center text-sm text-gray-600">
                    <Calendar className="w-4 h-4 mr-2" />
                    {formatDate(evento.data_inicio)}
                    {evento.data_fim !== evento.data_inicio && ` - ${formatDate(evento.data_fim)}`}
                  </div>

                  <div className="flex items-center text-sm text-gray-600">
                    <Clock className="w-4 h-4 mr-2" />
                    {evento.horario_inicio} - {evento.horario_fim}
                  </div>

                  <div className="flex items-center text-sm text-gray-600">
                    <MapPin className="w-4 h-4 mr-2" />
                    {evento.local}
                  </div>

                  <div className="flex items-center text-sm text-gray-600">
                    <Users className="w-4 h-4 mr-2" />
                    Organizador: {evento.organizador_nome}
                  </div>

                  {evento.valor_inscricao && (
                    <div className="flex items-center text-sm text-gray-600">
                      <DollarSign className="w-4 h-4 mr-2" />
                      R$ {evento.valor_inscricao.toFixed(2)}
                    </div>
                  )}

                  {evento.capacidade_maxima && (
                    <div className="text-sm text-gray-600">
                      <strong>Capacidade:</strong> {evento.capacidade_maxima} pessoas
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-3 border-t">
                    <div className="flex space-x-2">
                      {evento.aceita_inscricoes && (
                        <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                          Inscrições Abertas
                        </span>
                      )}
                      {evento.publico && (
                        <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                          Público
                        </span>
                      )}
                    </div>
                    <Button variant="outline" size="sm">
                      Ver Detalhes
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
