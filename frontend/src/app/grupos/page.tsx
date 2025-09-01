'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { Grupo } from '@/types';
import apiClient from '@/lib/api';
import { formatDate } from '@/lib/utils';
import { UserCheck, Plus, Users, Calendar, MapPin, Clock } from 'lucide-react';

export default function GruposPage() {
  const [grupos, setGrupos] = useState<Grupo[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [tipoFilter, setTipoFilter] = useState('');

  useEffect(() => {
    loadGrupos();
  }, []);

  const loadGrupos = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<{ results: Grupo[] }>('/api/groups/grupos/');
      setGrupos(response.results || []);
    } catch (error) {
      console.error('Erro ao carregar grupos:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredGrupos = grupos.filter(grupo => {
    const matchesSearch = grupo.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         grupo.descricao.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTipo = !tipoFilter || grupo.tipo === tipoFilter;
    return matchesSearch && matchesTipo;
  });

  const stats = [
    {
      title: 'Total de Grupos',
      value: grupos.length.toString(),
      description: 'Cadastrados no sistema',
      icon: UserCheck,
    },
    {
      title: 'Células',
      value: grupos.filter(g => g.tipo === 'celula').length.toString(),
      description: 'Grupos de células',
      icon: Users,
    },
    {
      title: 'Classes',
      value: grupos.filter(g => g.tipo === 'classe').length.toString(),
      description: 'Classes de ensino',
      icon: Users,
    },
    {
      title: 'Ministérios',
      value: grupos.filter(g => g.tipo === 'ministerio').length.toString(),
      description: 'Ministérios ativos',
      icon: Users,
    },
  ];

  const getDayName = (dayNumber: number) => {
    const days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
    return days[dayNumber] || 'N/A';
  };

  const getTypeColor = (tipo: string) => {
    const colors: Record<string, string> = {
      celula: 'bg-blue-100 text-blue-800',
      classe: 'bg-green-100 text-green-800',
      ministerio: 'bg-purple-100 text-purple-800',
      outro: 'bg-gray-100 text-gray-800',
    };
    return colors[tipo] || 'bg-gray-100 text-gray-800';
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
            <h1 className="text-2xl font-bold text-gray-900">Gestão de Grupos</h1>
            <p className="text-gray-600">Gerencie células, classes e ministérios</p>
          </div>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Novo Grupo
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
                  placeholder="Buscar por nome ou descrição..."
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
                  <option value="celula">Célula</option>
                  <option value="classe">Classe</option>
                  <option value="ministerio">Ministério</option>
                  <option value="outro">Outro</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Groups Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredGrupos.length === 0 ? (
            <div className="col-span-full">
              <Card>
                <CardContent className="text-center py-8">
                  <UserCheck className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum grupo encontrado</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {searchTerm || tipoFilter ? 'Tente ajustar os filtros.' : 'Comece criando um novo grupo.'}
                  </p>
                </CardContent>
              </Card>
            </div>
          ) : (
            filteredGrupos.map((grupo) => (
              <Card key={grupo.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: grupo.cor }}
                    />
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(grupo.tipo)}`}>
                      {grupo.tipo.charAt(0).toUpperCase() + grupo.tipo.slice(1)}
                    </span>
                  </div>
                  <CardTitle className="text-lg">{grupo.nome}</CardTitle>
                  <CardDescription className="line-clamp-2">
                    {grupo.descricao}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {grupo.lider_nome && (
                    <div className="flex items-center text-sm text-gray-600">
                      <Users className="w-4 h-4 mr-2" />
                      Líder: {grupo.lider_nome}
                    </div>
                  )}
                  
                  <div className="flex items-center text-sm text-gray-600">
                    <MapPin className="w-4 h-4 mr-2" />
                    {grupo.campus_nome}
                  </div>

                  <div className="flex items-center text-sm text-gray-600">
                    <Calendar className="w-4 h-4 mr-2" />
                    {getDayName(grupo.dia_semana)}
                  </div>

                  <div className="flex items-center text-sm text-gray-600">
                    <Clock className="w-4 h-4 mr-2" />
                    {grupo.horario_inicio} - {grupo.horario_fim}
                  </div>

                  {grupo.endereco_reuniao && (
                    <div className="text-sm text-gray-600">
                      <strong>Local:</strong> {grupo.endereco_reuniao}
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-3 border-t">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      grupo.ativo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {grupo.ativo ? 'Ativo' : 'Inativo'}
                    </span>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">
                        Ver Detalhes
                      </Button>
                    </div>
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
